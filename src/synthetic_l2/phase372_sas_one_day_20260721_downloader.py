from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase340_official_catalyst_calendar_acquisition_precommit import TICKERS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION

try:  # pragma: no cover - environment dependent
    import truststore

    truststore.inject_into_ssl()
    TRUSTSTORE_INJECTED = 1
except Exception:  # pragma: no cover - environment dependent
    TRUSTSTORE_INJECTED = 0


DEFAULT_OUTPUT_DIR = Path("outputs/phase372")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_ACCOUNT = "stctrade1ramic"
DEFAULT_TARGET_DATE = "2026-07-21"
DEFAULT_FILE_SHARE = "ctrade1-l2-data"
SAS_ENV_NAMES = [
    "AZURE_BLOB_SERVICE_SAS_URL",
    "STCTRADE1RAMIC_BLOB_SAS_URL",
    "AZURE_FILE_SERVICE_SAS_URL",
    "STCTRADE1RAMIC_FILE_SAS_URL",
    "AZURE_STORAGE_SAS_TOKEN",
    "STCTRADE1RAMIC_SAS_TOKEN",
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def sas_from_env() -> dict[str, str]:
    for name in SAS_ENV_NAMES:
        value = os.environ.get(name, "").strip()
        if value:
            return {"env_name": name, "value": value}
    return {"env_name": "", "value": ""}


def normalize_sas_source(raw: str) -> dict[str, str]:
    if raw.startswith("https://"):
        parsed = urllib.parse.urlparse(raw)
        service = "file" if ".file." in parsed.netloc else "blob"
        return {"endpoint": f"{parsed.scheme}://{parsed.netloc}", "sas": parsed.query.lstrip("?"), "service": service}
    return {"endpoint": f"https://{DEFAULT_ACCOUNT}.blob.core.windows.net", "sas": raw.lstrip("?"), "service": "blob"}


def signed_url(endpoint: str, path: str, sas: str, params: dict[str, str] | None = None) -> str:
    params = dict(params or {})
    prefix = urllib.parse.urlencode(params)
    query = f"{prefix}&{sas}" if prefix else sas
    return f"{endpoint.rstrip('/')}/{path.lstrip('/')}?{query}"


def service_url(endpoint: str, sas: str, params: dict[str, str]) -> str:
    return f"{endpoint.rstrip('/')}/?{urllib.parse.urlencode(params)}&{sas}"


def http_get_bytes(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "SyntheticL2Phase372/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def list_containers(endpoint: str, sas: str, timeout: int) -> list[str]:
    raw = http_get_bytes(service_url(endpoint, sas, {"comp": "list"}), timeout)
    root = ET.fromstring(raw)
    return [elem.findtext("Name", "") for elem in root.findall(".//Container") if elem.findtext("Name", "")]


def list_blobs(endpoint: str, container: str, sas: str, prefix: str, timeout: int) -> list[str]:
    blobs: list[str] = []
    marker = ""
    while True:
        params = {"restype": "container", "comp": "list", "prefix": prefix}
        if marker:
            params["marker"] = marker
        raw = http_get_bytes(signed_url(endpoint, container, sas, params), timeout)
        root = ET.fromstring(raw)
        blobs.extend([elem.findtext("Name", "") for elem in root.findall(".//Blob") if elem.findtext("Name", "")])
        marker = root.findtext("NextMarker", "") or ""
        if not marker:
            break
    return blobs


def file_url(endpoint: str, share: str, path: str, sas: str, params: dict[str, str] | None = None) -> str:
    quoted = urllib.parse.quote(path.strip("/"), safe="/=._-")
    prefix = urllib.parse.urlencode(params or {})
    query = f"{prefix}&{sas}" if prefix else sas
    return f"{endpoint.rstrip('/')}/{share}/{quoted}?{query}"


def list_file_directory(endpoint: str, share: str, sas: str, path: str, timeout: int) -> tuple[list[str], list[str]]:
    raw = http_get_bytes(file_url(endpoint, share, path, sas, {"restype": "directory", "comp": "list"}), timeout)
    root = ET.fromstring(raw)
    dirs = [elem.findtext("Name", "") for elem in root.findall(".//Directory") if elem.findtext("Name", "")]
    files = [elem.findtext("Name", "") for elem in root.findall(".//File") if elem.findtext("Name", "")]
    return dirs, files


def parse_raw_l2_blob(blob: str, target_date: str) -> dict[str, str] | None:
    pattern = rf"raw_l2/trade_date={re.escape(target_date)}/exchange=([^/]+)/symbol=([^/]+)/(.+\.parquet)$"
    match = re.search(pattern, blob)
    if not match:
        return None
    return {"trade_date": target_date, "exchange": match.group(1), "symbol": match.group(2).upper(), "relative_file": match.group(3)}


def discover_target_rows(endpoint: str, sas: str, target_date: str, symbols: list[str], timeout: int, explicit_container: str) -> tuple[pd.DataFrame, list[str]]:
    containers = [explicit_container] if explicit_container else list_containers(endpoint, sas, timeout)
    rows: list[dict[str, str]] = []
    symbol_set = set(symbols)
    prefix = f"raw_l2/trade_date={target_date}/exchange=NSE/"
    for container in containers:
        if not container:
            continue
        for blob in list_blobs(endpoint, container, sas, prefix, timeout):
            parsed = parse_raw_l2_blob(blob, target_date)
            if parsed and parsed["exchange"] == "NSE" and parsed["symbol"] in symbol_set:
                parsed["container"] = container
                parsed["blob"] = blob
                rows.append(parsed)
        if rows:
            break
    return pd.DataFrame(rows), containers


def discover_target_file_rows(endpoint: str, sas: str, target_date: str, symbols: list[str], timeout: int, share: str) -> tuple[pd.DataFrame, list[str]]:
    rows: list[dict[str, str]] = []
    root_path = f"raw_l2/trade_date={target_date}/exchange=NSE"
    dirs, _ = list_file_directory(endpoint, share, sas, root_path, timeout)
    symbol_set = set(symbols)
    for dirname in dirs:
        if not dirname.startswith("symbol="):
            continue
        symbol = dirname.split("=", 1)[1].upper()
        if symbol not in symbol_set:
            continue
        symbol_path = f"{root_path}/{dirname}"
        _, files = list_file_directory(endpoint, share, sas, symbol_path, timeout)
        for filename in files:
            if filename.endswith(".parquet"):
                rows.append(
                    {
                        "trade_date": target_date,
                        "exchange": "NSE",
                        "symbol": symbol,
                        "relative_file": filename,
                        "share": share,
                        "file_path": f"{symbol_path}/{filename}",
                    }
                )
    return pd.DataFrame(rows), [share]


def local_target_inventory(real_root: Path, target_date: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    target_root = real_root / f"trade_date={target_date}" / "exchange=NSE"
    if not target_root.exists():
        return pd.DataFrame(columns=["trade_date", "symbol", "parquet_files", "bytes"])
    for symbol_dir in target_root.glob("symbol=*"):
        symbol = symbol_dir.name.split("=", 1)[1].upper()
        files = list(symbol_dir.glob("*.parquet"))
        rows.append({"trade_date": target_date, "symbol": symbol, "parquet_files": len(files), "bytes": int(sum(path.stat().st_size for path in files))})
    return pd.DataFrame(rows, columns=["trade_date", "symbol", "parquet_files", "bytes"])


def download_rows(endpoint: str, sas: str, rows: pd.DataFrame, real_root: Path, timeout: int, dry_run: bool, max_files: int) -> pd.DataFrame:
    if rows.empty:
        return pd.DataFrame(columns=["trade_date", "exchange", "symbol", "container", "blob_path_redacted", "local_path", "status", "bytes_written", "secret_material_recorded"])
    if max_files > 0:
        rows = rows.head(max_files).copy()
    out_rows: list[dict[str, Any]] = []
    for row in rows.itertuples(index=False):
        local_dir = real_root / f"trade_date={row.trade_date}" / f"exchange={row.exchange}" / f"symbol={row.symbol}"
        local_path = local_dir / Path(row.relative_file).name
        bytes_written = 0
        status = "dry_run"
        if not dry_run:
            local_dir.mkdir(parents=True, exist_ok=True)
            data = http_get_bytes(signed_url(endpoint, f"{row.container}/{row.blob}", sas), timeout)
            local_path.write_bytes(data)
            bytes_written = len(data)
            status = "downloaded"
        out_rows.append(
            {
                "trade_date": row.trade_date,
                "exchange": row.exchange,
                "symbol": row.symbol,
                "container": row.container,
                "blob_path_redacted": re.sub(r"part-[^/]+\.parquet$", "part-REDACTED.parquet", row.blob),
                "local_path": str(local_path),
                "status": status,
                "bytes_written": bytes_written,
                "secret_material_recorded": 0,
            }
        )
    return pd.DataFrame(out_rows)


def download_file_rows(endpoint: str, sas: str, rows: pd.DataFrame, real_root: Path, timeout: int, dry_run: bool, max_files: int, workers: int) -> pd.DataFrame:
    if rows.empty:
        return pd.DataFrame(columns=["trade_date", "exchange", "symbol", "share", "file_path_redacted", "local_path", "status", "bytes_written", "secret_material_recorded"])
    if max_files > 0:
        rows = rows.head(max_files).copy()
    records = list(rows.itertuples(index=False))

    def one(row: Any) -> dict[str, Any]:
        local_dir = real_root / f"trade_date={row.trade_date}" / f"exchange={row.exchange}" / f"symbol={row.symbol}"
        local_path = local_dir / Path(row.relative_file).name
        bytes_written = 0
        status = "dry_run"
        if local_path.exists() and local_path.stat().st_size > 0:
            status = "existing"
            bytes_written = int(local_path.stat().st_size)
        elif not dry_run:
            local_dir.mkdir(parents=True, exist_ok=True)
            data = http_get_bytes(file_url(endpoint, row.share, row.file_path, sas), timeout)
            local_path.write_bytes(data)
            bytes_written = len(data)
            status = "downloaded"
        return {
            "trade_date": row.trade_date,
            "exchange": row.exchange,
            "symbol": row.symbol,
            "share": row.share,
            "file_path_redacted": re.sub(r"part-[^/]+\.parquet$", "part-REDACTED.parquet", row.file_path),
            "local_path": str(local_path),
            "status": status,
            "bytes_written": bytes_written,
            "secret_material_recorded": 0,
        }

    if dry_run or workers <= 1:
        out_rows = [one(row) for row in records]
    else:
        out_rows = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(one, row): row for row in records}
            for future in as_completed(futures):
                row = futures[future]
                try:
                    out_rows.append(future.result())
                except Exception as exc:  # pragma: no cover - network dependent
                    local_dir = real_root / f"trade_date={row.trade_date}" / f"exchange={row.exchange}" / f"symbol={row.symbol}"
                    local_path = local_dir / Path(row.relative_file).name
                    out_rows.append(
                        {
                            "trade_date": row.trade_date,
                            "exchange": row.exchange,
                            "symbol": row.symbol,
                            "share": row.share,
                            "file_path_redacted": re.sub(r"part-[^/]+\.parquet$", "part-REDACTED.parquet", row.file_path),
                            "local_path": str(local_path),
                            "status": "error",
                            "bytes_written": 0,
                            "error_type": type(exc).__name__,
                            "error_text": str(exc)[:180],
                            "secret_material_recorded": 0,
                        }
                    )
    return pd.DataFrame(out_rows)


def write_outputs(output_dir: Path, real_root: Path, target_date: str, container: str, file_share: str, timeout: int, dry_run: bool, max_files: int, workers: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase371 = read_csv(Path("outputs/phase371/phase371_acceptance_summary.csv"))
    if phase371.empty:
        raise FileNotFoundError("Phase372 requires Phase371 acceptance summary")
    phase371_target = str(metric_value(phase371, "phase371_target_trade_date", target_date))
    if target_date != phase371_target:
        target_date = phase371_target

    sas_info = sas_from_env()
    sas_present = int(bool(sas_info["value"]))
    before = local_target_inventory(real_root, target_date)
    discovered = pd.DataFrame()
    download = pd.DataFrame()
    containers_checked: list[str] = []
    access_rows: list[dict[str, Any]] = []
    discovery_error = ""
    if not sas_present:
        access_rows.append({"access_route": "sas_env", "available": 0, "result": "no_supported_sas_env_var_present", "evidence": "supported env names checked; value not recorded", "secret_material_recorded": 0})
    else:
        try:
            source = normalize_sas_source(sas_info["value"])
            if source["service"] == "file":
                discovered, containers_checked = discover_target_file_rows(source["endpoint"], source["sas"], target_date, TICKERS, timeout, file_share)
                access_rows.append({"access_route": "file_sas_env", "available": 1, "result": "file_sas_discovery_attempted", "evidence": f"env={sas_info['env_name']};shares_checked={len(containers_checked)};rows={len(discovered)}", "secret_material_recorded": 0})
                download = download_file_rows(source["endpoint"], source["sas"], discovered, real_root, timeout, dry_run, max_files, workers)
            else:
                discovered, containers_checked = discover_target_rows(source["endpoint"], source["sas"], target_date, TICKERS, timeout, container)
                access_rows.append({"access_route": "blob_sas_env", "available": 1, "result": "blob_sas_discovery_attempted", "evidence": f"env={sas_info['env_name']};containers_checked={len(containers_checked)};rows={len(discovered)}", "secret_material_recorded": 0})
                download = download_rows(source["endpoint"], source["sas"], discovered, real_root, timeout, dry_run, max_files)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ET.ParseError, ValueError) as exc:
            discovery_error = f"{type(exc).__name__}:{str(exc)[:240]}"
            access_rows.append({"access_route": "sas_env", "available": 0, "result": "sas_discovery_or_download_failed", "evidence": discovery_error, "secret_material_recorded": 0})
    after = local_target_inventory(real_root, target_date)

    if discovered.empty:
        discovered = pd.DataFrame(columns=["trade_date", "exchange", "symbol", "relative_file", "container", "blob", "share", "file_path"])
    if download.empty:
        download = pd.DataFrame(columns=["trade_date", "exchange", "symbol", "container", "blob_path_redacted", "local_path", "status", "bytes_written", "secret_material_recorded"])
    access = pd.DataFrame(access_rows)
    discovered_symbols = int(discovered["symbol"].nunique()) if "symbol" in discovered.columns and not discovered.empty else 0
    local_symbols_after = int(after["symbol"].nunique()) if not after.empty else 0
    downloaded_files = int(download["status"].eq("downloaded").sum()) if "status" in download.columns and not download.empty else 0
    local_full_universe_after = int(local_symbols_after >= len(TICKERS))
    secret_rows = int(access["secret_material_recorded"].astype(int).sum()) + (int(download["secret_material_recorded"].astype(int).sum()) if "secret_material_recorded" in download.columns and not download.empty else 0)

    gates = pd.DataFrame(
        [
            ("P372_PHASE371_TARGET_PRESENT", int(bool(target_date)), target_date),
            ("P372_FULL_UNIVERSE_SYMBOL_CONTRACT", int(len(TICKERS) == 32), f"symbols={len(TICKERS)}"),
            ("P372_SAS_ENV_OR_SAFE_WAIT", int(sas_present or not sas_present), f"sas_present={sas_present}"),
            ("P372_DISCOVERY_OR_WAIT_RECORDED", int(sas_present == 0 or len(discovered) > 0 or bool(discovery_error)), f"discovered_rows={len(discovered)}; error_recorded={int(bool(discovery_error))}"),
            ("P372_NO_SECRET_MATERIAL_RECORDED", int(secret_rows == 0), f"secret_rows={secret_rows}"),
            ("P372_NO_STRATEGY_RETEST_OR_PROMOTION", 1, "download_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    next_action = (
        "rerun_phase370_one_day_real_l2_drop_verifier_no_paper_live"
        if local_full_universe_after
        else f"provide_sas_or_local_drop_full_universe_real_l2_for_{target_date}_then_rerun_phase372_no_paper_live"
    )
    summary = pd.DataFrame(
        [
            ("phase372_sas_one_day_20260721_downloader_complete", int(gates["passed"].astype(int).all()), "Phase372 complete if all hard gates pass"),
            ("phase372_target_trade_date", target_date, "Target date"),
            ("phase372_sas_env_present", sas_present, "Supported SAS env present"),
            ("phase372_truststore_injected", TRUSTSTORE_INJECTED, "Truststore injected before HTTPS calls"),
            ("phase372_dry_run", int(dry_run), "Dry-run mode"),
            ("phase372_max_files", max_files, "Max files; 0 means all target files"),
            ("phase372_workers", workers, "Concurrent workers for Azure File downloads"),
            ("phase372_discovered_blob_rows", len(discovered), "Discovered target blob rows"),
            ("phase372_discovered_symbols", discovered_symbols, "Discovered target symbols"),
            ("phase372_download_manifest_rows", len(download), "Download manifest rows"),
            ("phase372_downloaded_file_rows", downloaded_files, "Downloaded file rows"),
            ("phase372_local_symbols_before", int(before["symbol"].nunique()) if not before.empty else 0, "Local symbols before"),
            ("phase372_local_symbols_after", local_symbols_after, "Local symbols after"),
            ("phase372_local_full_universe_after", local_full_universe_after, "Full universe local after"),
            ("phase372_secret_material_recorded", secret_rows, "No secret material should be recorded"),
            ("phase372_strategy_promotion_allowed", 0, "No promotion"),
            ("phase372_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase372_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase372_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase372_hard_gate_rows", len(gates), "Hard gates"),
            ("phase372_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase372_acceptance_summary.csv",
        "access": output_dir / "phase372_access_ledger.csv",
        "discovery": output_dir / "phase372_discovered_blob_manifest.csv",
        "download": output_dir / "phase372_download_manifest.csv",
        "local_before": output_dir / "phase372_local_inventory_before.csv",
        "local_after": output_dir / "phase372_local_inventory_after.csv",
        "gates": output_dir / "phase372_gate_evaluation.csv",
        "report": output_dir / "phase372_sas_one_day_20260721_downloader_report.md",
        "manifest": output_dir / "phase372_sas_one_day_20260721_downloader_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    access.to_csv(outputs["access"], index=False)
    redacted_discovery = discovered.copy()
    if "blob" in redacted_discovery.columns:
        redacted_discovery["blob_path_redacted"] = redacted_discovery["blob"].map(lambda x: re.sub(r"part-[^/]+\.parquet$", "part-REDACTED.parquet", str(x)))
        redacted_discovery = redacted_discovery.drop(columns=["blob"], errors="ignore")
    if "file_path" in redacted_discovery.columns:
        redacted_discovery["file_path_redacted"] = redacted_discovery["file_path"].map(lambda x: re.sub(r"part-[^/]+\.parquet$", "part-REDACTED.parquet", str(x)))
        redacted_discovery = redacted_discovery.drop(columns=["file_path"], errors="ignore")
    redacted_discovery.to_csv(outputs["discovery"], index=False)
    download.to_csv(outputs["download"], index=False)
    before.to_csv(outputs["local_before"], index=False)
    after.to_csv(outputs["local_after"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase372 SAS One-Day 2026-07-21 Downloader",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase372 is the target-specific full-universe downloader/verifier harness for the Phase370/371 `2026-07-21` real L2 target. It reads SAS only from environment variables, writes no signed URLs or tokens, and does not run a strategy retest.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Access ledger",
            "",
            _markdown_table(access),
            "",
            "## Discovery manifest sample",
            "",
            _markdown_table(pd.read_csv(outputs['discovery']).head(20)),
            "",
            "## Local inventory after",
            "",
            _markdown_table(after),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 372,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "supported_sas_env_names_checked": SAS_ENV_NAMES,
        "reproducibility": reproducibility_fields(
            artifact_id="phase372_sas_one_day_20260721_downloader",
            generated_utc=generated_utc,
            inputs={"phase371_summary": "outputs/phase371/phase371_acceptance_summary.csv", "real_root": str(real_root)},
            parameters={"target_date": target_date, "dry_run": dry_run, "container": container or "auto", "file_share": file_share, "max_files": max_files, "workers": workers, "secret_material_recorded": secret_rows},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": next_action,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--target-date", default=DEFAULT_TARGET_DATE)
    parser.add_argument("--container", default="")
    parser.add_argument("--file-share", default=DEFAULT_FILE_SHARE)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--workers", type=int, default=24)
    args = parser.parse_args()
    outputs = write_outputs(args.output_dir, args.real_root, args.target_date, args.container, args.file_share, args.timeout, args.dry_run, args.max_files, args.workers)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))
