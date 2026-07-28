from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

import requests

try:
    import truststore
except ImportError:  # pragma: no cover - environment guard
    truststore = None


DEFAULT_ACCOUNT = "stctrade1ramic"
DEFAULT_SHARE = "ctrade1-l2-data"
DEFAULT_REMOTE_ROOT = "raw_l2"
DEFAULT_TARGET_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase192")
DEFAULT_EXISTING_SPLIT_DATES = {"2026-07-08", "2026-07-09", "2026-07-10", "2026-07-13", "2026-07-14"}
FORBIDDEN_OUTPUTS = "test_replay_execution;test_result;promotion;paper_live_acceptance;orders;fills;pnl_replay;profitability_claim"


@dataclass(frozen=True)
class RemoteFile:
    remote_path: str
    relative_path: Path
    size: int


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_sas(value: str) -> str:
    sas = value.strip()
    if sas.startswith("?"):
        sas = sas[1:]
    if not sas:
        raise ValueError("SAS token is empty. Set AZURE_STORAGE_SAS_TOKEN or pass --sas-token-env.")
    return sas


def encoded_path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in path.strip("/").split("/"))


class AzureFileShareClient:
    def __init__(self, account: str, share: str, sas: str, timeout: int = 60) -> None:
        self.account = account
        self.share = share
        self.sas = normalize_sas(sas)
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {"x-ms-version": "2022-11-02"}

    def _directory_url(self, directory: str, marker: str = "") -> str:
        path = encoded_path(directory)
        url = (
            f"https://{self.account}.file.core.windows.net/{self.share}/{path}"
            f"?restype=directory&comp=list&{self.sas}"
        )
        if marker:
            url += f"&marker={quote(marker, safe='')}"
        return url

    def _file_url(self, remote_path: str) -> str:
        return f"https://{self.account}.file.core.windows.net/{self.share}/{encoded_path(remote_path)}?{self.sas}"

    def list_directory(self, directory: str) -> tuple[list[str], list[tuple[str, int]]]:
        directories: list[str] = []
        files: list[tuple[str, int]] = []
        marker = ""
        while True:
            response = self.session.get(self._directory_url(directory, marker), headers=self.headers, timeout=self.timeout)
            if response.status_code != 200:
                raise RuntimeError(f"Azure Files list failed for {directory}: HTTP {response.status_code} {response.text[:300]}")
            root = ET.fromstring(response.text)
            for item in root.findall(".//Entries/Directory"):
                name = item.findtext("Name")
                if name:
                    directories.append(name)
            for item in root.findall(".//Entries/File"):
                name = item.findtext("Name")
                size_text = item.findtext("Properties/Content-Length") or "0"
                files.append((name, int(size_text)))
            marker = root.findtext("NextMarker") or ""
            if not marker:
                break
        return directories, files

    def iter_files(self, directory: str) -> Iterable[RemoteFile]:
        stack = [directory.rstrip("/")]
        root_prefix = directory.rstrip("/") + "/"
        while stack:
            current = stack.pop()
            directories, files = self.list_directory(current)
            for name in sorted(directories, reverse=True):
                stack.append(f"{current}/{name}")
            for name, size in files:
                remote_path = f"{current}/{name}"
                relative = Path(remote_path.removeprefix(root_prefix))
                yield RemoteFile(remote_path=remote_path, relative_path=relative, size=size)

    def download_file(self, item: RemoteFile, target_root: Path, overwrite: bool = False) -> dict[str, object]:
        target = target_root / item.relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size == item.size and not overwrite:
            return {
                "remote_path": item.remote_path,
                "local_path": str(target),
                "bytes": item.size,
                "status": "skipped_existing",
                "error": "",
            }
        temp = target.with_suffix(target.suffix + ".partial")
        try:
            with self.session.get(self._file_url(item.remote_path), headers=self.headers, timeout=self.timeout, stream=True) as response:
                if response.status_code != 200:
                    return {
                        "remote_path": item.remote_path,
                        "local_path": str(target),
                        "bytes": item.size,
                        "status": "failed",
                        "error": f"HTTP {response.status_code}",
                    }
                with temp.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
            if temp.stat().st_size != item.size:
                return {
                    "remote_path": item.remote_path,
                    "local_path": str(target),
                    "bytes": item.size,
                    "status": "failed",
                    "error": f"size_mismatch expected={item.size} actual={temp.stat().st_size}",
                }
            temp.replace(target)
            return {
                "remote_path": item.remote_path,
                "local_path": str(target),
                "bytes": item.size,
                "status": "downloaded",
                "error": "",
            }
        except Exception as exc:  # noqa: BLE001 - safe ledger error, URL/signature omitted
            return {
                "remote_path": item.remote_path,
                "local_path": str(target),
                "bytes": item.size,
                "status": "failed",
                "error": f"{type(exc).__name__}: {str(exc)[:180]}",
            }
        finally:
            if temp.exists():
                try:
                    temp.unlink()
                except OSError:
                    pass


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def metric_rows(rows: list[tuple[str, object, str]]) -> list[dict[str, object]]:
    return [{"metric": metric, "value": value, "description": description} for metric, value, description in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase192 Azure Files real L2 validation-date downloader.")
    parser.add_argument("--dates", nargs="+", required=True, help="New trade dates to download, e.g. 2026-07-15.")
    parser.add_argument("--sas-token-env", default="AZURE_STORAGE_SAS_TOKEN")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT)
    parser.add_argument("--share", default=DEFAULT_SHARE)
    parser.add_argument("--remote-root", default=DEFAULT_REMOTE_ROOT)
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-workers", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--list-only", action="store_true")
    args = parser.parse_args()

    if truststore is not None:
        truststore.inject_into_ssl()

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    generated = utc_now()
    requested_dates = [date.strip() for raw in args.dates for date in raw.split(",") if date.strip()]
    sas = os.environ.get(args.sas_token_env, "").strip()

    available_rows: list[dict[str, object]] = []
    date_rows: list[dict[str, object]] = []
    download_rows: list[dict[str, object]] = []
    failed = 0
    downloaded = 0
    skipped = 0
    remote_file_count = 0
    remote_bytes = 0

    if not sas:
        failed = 1
        next_action = f"set_{args.sas_token_env}_then_rerun_phase192_real_validation_date_download"
        available_dates: list[str] = []
    else:
        client = AzureFileShareClient(args.account, args.share, sas, timeout=args.timeout)
        available_dirs, _ = client.list_directory(args.remote_root)
        available_dates = sorted(name.split("=", 1)[1] for name in available_dirs if name.startswith("trade_date="))
        for trade_date in available_dates:
            available_rows.append(
                {
                    "trade_date": trade_date,
                    "remote_partition": f"{args.remote_root}/trade_date={trade_date}",
                    "already_in_split_before_phase192": int(trade_date in DEFAULT_EXISTING_SPLIT_DATES),
                    "requested_for_download": int(trade_date in requested_dates),
                }
            )
        for trade_date in requested_dates:
            date_remote = f"{args.remote_root}/trade_date={trade_date}"
            date_target = args.target_root / f"trade_date={trade_date}"
            status = "available"
            error = ""
            files: list[RemoteFile] = []
            try:
                if trade_date not in available_dates:
                    status = "missing_remote"
                    error = "date_not_listed_under_remote_root"
                else:
                    files = list(client.iter_files(date_remote))
                    remote_file_count += len(files)
                    remote_bytes += sum(item.size for item in files)
                    if args.list_only:
                        status = "listed_only"
                    else:
                        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.max_workers)) as executor:
                            futures = [
                                executor.submit(client.download_file, item, date_target, args.overwrite)
                                for item in files
                            ]
                            for future in concurrent.futures.as_completed(futures):
                                row = future.result()
                                download_rows.append(row)
                                if row["status"] == "downloaded":
                                    downloaded += 1
                                elif row["status"] == "skipped_existing":
                                    skipped += 1
                                else:
                                    failed += 1
                        status = "downloaded_or_skipped" if failed == 0 else "download_failed"
            except Exception as exc:  # noqa: BLE001 - safe error, no URL or SAS
                failed += 1
                status = "failed"
                error = f"{type(exc).__name__}: {str(exc)[:220]}"
            local_files = list(date_target.rglob("*.parquet")) if date_target.exists() else []
            date_rows.append(
                {
                    "trade_date": trade_date,
                    "remote_partition": date_remote,
                    "target_partition": str(date_target),
                    "status": status,
                    "remote_files": len(files),
                    "remote_bytes": sum(item.size for item in files),
                    "local_parquet_files_after": len(local_files),
                    "local_bytes_after": sum(path.stat().st_size for path in local_files),
                    "error": error,
                }
            )
        if failed:
            next_action = "fix_phase192_download_errors_before_materialization"
        elif args.list_only:
            next_action = "rerun_phase192_without_list_only_to_download_selected_validation_dates"
        else:
            next_action = "run_phase172_phase176_phase181_then_validation_breadth_replay"

    acceptance = metric_rows(
        [
            ("phase192_requested_date_rows", len(requested_dates), "Dates requested for Phase192 download"),
            ("phase192_azure_available_date_rows", len(available_dates), "Dates listed under Azure Files raw_l2"),
            ("phase192_new_remote_dates_beyond_existing_split", len(set(available_dates).difference(DEFAULT_EXISTING_SPLIT_DATES)), "Azure dates not in the pre-Phase192 local split"),
            ("phase192_remote_files_selected", remote_file_count, "Remote files listed for requested dates"),
            ("phase192_remote_bytes_selected", remote_bytes, "Remote bytes listed for requested dates"),
            ("phase192_downloaded_files", downloaded, "Files downloaded in this run"),
            ("phase192_skipped_existing_files", skipped, "Files already present with matching size"),
            ("phase192_failed_files_or_dates", failed, "Failed file/date operations"),
            ("phase192_list_only", int(args.list_only), "1 means no files were downloaded"),
            ("phase192_test_replay_execution", 0, "Phase192 does not execute untouched test replay"),
            ("phase192_test_result_allowed", 0, "Phase192 does not emit a test result"),
            ("phase192_promotion_allowed", 0, "Phase192 does not open promotion"),
            ("phase192_paper_or_live_acceptance_allowed", 0, "Phase192 keeps paper/live closed"),
            ("phase192_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase192_next_best_action", next_action, "Recommended next milestone"),
        ]
    )

    write_csv(output_dir / "phase192_azure_available_dates.csv", available_rows, ["trade_date", "remote_partition", "already_in_split_before_phase192", "requested_for_download"])
    write_csv(output_dir / "phase192_requested_date_download_summary.csv", date_rows, ["trade_date", "remote_partition", "target_partition", "status", "remote_files", "remote_bytes", "local_parquet_files_after", "local_bytes_after", "error"])
    write_csv(output_dir / "phase192_download_file_ledger.csv", download_rows, ["remote_path", "local_path", "bytes", "status", "error"])
    write_csv(output_dir / "phase192_real_validation_date_download_acceptance_summary.csv", acceptance, ["metric", "value", "description"])

    report = [
        "# Phase192 Azure Real Validation-Date Download",
        "",
        f"Generated UTC: {generated}",
        "",
        "Phase192 downloads additional real Zerodha top-five market-by-price WebSocket L2 date partitions for validation breadth.",
        "It does not run untouched test replay, emit a test result, open promotion, or make paper/live claims.",
        "",
        "## Requested Dates",
        "",
        ", ".join(requested_dates),
        "",
        "## Acceptance Summary",
        "",
    ]
    report.extend(",".join(map(str, row.values())) for row in acceptance)
    (output_dir / "phase192_real_validation_date_download_report.md").write_text("\n".join(report), encoding="utf-8")

    manifest = {
        "generated_utc": generated,
        "scope": "phase192_azure_real_validation_date_download",
        "requested_dates": requested_dates,
        "target_root": str(args.target_root),
        "sas_policy": "read_from_environment_only_not_persisted",
        "elapsed_seconds": round(time.time() - started, 3),
        "forbidden_outputs": FORBIDDEN_OUTPUTS,
        "outputs": {
            "available_dates": str(output_dir / "phase192_azure_available_dates.csv"),
            "requested_date_summary": str(output_dir / "phase192_requested_date_download_summary.csv"),
            "download_file_ledger": str(output_dir / "phase192_download_file_ledger.csv"),
            "acceptance_summary": str(output_dir / "phase192_real_validation_date_download_acceptance_summary.csv"),
            "report": str(output_dir / "phase192_real_validation_date_download_report.md"),
            "manifest": str(output_dir / "phase192_real_validation_date_download_manifest.json"),
        },
    }
    (output_dir / "phase192_real_validation_date_download_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    for row in acceptance:
        print(f"{row['metric']}={row['value']}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
