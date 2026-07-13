from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Mapping


REPRODUCIBILITY_SCHEMA_NAME = "synthetic_l2_reproducibility_manifest_v1"

DEFAULT_CALIBRATION_DATASET_ID = "zerodha_l2_single_day_seed_and_current_synthetic_outputs"
DEFAULT_TICKER_METADATA_VERSION = "nse_32_symbol_universe_current_plan"
DEFAULT_REGIME_CALENDAR_VERSION = "outputs/phase4/scenario_calendar.csv_or_not_applicable"
DEFAULT_SCENARIO_IDS = "current_phase_outputs_all_available_scenarios_or_not_applicable"


def git_generator_version(base_dir: Path = Path(".")) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=base_dir, text=True).strip()
    except Exception:
        return "git_sha_unavailable"


def stable_configuration_hash(
    *,
    artifact_id: str,
    inputs: Mapping[str, Any] | None = None,
    parameters: Mapping[str, Any] | None = None,
    outputs: Mapping[str, Any] | None = None,
) -> str:
    payload = {
        "artifact_id": artifact_id,
        "inputs": dict(inputs or {}),
        "parameters": dict(parameters or {}),
        "outputs": dict(outputs or {}),
    }
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def reproducibility_fields(
    *,
    artifact_id: str,
    generated_utc: str,
    inputs: Mapping[str, Any] | None = None,
    parameters: Mapping[str, Any] | None = None,
    outputs: Mapping[str, Any] | None = None,
    random_seed: Any = "not_applicable_deterministic",
    calibration_dataset_id: str = DEFAULT_CALIBRATION_DATASET_ID,
    ticker_metadata_version: str = DEFAULT_TICKER_METADATA_VERSION,
    regime_calendar_version: str = DEFAULT_REGIME_CALENDAR_VERSION,
    scenario_ids: Any = DEFAULT_SCENARIO_IDS,
    cost_model_version: str = "not_applicable_no_execution_costs",
    latency_model_version: str = "not_applicable_no_latency_model",
    base_dir: Path = Path("."),
) -> dict[str, Any]:
    return {
        "reproducibility_schema_name": REPRODUCIBILITY_SCHEMA_NAME,
        "generator_version": git_generator_version(base_dir),
        "configuration_hash": stable_configuration_hash(
            artifact_id=artifact_id,
            inputs=inputs,
            parameters=parameters,
            outputs=outputs,
        ),
        "random_seed": random_seed,
        "calibration_dataset_id": calibration_dataset_id,
        "ticker_metadata_version": ticker_metadata_version,
        "regime_calendar_version": regime_calendar_version,
        "scenario_ids": scenario_ids,
        "cost_model_version": cost_model_version,
        "latency_model_version": latency_model_version,
        "creation_timestamp": generated_utc,
    }
