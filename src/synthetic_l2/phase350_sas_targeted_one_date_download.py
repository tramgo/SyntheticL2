from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE349_DIR = Path("outputs/phase349")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase350")
DEFAULT_ACCOUNT = "stctrade1ramic"

SAS_ENV_NAMES = [
    "AZURE_BLOB_SERVICE_SAS_URL",
    "STCTRADE1RAMIC_BLOB_SAS_URL",
    "AZURE_STORAGE_SAS_TOKEN",
    "STCTRADE1RAMIC_SAS_TOKEN",
]

NEXT_ACTION_DOWNLOADED = "run_phase351_verify_join_and_rerun_candidate_grid_no_paper_live"
NEXT_ACTION_WAITING = "set_fresh_blob_sas_env_or_local_drop_then_rerun_phase350_no_paper_live"


def local_real_l2_dates(real_root: Path) -> list[str]:
    if not real_root.exists():
        return []
    return sorted(
        p.name.split("=", 1)[1]
        for p in real_root.iterdir()
        if p.is_dir() and p.name.startswith("trade_date=")
    )


def parse_contract_symbols(phase349_dir: Path) -> list[str]:
    contract = pd.read_csv(phase349_dir / "phase349_phase350_targeted_download_contract.csv")
    value = str(contract.set_index("contract_id").loc["target_symbols", "contract_value"])
    return [s.strip() for s in value.split(";") if s.strip()]


def sas_from_env() -> dict[str, str]:
    for name in SAS_ENV_NAMES:
        value = os.environ.get(name, "").strip()
        if value:
            return {"env_name": name, "value": value}
    return {"env_name": "", "value": ""}


def normalize_sas_source(raw: str) -> dict[str, str]:
    if raw.startswith("https://"):
        parsed = urllib.parse.urlparse(raw)
        endpoint = f"{parsed.scheme}://{parsed.netloc}"
        sas = parsed.query
        return {"endpoint": endpoint, "sas": sas.lstrip("?")}
    return {"endpoint": f"https://{DEFAULT_ACCOUNT}.blob.core.windows.net", "sas": raw.lstrip("?")}


def signed_url(endpoint: str, path: str, sas: str, params: dict[str, str] | None = None) -> str:
    params = dict(params or {})
    query = urllib.parse.urlencode(params)
    if query:
        query = f"{query}&{sas}"
    else:
        query = sas
    return f"{endpoint.rstrip('/')}/{path.lstrip('/')}?{query}"


def service_url(endpoint: str, sas: str, params: dict[str, str]) -> str:
    query = urllib.parse.urlencode(params)
    return f"{endpoint.rstrip('/')}/?{query}&{sas}"


def http_get_bytes(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "SyntheticL2Phase350/1.0"})
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


def parse_raw_l2_blob(blob: str) -> dict[str, str] | None:
    match = re.search(r"raw_l2/trade_date=([^/]+)/exchange=([^/]+)/symbol=([^/]+)/(.+\.parquet)$", blob)
    if not match:
        return None
    return {
        "trade_date": match.group(1),
        "exchange": match.group(2),
        "symbol": match.group(3),
        "relative_file": match.group(4),
    }


def discover_target(endpoint: str, sas: str, symbols: list[str], existing_dates: list[str], timeout: int, explicit_container: str = "") -> tuple[str, list[dict[str, str]], list[str]]:
    containers = [explicit_container] if explicit_container else list_containers(endpoint, sas, timeout)
    candidates: list[dict[str, str]] = []
    for container in containers:
        if not container:
            continue
        blobs = list_blobs(endpoint, container, sas, "raw_l2/", timeout)
        symbol_set = set(symbols)
        for blob in blobs:
            parsed = parse_raw_l2_blob(blob)
            if parsed and parsed["symbol"] in symbol_set and parsed["exchange"] == "NSE" and parsed["trade_date"] not in existing_dates:
                parsed["container"] = container
                parsed["blob"] = blob
                candidates.append(parsed)
        if candidates:
            break
    if not candidates:
        return "", [], containers
    dates = sorted({row["trade_date"] for row in candidates})
    target_date = dates[0]
    target_rows = [row for row in candidates if row["trade_date"] == target_date]
    return target_date, target_rows, containers


def download_rows(endpoint: str, sas: str, rows: list[dict[str, str]], real_root: Path, timeout: int, dry_run: bool) -> pd.DataFrame:
    out_rows = []
    for row in rows:
        local_dir = real_root / f"trade_date={row['trade_date']}" / f"exchange={row['exchange']}" / f"symbol={row['symbol']}"
        local_path = local_dir / Path(row["relative_file"]).name
        status = "dry_run"
        bytes_written = 0
        if not dry_run:
            local_dir.mkdir(parents=True, exist_ok=True)
            data = http_get_bytes(signed_url(endpoint, f"{row['container']}/{row['blob']}", sas), timeout)
            local_path.write_bytes(data)
            bytes_written = len(data)
            status = "downloaded"
        out_rows.append(
            {
                "trade_date": row["trade_date"],
                "exchange": row["exchange"],
                "symbol": row["symbol"],
                "container": row["container"],
                "blob_path_redacted": re.sub(r"part-[^/]+\.parquet$", "part-REDACTED.parquet", row["blob"]),
                "local_path": str(local_path),
                "status": status,
                "bytes_written": bytes_written,
                "secret_material_recorded": 0,
            }
        )
    return pd.DataFrame(out_rows)


def write_outputs(phase349_dir: Path, real_root: Path, output_dir: Path, timeout: int, dry_run: bool, local_only_verify: bool, container: str) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase349 = read_csv(phase349_dir / "phase349_acceptance_summary.csv")
    symbols = parse_contract_symbols(phase349_dir)
    existing_dates_before = local_real_l2_dates(real_root)
    sas_info = sas_from_env()
    sas_present = bool(sas_info["value"])
    download = pd.DataFrame()
    access_rows = []
    target_date = ""
    discovered_containers: list[str] = []
    if local_only_verify:
        access_rows.append(("local_only_verify", 1, "manual local drop verification mode", 0))
    elif not sas_present:
        access_rows.append(("sas_env", 0, "no supported SAS env var present", 0))
    else:
        try:
            source = normalize_sas_source(sas_info["value"])
            target_date, rows, discovered_containers = discover_target(source["endpoint"], source["sas"], symbols, existing_dates_before, timeout, explicit_container=container)
            access_rows.append(("sas_env", 1, f"env={sas_info['env_name']};containers_checked={len(discovered_containers)};target_date_found={int(bool(target_date))}", 0))
            if rows:
                download = download_rows(source["endpoint"], source["sas"], rows, real_root, timeout, dry_run=dry_run)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ET.ParseError, ValueError) as exc:
            access_rows.append(("sas_env", 0, f"{type(exc).__name__}:{str(exc)[:220]}", 0))
    existing_dates_after = local_real_l2_dates(real_root)
    new_dates = sorted(set(existing_dates_after) - set(existing_dates_before))
    downloaded_rows = int(len(download[download["status"].eq("downloaded")])) if not download.empty else 0
    access = pd.DataFrame(access_rows, columns=["access_route", "available", "evidence", "secret_material_recorded"])
    if download.empty:
        download = pd.DataFrame(
            columns=["trade_date", "exchange", "symbol", "container", "blob_path_redacted", "local_path", "status", "bytes_written", "secret_material_recorded"]
        )
    gates = pd.DataFrame(
        [
            ("P350_PHASE349_COMPLETE", as_int(metric_value(phase349, "phase349_storage_access_repair_or_sas_targeted_download_precommit_complete", 0)) == 1, metric_value(phase349, "phase349_storage_access_repair_or_sas_targeted_download_precommit_complete", 0), 1),
            ("P350_SECRET_INPUT_NOT_PERSISTED", True, "not_recorded", "not_recorded"),
            ("P350_SAS_OR_LOCAL_VERIFY_ROUTE_AVAILABLE", sas_present or local_only_verify, int(sas_present or local_only_verify), 1),
            ("P350_TARGET_DATE_DISCOVERED_OR_LOCAL_VERIFY", bool(target_date) or local_only_verify, target_date or "local_only_verify" if local_only_verify else "", "target_date"),
            ("P350_DOWNLOAD_EXECUTED_OR_SAFE_WAIT", downloaded_rows > 0 or not sas_present or dry_run or local_only_verify, f"downloaded_rows={downloaded_rows};dry_run={int(dry_run)};sas_present={int(sas_present)}", "safe"),
            ("P350_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
        ],
        columns=["gate_id", "passed", "observed", "required"],
    )
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    summary = pd.DataFrame(
        [
            ("phase350_sas_targeted_one_date_download_attempted", 1, "Phase350 attempted"),
            ("phase350_phase349_complete", as_int(metric_value(phase349, "phase349_storage_access_repair_or_sas_targeted_download_precommit_complete", 0)), "Phase349 complete"),
            ("phase350_sas_env_present", int(sas_present), "Supported SAS env var present"),
            ("phase350_local_only_verify", int(local_only_verify), "Local-only verify mode"),
            ("phase350_dry_run", int(dry_run), "Dry-run mode"),
            ("phase350_candidate_symbol_rows", len(symbols), "Candidate symbol rows"),
            ("phase350_existing_local_dates_before", len(existing_dates_before), "Local real L2 dates before"),
            ("phase350_target_trade_date", target_date, "Selected target trade date"),
            ("phase350_download_manifest_rows", len(download), "Download manifest rows"),
            ("phase350_downloaded_file_rows", downloaded_rows, "Downloaded file rows"),
            ("phase350_new_real_l2_dates_added", len(new_dates), "New local real L2 dates added"),
            ("phase350_secret_material_recorded", 0, "No secret material recorded"),
            ("phase350_strategy_promotion_allowed", 0, "No promotion"),
            ("phase350_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase350_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase350_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase350_hard_gate_rows", total, "Hard gates"),
            ("phase350_next_best_action", NEXT_ACTION_DOWNLOADED if downloaded_rows > 0 or len(new_dates) > 0 else NEXT_ACTION_WAITING, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase350 SAS Targeted One-Date Download",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase350 safely attempts a one-date targeted official-catalyst L2 download. SAS values and signed URLs are never written to outputs.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Access ledger",
            "",
            _markdown_table(access),
            "",
            "## Download manifest",
            "",
            _markdown_table(download.head(50)),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
        ]
    )
    outputs = {
        "summary": output_dir / "phase350_acceptance_summary.csv",
        "access": output_dir / "phase350_access_ledger.csv",
        "download": output_dir / "phase350_download_manifest.csv",
        "gates": output_dir / "phase350_gate_evaluation.csv",
        "report": output_dir / "phase350_sas_targeted_one_date_download_report.md",
        "manifest": output_dir / "phase350_sas_targeted_one_date_download_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    access.to_csv(outputs["access"], index=False)
    download.to_csv(outputs["download"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 350,
        "generated_at_utc": generated_utc,
        "phase349_dir": str(phase349_dir),
        "real_root": str(real_root),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase350_sas_targeted_one_date_download",
            generated_utc=generated_utc,
            inputs={"phase349_dir": str(phase349_dir), "real_root": str(real_root)},
            parameters={"dry_run": dry_run, "local_only_verify": local_only_verify, "container": container or "auto"},
            outputs={key: str(value) for key, value in outputs.items()},
        ),
        "next_action": str(summary[summary["metric"].eq("phase350_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase349-dir", type=Path, default=DEFAULT_PHASE349_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--local-only-verify", action="store_true")
    parser.add_argument("--container", default="")
    args = parser.parse_args()
    outputs = write_outputs(args.phase349_dir, args.real_root, args.output_dir, args.timeout, args.dry_run, args.local_only_verify, args.container)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
