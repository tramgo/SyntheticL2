from __future__ import annotations

import argparse
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE239_DIR = Path("outputs/phase239")
DEFAULT_OUTPUT_DIR = Path("outputs/phase240")
DEFAULT_DEST_ROOT = Path("real_data_sample/l2_unseen_validation")
STORAGE_ACCOUNT = "stctrade1ramic"
FILE_SHARE = "ctrade1-l2-data"
MAX_WORKERS = 16
PROGRESS_EVERY_FILES = 250
_THREAD_LOCAL = threading.local()


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def require_sas() -> str:
    sas = os.environ.get("AZURE_STORAGE_SAS_TOKEN")
    if not sas:
        raise RuntimeError("AZURE_STORAGE_SAS_TOKEN is required in the process environment; it is not written to disk.")
    return sas


def make_share_client():
    import truststore
    from azure.storage.fileshare import ShareServiceClient

    truststore.inject_into_ssl()
    sas = require_sas()
    service = ShareServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT}.file.core.windows.net",
        credential=sas,
    )
    return service.get_share_client(FILE_SHARE)


def thread_share_client():
    client = getattr(_THREAD_LOCAL, "share_client", None)
    if client is None:
        client = make_share_client()
        _THREAD_LOCAL.share_client = client
    return client


def target_dates_from_phase239(phase239_dir: Path, max_dates: int | None = None) -> list[str]:
    targets = read_csv(phase239_dir / "phase239_target_unseen_dates.csv")
    if targets.empty:
        raise FileNotFoundError(phase239_dir / "phase239_target_unseen_dates.csv")
    dates = targets["target_trade_date"].astype(str).tolist()
    return dates[:max_dates] if max_dates else dates


def parse_trade_dates(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    dates = [part.strip() for part in raw.split(",") if part.strip()]
    return dates or None


def list_remote_files_for_date(share, trade_date: str) -> list[dict[str, Any]]:
    base = f"raw_l2/trade_date={trade_date}/exchange=NSE"
    base_dir = share.get_directory_client(base)
    symbols = [
        item["name"].split("=", 1)[1]
        for item in base_dir.list_directories_and_files()
        if str(item["name"]).startswith("symbol=")
    ]
    rows: list[dict[str, Any]] = []
    for symbol in sorted(symbols):
        remote_dir = f"{base}/symbol={symbol}"
        directory = share.get_directory_client(remote_dir)
        for item in directory.list_directories_and_files():
            if item.get("is_directory"):
                continue
            name = str(item["name"])
            size = int(item.get("size") or 0)
            remote_path = f"{remote_dir}/{name}"
            local_path = DEFAULT_DEST_ROOT / f"trade_date={trade_date}" / "exchange=NSE" / f"symbol={symbol}" / name
            rows.append(
                {
                    "trade_date": trade_date,
                    "exchange": "NSE",
                    "symbol": symbol,
                    "remote_path": remote_path,
                    "local_path": str(local_path),
                    "remote_size": size,
                }
            )
    return rows


def write_listing_progress(output_dir: Path, trade_dates: list[str], completed_dates: list[str], rows: int, bytes_seen: int, started: float) -> None:
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "target_trade_dates": trade_dates,
        "listed_trade_dates": completed_dates,
        "listed_date_count": len(completed_dates),
        "target_date_count": len(trade_dates),
        "listed_remote_files": rows,
        "listed_remote_bytes": bytes_seen,
        "elapsed_seconds": time.time() - started,
    }
    (output_dir / "phase240_listing_progress.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_remote_manifest(share, trade_dates: list[str], output_dir: Path | None = None, started: float | None = None) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    completed_dates: list[str] = []
    for d in trade_dates:
        rows_for_date = list_remote_files_for_date(share, d)
        rows.extend(rows_for_date)
        completed_dates.append(d)
        if output_dir is not None and started is not None:
            write_listing_progress(
                output_dir,
                trade_dates=trade_dates,
                completed_dates=completed_dates,
                rows=len(rows),
                bytes_seen=sum(int(row.get("remote_size") or 0) for row in rows),
                started=started,
            )
    return pd.DataFrame(rows)


def needs_download(row: dict[str, Any]) -> bool:
    path = Path(str(row["local_path"]))
    if not path.exists():
        return True
    try:
        return path.stat().st_size != int(row["remote_size"])
    except OSError:
        return True


def download_one(row: dict[str, Any]) -> dict[str, Any]:
    share = thread_share_client()
    local_path = Path(str(row["local_path"]))
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if not needs_download(row):
        return {**row, "download_status": "skipped_existing", "downloaded_bytes": int(row["remote_size"]), "error": ""}
    temp_path = local_path.with_suffix(local_path.suffix + ".part")
    try:
        file_client = share.get_file_client(str(row["remote_path"]))
        downloader = file_client.download_file()
        with temp_path.open("wb") as fh:
            downloader.readinto(fh)
        if temp_path.stat().st_size != int(row["remote_size"]):
            raise IOError(f"size mismatch downloaded={temp_path.stat().st_size} expected={row['remote_size']}")
        temp_path.replace(local_path)
        return {**row, "download_status": "downloaded", "downloaded_bytes": int(row["remote_size"]), "error": ""}
    except Exception as exc:
        try:
            if temp_path.exists():
                temp_path.unlink()
        except OSError:
            pass
        return {**row, "download_status": "failed", "downloaded_bytes": 0, "error": repr(exc)[:500]}


def write_progress(output_dir: Path, results: list[dict[str, Any]], total_files: int, started: float) -> None:
    completed = len(results)
    downloaded = sum(1 for r in results if r.get("download_status") == "downloaded")
    skipped = sum(1 for r in results if r.get("download_status") == "skipped_existing")
    failed = sum(1 for r in results if r.get("download_status") == "failed")
    bytes_done = sum(int(r.get("downloaded_bytes") or 0) for r in results)
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "completed_files": completed,
        "total_files": total_files,
        "downloaded_files": downloaded,
        "skipped_existing_files": skipped,
        "failed_files": failed,
        "completed_bytes": bytes_done,
        "elapsed_seconds": time.time() - started,
    }
    (output_dir / "phase240_download_progress.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_date_summary(manifest: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    if manifest.empty:
        return pd.DataFrame()
    left = manifest.groupby("trade_date", sort=True).agg(
        remote_files=("remote_path", "count"),
        remote_bytes=("remote_size", "sum"),
        symbols=("symbol", "nunique"),
    )
    if results.empty:
        left["completed_files"] = 0
        left["downloaded_files"] = 0
        left["skipped_existing_files"] = 0
        left["failed_files"] = 0
        left["completed_bytes"] = 0
        return left.reset_index()
    right = results.groupby("trade_date", sort=True).agg(
        completed_files=("remote_path", "count"),
        downloaded_files=("download_status", lambda s: int((s == "downloaded").sum())),
        skipped_existing_files=("download_status", lambda s: int((s == "skipped_existing").sum())),
        failed_files=("download_status", lambda s: int((s == "failed").sum())),
        completed_bytes=("downloaded_bytes", "sum"),
    )
    return left.join(right, how="left").fillna(0).reset_index()


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase240 Unseen Real L2 Download Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase240 downloads raw unseen real L2 dates from Azure Files using a process-provided SAS token.",
        "The SAS value is not written to disk. Downloads are resumable by local file-size checks.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase239_dir: Path = DEFAULT_PHASE239_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    trade_dates: list[str] | None = None,
    max_dates: int | None = None,
    max_files: int | None = None,
    workers: int = MAX_WORKERS,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    share = make_share_client()
    if trade_dates is None:
        trade_dates = target_dates_from_phase239(phase239_dir, max_dates=max_dates)
    elif max_dates:
        trade_dates = trade_dates[:max_dates]
    write_listing_progress(output_dir, trade_dates=trade_dates, completed_dates=[], rows=0, bytes_seen=0, started=started)
    manifest = build_remote_manifest(share, trade_dates, output_dir=output_dir, started=started)
    if max_files:
        manifest = manifest.head(max_files).copy()
    manifest.to_csv(output_dir / "phase240_remote_file_manifest.csv", index=False)
    to_process = [row for row in manifest.to_dict("records") if needs_download(row)]
    already = [
        {**row, "download_status": "skipped_existing", "downloaded_bytes": int(row["remote_size"]), "error": ""}
        for row in manifest.to_dict("records")
        if not needs_download(row)
    ]
    results: list[dict[str, Any]] = list(already)
    total_files = int(len(manifest))
    write_progress(output_dir, results, total_files, started)
    with ThreadPoolExecutor(max_workers=max(1, int(workers))) as executor:
        futures = [executor.submit(download_one, row) for row in to_process]
        for fut in as_completed(futures):
            results.append(fut.result())
            if len(results) % PROGRESS_EVERY_FILES == 0:
                write_progress(output_dir, results, total_files, started)
    write_progress(output_dir, results, total_files, started)
    result_frame = pd.DataFrame(results)
    result_frame.to_csv(output_dir / "phase240_download_file_ledger.csv", index=False)
    date_summary = build_date_summary(manifest, result_frame)
    date_summary.to_csv(output_dir / "phase240_download_date_summary.csv", index=False)
    failed_files = int((result_frame["download_status"].astype(str) == "failed").sum()) if not result_frame.empty else total_files
    completed_files = int(len(result_frame))
    phase239_dates = target_dates_from_phase239(phase239_dir, max_dates=None)
    partial_attempt = int(bool(max_dates or max_files or trade_dates != phase239_dates))
    completed_dates = 0 if max_files else (int((date_summary["failed_files"].astype(int).eq(0) & date_summary["completed_files"].astype(int).eq(date_summary["remote_files"].astype(int))).sum()) if not date_summary.empty else 0)
    full_attempt_complete = int(failed_files == 0 and completed_files == total_files and partial_attempt == 0)
    acceptance = pd.DataFrame(
        [
            ("phase240_unseen_raw_l2_download_complete", full_attempt_complete, "Whether the full unseen raw L2 plan downloaded or already existed"),
            ("phase240_partial_attempt", partial_attempt, "Whether --max-dates or --max-files limited the run"),
            ("phase240_target_trade_dates", ";".join(trade_dates), "Target unseen dates attempted"),
            ("phase240_remote_manifest_files", total_files, "Remote files in attempted manifest"),
            ("phase240_remote_manifest_bytes", int(manifest["remote_size"].sum()) if not manifest.empty else 0, "Remote bytes in attempted manifest"),
            ("phase240_completed_files", completed_files, "Files processed"),
            ("phase240_failed_files", failed_files, "Files failed"),
            ("phase240_completed_dates", completed_dates, "Dates fully downloaded"),
            ("phase240_elapsed_seconds", time.time() - started, "Elapsed seconds"),
            ("phase240_validation_execution_allowed_now", 0, "Phase240 does not run validation"),
            ("phase240_strategy_promotion_allowed", 0, "No strategy promotion from Phase240"),
            ("phase240_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase240"),
            ("phase240_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase240"),
            ("phase240_next_best_action", "run_phase241_materialize_unseen_real_event_bars_for_phase238_candidate_no_paper_live" if full_attempt_complete and completed_dates >= len(trade_dates) else "resume_phase240_unseen_raw_l2_download_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    acceptance.to_csv(output_dir / "phase240_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase240_unseen_l2_download_report.md",
        {
            "Acceptance Summary": acceptance,
            "Date Summary": date_summary,
            "Failed Files": result_frame[result_frame["download_status"].astype(str).eq("failed")].head(20) if not result_frame.empty else pd.DataFrame(),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest_payload = {
        "generated_utc": generated_utc,
        "scope": "phase240_unseen_raw_l2_download",
        **reproducibility_fields(
            artifact_id="phase240",
            generated_utc=generated_utc,
            inputs={"phase239_dir": str(phase239_dir)},
            parameters={
                "trade_dates": trade_dates,
                "max_dates": max_dates,
                "max_files": max_files,
                "workers": workers,
                "storage_account": STORAGE_ACCOUNT,
                "file_share": FILE_SHARE,
                "validation_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "remote_file_manifest": str(output_dir / "phase240_remote_file_manifest.csv"),
                "download_file_ledger": str(output_dir / "phase240_download_file_ledger.csv"),
                "download_date_summary": str(output_dir / "phase240_download_date_summary.csv"),
                "acceptance_summary": str(output_dir / "phase240_acceptance_summary.csv"),
                "report": str(output_dir / "phase240_unseen_l2_download_report.md"),
            },
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
        ),
    }
    (output_dir / "phase240_unseen_l2_download_manifest.json").write_text(json.dumps(manifest_payload, indent=2), encoding="utf-8")
    return manifest_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Download unseen raw L2 dates from Azure Files.")
    parser.add_argument("--phase239-dir", type=Path, default=DEFAULT_PHASE239_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--trade-dates", type=str, default=None, help="Comma-separated YYYY-MM-DD shards to download instead of the Phase239 full target list.")
    parser.add_argument("--max-dates", type=int, default=None)
    parser.add_argument("--max-files", type=int, default=None)
    parser.add_argument("--workers", type=int, default=MAX_WORKERS)
    args = parser.parse_args()
    manifest = run(
        phase239_dir=args.phase239_dir,
        output_dir=args.output_dir,
        trade_dates=parse_trade_dates(args.trade_dates),
        max_dates=args.max_dates,
        max_files=args.max_files,
        workers=args.workers,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
