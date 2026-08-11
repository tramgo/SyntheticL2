from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase149")
DEFAULT_OUTPUTS_ROOT = Path("outputs")
DEFAULT_SCRIPTS_ROOT = Path("scripts")
DEFAULT_PLAN_PATH = Path("Plan/zerodha_l2_synthetic_data_strategy_validation_plan.md")


PHASE_RE = re.compile(r"phase(\d+)", re.IGNORECASE)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def discover_script_phases(scripts_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path in sorted(scripts_root.glob("run_phase*.*")):
        match = PHASE_RE.search(path.name)
        if not match:
            continue
        rows.append(
            {
                "phase": int(match.group(1)),
                "runner": str(path),
                "runner_exists": True,
                "runner_suffix": path.suffix.lower(),
            }
        )
    return pd.DataFrame(rows)


def discover_output_phases(outputs_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not outputs_root.exists():
        return pd.DataFrame(columns=["phase", "output_dir", "output_exists", "file_count", "acceptance_files", "manifest_files"])
    for directory in sorted(path for path in outputs_root.iterdir() if path.is_dir()):
        match = PHASE_RE.search(directory.name)
        if not match:
            continue
        files = sorted(path for path in directory.rglob("*") if path.is_file())
        acceptance = [path for path in files if "acceptance_summary" in path.name]
        manifests = [path for path in files if path.name.endswith("_manifest.json") or path.name.endswith("manifest.json")]
        rows.append(
            {
                "phase": int(match.group(1)),
                "output_dir": str(directory),
                "output_exists": True,
                "file_count": int(len(files)),
                "acceptance_files": "|".join(str(path) for path in acceptance),
                "manifest_files": "|".join(str(path) for path in manifests),
                "is_smoke_or_partial": bool("smoke" in directory.name.lower() or "partial" in directory.name.lower()),
            }
        )
    return pd.DataFrame(rows)


def phase_status_from_metrics(phase: int) -> dict[str, Any]:
    paths = {
        52: Path("outputs/phase52/dense_replay_acceptance_summary_partial.csv"),
        96: Path("outputs/phase115/subruns/phase96/real_anchor_panel_builder_acceptance_summary.csv"),
        110: Path("outputs/phase115/subruns/phase110/phase110_multiday_replay_unlock_acceptance_summary.csv"),
        115: Path("outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv"),
        132: Path("outputs/phase132/phase132_deep_book_feature_diagnostics_acceptance_summary.csv"),
        133: Path("outputs/phase133/phase133_passive_execution_model_upgrade_acceptance_summary.csv"),
        136: Path("outputs/phase136/phase136_deep_book_verdict_acceptance_summary.csv"),
        142: Path("outputs/phase142/phase142_local_real_l2_download_verifier_acceptance_summary.csv"),
        143: Path("outputs/phase143/phase143_real_l2_two_date_preflight_acceptance_summary.csv"),
        145: Path("outputs/phase145/phase145_real_l2_post_download_refresh_acceptance_summary.csv"),
        146: Path("outputs/phase146/phase146_real_anchor_minimum_unlock_audit_acceptance_summary.csv"),
        147: Path("outputs/phase147/phase147_azcopy_download_intake_audit_acceptance_summary.csv"),
        148: Path("outputs/phase148/phase148_real_l2_download_refresh_workflow_acceptance_summary.csv"),
        171: Path("outputs/phase171/phase171_external_orderflow_source_acceptance_summary.csv"),
        172: Path("outputs/phase172/phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
        173: Path("outputs/phase173/phase173_real_l2_download_credential_preflight_acceptance_summary.csv"),
        174: Path("outputs/phase174/phase174_secure_real_l2_download_orchestrator_acceptance_summary.csv"),
        175: Path("outputs/phase175/phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv"),
        176: Path("outputs/phase176/phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
        177: Path("outputs/phase177/phase177_receive_flow_feature_quality_audit_acceptance_summary.csv"),
        178: Path("outputs/phase178/phase178_receive_flow_feature_handoff_precommit_acceptance_summary.csv"),
        179: Path("outputs/phase179/phase179_strategy_family_precommit_acceptance_summary.csv"),
        180: Path("outputs/phase180/phase180_cost_latency_label_precommit_acceptance_summary.csv"),
        181: Path("outputs/phase181/phase181_label_materialization_acceptance_summary.csv"),
        182: Path("outputs/phase182/phase182_label_quality_leakage_audit_acceptance_summary.csv"),
        183: Path("outputs/phase183/phase183_replay_readiness_precommit_acceptance_summary.csv"),
        184: Path("outputs/phase184/phase184_train_validation_replay_dry_run_acceptance_summary.csv"),
        185: Path("outputs/phase185/phase185_validation_replay_interpretation_acceptance_summary.csv"),
        186: Path("outputs/phase186/phase186_cost_aware_family_closure_acceptance_summary.csv"),
        187: Path("outputs/phase187/phase187_cost_aware_sparse_candidate_acceptance_summary.csv"),
        188: Path("outputs/phase188/phase188_sparse_candidate_interpretation_acceptance_summary.csv"),
        189: Path("outputs/phase189/phase189_test_replay_precommit_decision_acceptance_summary.csv"),
        190: Path("outputs/phase190/phase190_validation_breadth_or_diagnostic_test_spec_acceptance_summary.csv"),
        191: Path("outputs/phase191/phase191_diagnostic_test_replay_precommit_acceptance_summary.csv"),
        192: Path("outputs/phase192/phase192_real_validation_date_download_acceptance_summary.csv"),
        193: Path("outputs/phase193/phase193_validation_breadth_extension_acceptance_summary.csv"),
        194: Path("outputs/phase194/phase194_sparse_candidate_fragility_acceptance_summary.csv"),
        195: Path("outputs/phase195/phase195_receive_flow_redesign_candidate_acceptance_summary.csv"),
        196: Path("outputs/phase196/phase196_expanded_feature_model_acceptance_summary.csv"),
        197: Path("outputs/phase197/phase197_non_receive_flow_feature_acceptance_summary.csv"),
        198: Path("outputs/phase198/phase198_context_model_acceptance_summary.csv"),
        199: Path("outputs/phase199/phase199_branch_decision_acceptance_summary.csv"),
        200: Path("outputs/phase200/phase200_material_new_hypothesis_acceptance_summary.csv"),
        201: Path("outputs/phase201/phase201_stage01_acceptance_summary.csv"),
        202: Path("outputs/phase202/phase202_passive_feature_redesign_acceptance_summary.csv"),
        203: Path("outputs/phase203/phase203_redesigned_passive_label_acceptance_summary.csv"),
        204: Path("outputs/phase204/phase204_passive_redesign_closure_acceptance_summary.csv"),
        205: Path("outputs/phase205/phase205_material_new_source_acceptance_summary.csv"),
        206: Path("outputs/phase206/phase206_nonoverlap_feature_acceptance_summary.csv"),
        207: Path("outputs/phase207/phase207_feature_matrix_acceptance_summary.csv"),
        208: Path("outputs/phase208/phase208_feature_matrix_quality_acceptance_summary.csv"),
        209: Path("outputs/phase209/phase209_model_fit_precommit_acceptance_summary.csv"),
        210: Path("outputs/phase210/phase210_train_validation_model_fit_acceptance_summary.csv"),
        211: Path("outputs/phase211/phase211_model_fit_validation_interpretation_acceptance_summary.csv"),
        212: Path("outputs/phase212/phase212_model_family_closure_acceptance_summary.csv"),
        213: Path("outputs/phase213/phase213_material_new_source_acceptance_summary.csv"),
        214: Path("outputs/phase214/phase214_event_surprise_label_acceptance_summary.csv"),
        215: Path("outputs/phase215/phase215_label_quality_interpretation_acceptance_summary.csv"),
        216: Path("outputs/phase216/phase216_event_only_target_acceptance_summary.csv"),
        217: Path("outputs/phase217/phase217_design_matrix_acceptance_summary.csv"),
        218: Path("outputs/phase218/phase218_model_fit_precommit_acceptance_summary.csv"),
        219: Path("outputs/phase219/phase219_model_fit_acceptance_summary.csv"),
        220: Path("outputs/phase220/phase220_validation_interpretation_acceptance_summary.csv"),
        221: Path("outputs/phase221/phase221_signal_replay_precommit_acceptance_summary.csv"),
        222: Path("outputs/phase222/phase222_signal_replay_acceptance_summary.csv"),
        223: Path("outputs/phase223/phase223_validation_interpretation_acceptance_summary.csv"),
        224: Path("outputs/phase224/phase224_closure_or_redesign_acceptance_summary.csv"),
        225: Path("outputs/phase225/phase225_redesign_precommit_acceptance_summary.csv"),
        226: Path("outputs/phase226/phase226_label_materialization_acceptance_summary.csv"),
        227: Path("outputs/phase227/phase227_quality_interpretation_acceptance_summary.csv"),
        228: Path("outputs/phase228/phase228_closure_or_relaxation_acceptance_summary.csv"),
        229: Path("outputs/phase229/phase229_strategy_search_acceptance_summary.csv"),
        230: Path("outputs/phase230/phase230_strategy_search_acceptance_summary.csv"),
        231: Path("outputs/phase231/phase231_acceptance_summary.csv"),
        232: Path("outputs/phase232/phase232_acceptance_summary.csv"),
        233: Path("outputs/phase233/phase233_acceptance_summary.csv"),
        234: Path("outputs/phase234/phase234_acceptance_summary.csv"),
        235: Path("outputs/phase235/phase235_acceptance_summary.csv"),
        236: Path("outputs/phase236/phase236_acceptance_summary.csv"),
        237: Path("outputs/phase237/phase237_acceptance_summary.csv"),
        238: Path("outputs/phase238/phase238_acceptance_summary.csv"),
        239: Path("outputs/phase239/phase239_acceptance_summary.csv"),
        240: Path("outputs/phase240/phase240_acceptance_summary.csv"),
        241: Path("outputs/phase241/phase241_acceptance_summary.csv"),
        242: Path("outputs/phase242/phase242_acceptance_summary.csv"),
        243: Path("outputs/phase243/phase243_acceptance_summary.csv"),
        244: Path("outputs/phase244/phase244_acceptance_summary.csv"),
        245: Path("outputs/phase245/phase245_acceptance_summary.csv"),
        246: Path("outputs/phase246/phase246_acceptance_summary.csv"),
        247: Path("outputs/phase247/phase247_acceptance_summary.csv"),
        248: Path("outputs/phase248/phase248_acceptance_summary.csv"),
        249: Path("outputs/phase249/phase249_acceptance_summary.csv"),
        250: Path("outputs/phase250/phase250_acceptance_summary.csv"),
        251: Path("outputs/phase251/phase251_acceptance_summary.csv"),
        252: Path("outputs/phase252/phase252_acceptance_summary.csv"),
        253: Path("outputs/phase253/phase253_acceptance_summary.csv"),
        254: Path("outputs/phase254/phase254_acceptance_summary.csv"),
        255: Path("outputs/phase255/phase255_acceptance_summary.csv"),
        256: Path("outputs/phase256/phase256_acceptance_summary.csv"),
        257: Path("outputs/phase257/phase257_acceptance_summary.csv"),
        258: Path("outputs/phase258/phase258_acceptance_summary.csv"),
        259: Path("outputs/phase259/phase259_acceptance_summary.csv"),
        260: Path("outputs/phase260/phase260_acceptance_summary.csv"),
        261: Path("outputs/phase261/phase261_acceptance_summary.csv"),
        262: Path("outputs/phase262/phase262_acceptance_summary.csv"),
        263: Path("outputs/phase263/phase263_acceptance_summary.csv"),
        264: Path("outputs/phase264/phase264_acceptance_summary.csv"),
        265: Path("outputs/phase265/phase265_acceptance_summary.csv"),
        266: Path("outputs/phase266/phase266_acceptance_summary.csv"),
        267: Path("outputs/phase267/phase267_acceptance_summary.csv"),
        268: Path("outputs/phase268/phase268_acceptance_summary.csv"),
        269: Path("outputs/phase269/phase269_acceptance_summary.csv"),
        270: Path("outputs/phase270/phase270_acceptance_summary.csv"),
        271: Path("outputs/phase271/phase271_acceptance_summary.csv"),
        272: Path("outputs/phase272/phase272_acceptance_summary.csv"),
        273: Path("outputs/phase273/phase273_acceptance_summary.csv"),
        274: Path("outputs/phase274/phase274_acceptance_summary.csv"),
        275: Path("outputs/phase275/phase275_acceptance_summary.csv"),
        276: Path("outputs/phase276/phase276_acceptance_summary.csv"),
        277: Path("outputs/phase277/phase277_acceptance_summary.csv"),
        278: Path("outputs/phase278/phase278_acceptance_summary.csv"),
        279: Path("outputs/phase279/phase279_acceptance_summary.csv"),
        280: Path("outputs/phase280/phase280_acceptance_summary.csv"),
        281: Path("outputs/phase281/phase281_acceptance_summary.csv"),
        282: Path("outputs/phase282/phase282_acceptance_summary.csv"),
        283: Path("outputs/phase283/phase283_acceptance_summary.csv"),
        284: Path("outputs/phase284/phase284_acceptance_summary.csv"),
        285: Path("outputs/phase285/phase285_acceptance_summary.csv"),
        286: Path("outputs/phase286/phase286_acceptance_summary.csv"),
        287: Path("outputs/phase287/phase287_acceptance_summary.csv"),
        288: Path("outputs/phase288/phase288_acceptance_summary.csv"),
        289: Path("outputs/phase289/phase289_acceptance_summary.csv"),
        290: Path("outputs/phase290/phase290_acceptance_summary.csv"),
        291: Path("outputs/phase291/phase291_acceptance_summary.csv"),
        292: Path("outputs/phase292/phase292_acceptance_summary.csv"),
        293: Path("outputs/phase293/phase293_acceptance_summary.csv"),
        294: Path("outputs/phase294/phase294_acceptance_summary.csv"),
        295: Path("outputs/phase295/phase295_acceptance_summary.csv"),
        296: Path("outputs/phase296/phase296_acceptance_summary.csv"),
        297: Path("outputs/phase297/phase297_acceptance_summary.csv"),
        298: Path("outputs/phase298/phase298_acceptance_summary.csv"),
        299: Path("outputs/phase299/phase299_acceptance_summary.csv"),
        300: Path("outputs/phase300/phase300_acceptance_summary.csv"),
        301: Path("outputs/phase301/phase301_acceptance_summary.csv"),
        302: Path("outputs/phase302/phase302_acceptance_summary.csv"),
        303: Path("outputs/phase303/phase303_acceptance_summary.csv"),
        304: Path("outputs/phase304/phase304_acceptance_summary.csv"),
        305: Path("outputs/phase305/phase305_acceptance_summary.csv"),
        306: Path("outputs/phase306/phase306_acceptance_summary.csv"),
        307: Path("outputs/phase307/phase307_acceptance_summary.csv"),
        308: Path("outputs/phase308/phase308_acceptance_summary.csv"),
        309: Path("outputs/phase309/phase309_acceptance_summary.csv"),
        310: Path("outputs/phase310/phase310_acceptance_summary.csv"),
        311: Path("outputs/phase311/phase311_acceptance_summary.csv"),
        312: Path("outputs/phase312/phase312_acceptance_summary.csv"),
        313: Path("outputs/phase313/phase313_acceptance_summary.csv"),
        314: Path("outputs/phase314/phase314_acceptance_summary.csv"),
        315: Path("outputs/phase315/phase315_acceptance_summary.csv"),
        316: Path("outputs/phase316/phase316_acceptance_summary.csv"),
        317: Path("outputs/phase317/phase317_acceptance_summary.csv"),
        318: Path("outputs/phase318/phase318_acceptance_summary.csv"),
        319: Path("outputs/phase319/phase319_acceptance_summary.csv"),
        320: Path("outputs/phase320/phase320_acceptance_summary.csv"),
        321: Path("outputs/phase321/phase321_acceptance_summary.csv"),
        322: Path("outputs/phase322/phase322_acceptance_summary.csv"),
        323: Path("outputs/phase323/phase323_acceptance_summary.csv"),
        324: Path("outputs/phase324/phase324_acceptance_summary.csv"),
        325: Path("outputs/phase325/phase325_acceptance_summary.csv"),
        326: Path("outputs/phase326/phase326_acceptance_summary.csv"),
        327: Path("outputs/phase327/phase327_acceptance_summary.csv"),
        328: Path("outputs/phase328/phase328_acceptance_summary.csv"),
        329: Path("outputs/phase329/phase329_acceptance_summary.csv"),
        330: Path("outputs/phase330/phase330_acceptance_summary.csv"),
        331: Path("outputs/phase331/phase331_acceptance_summary.csv"),
        332: Path("outputs/phase332/phase332_acceptance_summary.csv"),
        333: Path("outputs/phase333/phase333_acceptance_summary.csv"),
        334: Path("outputs/phase334/phase334_acceptance_summary.csv"),
        335: Path("outputs/phase335/phase335_acceptance_summary.csv"),
        336: Path("outputs/phase336/phase336_acceptance_summary.csv"),
        337: Path("outputs/phase337/phase337_acceptance_summary.csv"),
    }
    path = paths.get(phase)
    if path is None or not path.exists():
        return {}
    if phase == 52:
        return {
            "branch": "dense_synthetic_replay",
            "state": "partial_or_smoke_artifacts_present",
            "strategy_replay_allowed": 0,
            "next_action": "do_not_promote_partial_dense_replay_without_acceptance_gate",
        }
    if phase == 132:
        return {
            "branch": "top_five_depth_passive",
            "state": "closed_kill_switch",
            "kill_switch_fired": as_int(metric_value(path, "phase132_kill_switch_fired", 0)),
            "surviving_feature_rows": as_int(metric_value(path, "phase132_surviving_feature_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase132_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase132_next_best_action", ""),
        }
    if phase == 133:
        return {
            "branch": "top_five_depth_passive",
            "state": "execution_contract_pinned_phase134_closed",
            "hard_gate_pass_rows": as_int(metric_value(path, "phase133_hard_gate_pass_rows", 0)),
            "phase134_open_allowed": as_int(metric_value(path, "phase133_phase134_open_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase133_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase133_next_best_action", ""),
        }
    if phase == 136:
        return {
            "branch": "top_five_depth_passive",
            "state": "closed_clean_falsification",
            "outcome": metric_value(path, "phase136_outcome", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase136_hard_gate_pass_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase136_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase136_next_best_action", ""),
        }
    if phase in {96, 110, 115, 142, 143, 145, 146, 147, 148}:
        ready_days = (
            metric_value(path, f"phase{phase}_ready_real_anchor_days", None)
            or metric_value(path, f"phase{phase}_phase115_ready_real_anchor_days", None)
            or metric_value(path, f"phase{phase}_phase110_ready_real_anchor_days", None)
            or metric_value(path, "phase110_ready_real_anchor_days", None)
            or metric_value(path, "phase96_ready_anchor_days", None)
        )
        days_needed = (
            metric_value(path, f"phase{phase}_days_needed_for_min", None)
            or metric_value(path, f"phase{phase}_phase146_days_needed_for_min", None)
            or metric_value(path, "phase110_days_needed_for_min", None)
        )
        strategy_allowed = (
            metric_value(path, f"phase{phase}_strategy_replay_allowed", None)
            or metric_value(path, f"phase{phase}_replay_unlock_allowed", None)
            or metric_value(path, "phase110_strategy_replay_allowed", None)
            or 0
        )
        return {
            "branch": "real_l2_anchor_gate",
            "state": "gated_waiting_for_more_real_anchor_days",
            "ready_real_anchor_days": as_int(ready_days, -1) if ready_days is not None else "",
            "days_needed_for_min": as_int(days_needed, -1) if days_needed is not None else "",
            "strategy_replay_allowed": as_int(strategy_allowed, 0),
            "next_action": metric_value(path, f"phase{phase}_next_best_action", ""),
        }
    if phase == 171:
        return {
            "branch": "real_receive_flow_source",
            "state": "source_contract_declared_no_replay",
            "selected_source_id": metric_value(path, "phase171_selected_source_id", ""),
            "source_contract_rows": as_int(metric_value(path, "phase171_source_contract_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase171_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase171_next_best_action", ""),
        }
    if phase == 172:
        return {
            "branch": "real_receive_flow_source",
            "state": "local_receive_flow_structural_ready_but_day_count_gated",
            "ready_receive_flow_dates": as_int(metric_value(path, "phase172_ready_receive_flow_dates", 0)),
            "additional_dates_needed": as_int(metric_value(path, "phase172_additional_dates_needed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase172_hard_gate_pass_rows", 0)),
            "unlock_gate_pass_rows": as_int(metric_value(path, "phase172_unlock_gate_pass_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase172_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase172_next_best_action", ""),
        }
    if phase == 173:
        download_ready = as_int(metric_value(path, "phase173_download_ready_now", 0))
        return {
            "branch": "real_receive_flow_download_gate",
            "state": "download_preflight_ready" if download_ready else "download_preflight_waiting_for_sas_or_key_or_tls_fix",
            "download_ready_now": download_ready,
            "additional_dates_needed": as_int(metric_value(path, "phase173_additional_dates_needed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase173_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase173_next_best_action", ""),
        }
    if phase == 174:
        download_ran = as_int(metric_value(path, "phase174_download_ran", 0))
        return {
            "branch": "real_receive_flow_download_gate",
            "state": "secure_download_executed" if download_ran else "secure_download_skipped_no_credential",
            "download_ran": download_ran,
            "additional_dates_needed": as_int(metric_value(path, "phase174_phase172_additional_dates_needed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase174_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase174_next_best_action", ""),
        }
    if phase == 175:
        activation_ready = as_int(metric_value(path, "phase175_activation_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_schema_activation_ready" if activation_ready else "receive_flow_feature_schema_precommitted_gated",
            "feature_schema_rows": as_int(metric_value(path, "phase175_feature_schema_rows", 0)),
            "activation_ready": activation_ready,
            "additional_dates_needed": as_int(metric_value(path, "phase175_additional_dates_needed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase175_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase175_next_best_action", ""),
        }
    if phase == 176:
        features_materialized = as_int(metric_value(path, "phase176_features_materialized", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_materializer_ready_gated" if features_materialized == 0 else "receive_flow_features_materialized_no_replay",
            "features_materialized": features_materialized,
            "activation_ready": as_int(metric_value(path, "phase176_activation_ready", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase176_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase176_next_best_action", ""),
        }
    if phase == 177:
        audit_ran = as_int(metric_value(path, "phase177_feature_quality_audit_ran", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_quality_audit_scaffold_gated" if audit_ran == 0 else "receive_flow_feature_quality_audited_no_replay",
            "feature_quality_audit_ran": audit_ran,
            "quality_check_rows": as_int(metric_value(path, "phase177_quality_check_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase177_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase177_next_best_action", ""),
        }
    if phase == 178:
        handoff_ready = as_int(metric_value(path, "phase178_handoff_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_handoff_precommitted_no_replay" if handoff_ready else "receive_flow_feature_handoff_gated",
            "handoff_ready": handoff_ready,
            "handoff_feature_rows": as_int(metric_value(path, "phase178_handoff_feature_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase178_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase178_next_best_action", ""),
        }
    if phase == 179:
        precommit_ready = as_int(metric_value(path, "phase179_precommit_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "strategy_family_precommitted_no_replay" if precommit_ready else "strategy_family_precommit_gated",
            "precommit_ready": precommit_ready,
            "strategy_family_rows": as_int(metric_value(path, "phase179_strategy_family_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase179_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase179_next_best_action", ""),
        }
    if phase == 180:
        precommit_ready = as_int(metric_value(path, "phase180_precommit_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_latency_label_precommitted_no_replay" if precommit_ready else "cost_latency_label_precommit_gated",
            "precommit_ready": precommit_ready,
            "label_family_rows": as_int(metric_value(path, "phase180_label_family_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase180_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase180_next_best_action", ""),
        }
    if phase == 181:
        labels_materialized = as_int(metric_value(path, "phase181_labels_materialized", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "labels_materialized_no_replay" if labels_materialized else "label_materialization_gated",
            "labels_materialized": labels_materialized,
            "label_rows": as_int(metric_value(path, "phase181_label_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase181_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase181_next_best_action", ""),
        }
    if phase == 182:
        audit_pass = as_int(metric_value(path, "phase182_label_quality_leakage_audit_pass", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "label_quality_leakage_audited_no_replay" if audit_pass else "label_quality_leakage_audit_gated",
            "label_quality_leakage_audit_pass": audit_pass,
            "partition_audit_rows": as_int(metric_value(path, "phase182_partition_audit_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase182_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase182_next_best_action", ""),
        }
    if phase == 183:
        readiness = as_int(metric_value(path, "phase183_replay_readiness_precommitted", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "replay_readiness_precommitted_no_pnl" if readiness else "replay_readiness_precommit_gated",
            "replay_readiness_precommitted": readiness,
            "strategy_replay_allowed": as_int(metric_value(path, "phase183_strategy_replay_allowed", 0)),
            "pnl_allowed": as_int(metric_value(path, "phase183_pnl_allowed", 0)),
            "next_action": metric_value(path, "phase183_next_best_action", ""),
        }
    if phase == 184:
        dry_run_complete = as_int(metric_value(path, "phase184_train_validation_dry_run_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "train_validation_replay_dry_run_complete_no_test_no_promotion" if dry_run_complete else "train_validation_replay_dry_run_gated",
            "train_validation_dry_run_complete": dry_run_complete,
            "strategy_replay_dry_run_performed": as_int(metric_value(path, "phase184_strategy_replay_dry_run_performed", 0)),
            "test_rows_used": as_int(metric_value(path, "phase184_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase184_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase184_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase184_next_best_action", ""),
        }
    if phase == 185:
        interpretation_complete = as_int(metric_value(path, "phase185_validation_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "validation_interpretation_cost_dominated_no_test_no_promotion" if interpretation_complete else "validation_interpretation_gated",
            "validation_interpretation_complete": interpretation_complete,
            "cost_dominates_validation_edge": as_int(metric_value(path, "phase185_cost_dominates_validation_edge", 0)),
            "test_rows_used": as_int(metric_value(path, "phase185_test_rows_used", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase185_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase185_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase185_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase185_next_best_action", ""),
        }
    if phase == 186:
        family_set_closed = as_int(metric_value(path, "phase186_current_family_set_closed", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "current_family_set_closed_cost_aware_redesign_pending" if family_set_closed else "family_closure_gated",
            "current_family_set_closed": family_set_closed,
            "reuse_without_redesign_allowed": as_int(metric_value(path, "phase186_reuse_without_redesign_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase186_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase186_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase186_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase186_next_best_action", ""),
        }
    if phase == 187:
        candidate_complete = as_int(metric_value(path, "phase187_cost_aware_sparse_candidate_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_aware_sparse_candidate_validation_interpretation_pending" if candidate_complete else "cost_aware_sparse_candidate_gated",
            "cost_aware_sparse_candidate_complete": candidate_complete,
            "validation_positive_all_profiles": as_int(metric_value(path, "phase187_validation_positive_all_profiles", 0)),
            "test_rows_used": as_int(metric_value(path, "phase187_test_rows_used", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase187_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase187_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase187_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase187_next_best_action", ""),
        }
    if phase == 188:
        interpretation_complete = as_int(metric_value(path, "phase188_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "sparse_candidate_interpreted_phase189_decision_pending" if interpretation_complete else "sparse_candidate_interpretation_gated",
            "sparse_candidate_interpretation_complete": interpretation_complete,
            "breadth_warning": as_int(metric_value(path, "phase188_breadth_warning", 0)),
            "date_count_warning": as_int(metric_value(path, "phase188_date_count_warning", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase188_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase188_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase188_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase188_next_best_action", ""),
        }
    if phase == 189:
        decision_complete = as_int(metric_value(path, "phase189_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "test_replay_deferred_validation_breadth_pending" if decision_complete else "test_replay_precommit_decision_gated",
            "test_precommit_decision_complete": decision_complete,
            "untouched_test_replay_precommit_allowed": as_int(metric_value(path, "phase189_untouched_test_replay_precommit_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase189_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase189_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase189_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase189_next_best_action", ""),
        }
    if phase == 190:
        decision_complete = as_int(metric_value(path, "phase190_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "diagnostic_test_spec_written_validation_breadth_pending" if decision_complete else "validation_breadth_or_diagnostic_spec_gated",
            "phase190_decision_complete": decision_complete,
            "additional_validation_breadth_available_now": as_int(metric_value(path, "phase190_additional_validation_breadth_available_now", 0)),
            "may_relabel_test_as_validation": as_int(metric_value(path, "phase190_may_relabel_test_as_validation", 0)),
            "test_replay_execution": as_int(metric_value(path, "phase190_test_replay_execution", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase190_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase190_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase190_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase190_next_best_action", ""),
        }
    if phase == 191:
        precommit_complete = as_int(metric_value(path, "phase191_diagnostic_test_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "diagnostic_test_replay_precommitted_no_execution" if precommit_complete else "diagnostic_test_replay_precommit_gated",
            "diagnostic_test_precommit_complete": precommit_complete,
            "test_replay_execution": as_int(metric_value(path, "phase191_test_replay_execution", 0)),
            "test_result_allowed": as_int(metric_value(path, "phase191_test_result_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase191_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase191_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase191_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase191_next_best_action", ""),
        }
    if phase == 192:
        failed = as_int(metric_value(path, "phase192_failed_files_or_dates", 0))
        downloaded = as_int(metric_value(path, "phase192_downloaded_files", 0))
        skipped = as_int(metric_value(path, "phase192_skipped_existing_files", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "real_validation_date_downloaded_no_test" if failed == 0 and (downloaded + skipped) > 0 else "real_validation_date_download_gated",
            "real_validation_download_complete": int(failed == 0 and (downloaded + skipped) > 0),
            "test_replay_execution": as_int(metric_value(path, "phase192_test_replay_execution", 0)),
            "test_result_allowed": as_int(metric_value(path, "phase192_test_result_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase192_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase192_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase192_next_best_action", ""),
        }
    if phase == 193:
        complete = as_int(metric_value(path, "phase193_validation_breadth_extension_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "validation_breadth_extended_mixed_negative_by_date_no_test" if complete else "validation_breadth_extension_gated",
            "validation_breadth_extension_complete": complete,
            "extension_validation_dates": metric_value(path, "phase193_extension_validation_dates", ""),
            "min_profile_net_bps_proxy_mean": metric_value(path, "phase193_min_profile_net_bps_proxy_mean", ""),
            "breadth_warning": as_int(metric_value(path, "phase193_breadth_warning", 0)),
            "date_count_warning": as_int(metric_value(path, "phase193_date_count_warning", 0)),
            "test_replay_execution": as_int(metric_value(path, "phase193_test_replay_execution", 0)),
            "test_result_allowed": as_int(metric_value(path, "phase193_test_result_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase193_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase193_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase193_next_best_action", ""),
        }
    if phase == 194:
        complete = as_int(metric_value(path, "phase194_fragility_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "frozen_sparse_candidate_closed_for_test_replay_redesign_required" if complete else "sparse_candidate_fragility_decision_gated",
            "fragility_decision_complete": complete,
            "extension_validation_dates": metric_value(path, "phase194_extension_validation_dates", ""),
            "all_extension_profile_dates_negative": as_int(metric_value(path, "phase194_all_extension_profile_dates_negative", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase194_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase194_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase194_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase194_next_best_action", ""),
        }
    if phase == 195:
        complete = as_int(metric_value(path, "phase195_redesign_search_complete", 0))
        passing = as_int(metric_value(path, "phase195_passing_extension_gate_candidates", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "redesign_search_no_extension_gate_survivor_no_test" if complete and passing == 0 else "redesign_search_candidate_precommit_pending" if complete else "redesign_search_gated",
            "redesign_search_complete": complete,
            "passing_extension_gate_candidates": passing,
            "best_candidate_id": metric_value(path, "phase195_best_candidate_id", ""),
            "best_min_extension_net_bps": metric_value(path, "phase195_best_min_extension_net_bps", ""),
            "best_date_positive_fraction": metric_value(path, "phase195_best_date_positive_fraction", ""),
            "best_symbol_positive_fraction": metric_value(path, "phase195_best_symbol_positive_fraction", ""),
            "test_replay_allowed_next": as_int(metric_value(path, "phase195_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase195_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase195_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase195_next_best_action", ""),
        }
    if phase == 196:
        complete = as_int(metric_value(path, "phase196_expanded_model_search_complete", 0))
        passing = as_int(metric_value(path, "phase196_passing_extension_gate_models", 0))
        selected = as_int(metric_value(path, "phase196_train_selected_model_rows", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "expanded_feature_model_search_no_train_survivor_no_test" if complete and selected == 0 else "expanded_feature_model_search_no_extension_survivor_no_test" if complete and passing == 0 else "expanded_feature_model_contract_pending" if complete else "expanded_feature_model_search_gated",
            "expanded_model_search_complete": complete,
            "train_selected_model_rows": selected,
            "passing_extension_gate_models": passing,
            "best_model_id": metric_value(path, "phase196_best_model_id", ""),
            "best_min_extension_net_bps": metric_value(path, "phase196_best_min_extension_net_bps", ""),
            "test_replay_allowed_next": as_int(metric_value(path, "phase196_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase196_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase196_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase196_next_best_action", ""),
        }
    if phase == 197:
        complete = as_int(metric_value(path, "phase197_non_receive_flow_feature_precommit_complete", 0))
        ready = as_int(metric_value(path, "phase197_ready_feature_families", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "non_receive_flow_feature_expansion_precommitted_phase198_ready_no_test" if complete and ready > 0 else "non_receive_flow_feature_expansion_precommitted_no_ready_features_no_test" if complete else "non_receive_flow_feature_expansion_gated",
            "non_receive_flow_feature_precommit_complete": complete,
            "ready_feature_families": ready,
            "strategy_replay_allowed": as_int(metric_value(path, "phase197_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase197_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase197_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase197_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase197_next_best_action", ""),
        }
    if phase == 198:
        complete = as_int(metric_value(path, "phase198_context_model_search_complete", 0))
        selected = as_int(metric_value(path, "phase198_train_selected_model_rows", 0))
        passing = as_int(metric_value(path, "phase198_passing_extension_gate_models", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "non_receive_flow_context_model_search_no_train_survivor_no_test" if complete and selected == 0 else "non_receive_flow_context_model_search_no_extension_survivor_no_test" if complete and passing == 0 else "non_receive_flow_context_model_contract_pending" if complete else "non_receive_flow_context_model_search_gated",
            "context_model_search_complete": complete,
            "train_selected_model_rows": selected,
            "passing_extension_gate_models": passing,
            "best_model_id": metric_value(path, "phase198_best_model_id", ""),
            "best_feature_family": metric_value(path, "phase198_best_feature_family", ""),
            "best_min_extension_net_bps": metric_value(path, "phase198_best_min_extension_net_bps", ""),
            "test_replay_allowed_next": as_int(metric_value(path, "phase198_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase198_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase198_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase198_next_best_action", ""),
        }
    if phase == 199:
        complete = as_int(metric_value(path, "phase199_branch_decision_complete", 0))
        paused = as_int(metric_value(path, "phase199_current_branch_paused", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "current_receive_flow_context_branch_paused_material_redesign_required_no_test" if complete and paused == 1 else "branch_decision_recorded_no_pause_no_test" if complete else "branch_decision_gated",
            "branch_decision_complete": complete,
            "current_branch_paused": paused,
            "material_redesign_required": as_int(metric_value(path, "phase199_material_redesign_required", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase199_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase199_test_replay_allowed_next", 0)),
            "untouched_test_replay_precommit_allowed": as_int(metric_value(path, "phase199_untouched_test_replay_precommit_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase199_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase199_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase199_next_best_action", ""),
        }
    if phase == 200:
        complete = as_int(metric_value(path, "phase200_material_new_hypothesis_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "material_new_passive_queue_hypothesis_precommitted_label_expansion_pending_no_test" if complete else "material_new_hypothesis_precommit_gated",
            "material_new_hypothesis_precommit_complete": complete,
            "selected_hypothesis_id": metric_value(path, "phase200_selected_hypothesis_id", ""),
            "label_contract_rows": as_int(metric_value(path, "phase200_label_contract_rows", 0)),
            "stage_action_rows": as_int(metric_value(path, "phase200_stage_action_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase200_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase200_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase200_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase200_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase200_next_best_action", ""),
        }
    if phase == 201:
        complete = as_int(metric_value(path, "phase201_label_only_stage01_complete", 0))
        pre_replay = as_int(metric_value(path, "phase201_pre_replay_candidate_rows", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "passive_queue_stage01_label_expansion_complete_no_replay_candidate_redesign_pending" if complete and pre_replay == 0 else "passive_queue_stage01_label_expansion_complete_candidate_precommit_pending" if complete else "passive_queue_stage01_label_expansion_gated",
            "label_only_stage01_complete": complete,
            "pre_replay_candidate_rows": pre_replay,
            "joined_label_candidate_rows": as_int(metric_value(path, "phase201_joined_label_candidate_rows", 0)),
            "max_candidate_symbols": as_int(metric_value(path, "phase201_max_candidate_symbols", 0)),
            "max_candidate_trade_dates": as_int(metric_value(path, "phase201_max_candidate_trade_dates", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase201_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase201_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase201_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase201_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase201_next_best_action", ""),
        }
    if phase == 202:
        complete = as_int(metric_value(path, "phase202_passive_feature_redesign_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "passive_feature_redesign_precommitted_label_materialization_pending_no_replay" if complete else "passive_feature_redesign_precommit_gated",
            "passive_feature_redesign_precommit_complete": complete,
            "redesigned_feature_rows": as_int(metric_value(path, "phase202_redesigned_feature_rows", 0)),
            "acceptance_contract_rows": as_int(metric_value(path, "phase202_acceptance_contract_rows", 0)),
            "phase203_action_rows": as_int(metric_value(path, "phase202_phase203_action_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase202_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase202_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase202_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase202_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase202_next_best_action", ""),
        }
    if phase == 203:
        complete = as_int(metric_value(path, "phase203_label_materialization_complete", 0))
        candidate_gate = as_int(metric_value(path, "phase203_candidate_gate_open", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "redesigned_passive_labels_materialized_candidate_gate_closed_no_replay" if complete and candidate_gate == 0 else "redesigned_passive_labels_materialized_candidate_precommit_pending" if complete else "redesigned_passive_label_materialization_gated",
            "label_materialization_complete": complete,
            "materialized_label_rows": as_int(metric_value(path, "phase203_materialized_label_rows", 0)),
            "redesigned_candidate_pass_rows": as_int(metric_value(path, "phase203_redesigned_candidate_pass_rows", 0)),
            "max_candidate_symbols": as_int(metric_value(path, "phase203_max_candidate_symbols", 0)),
            "max_candidate_trade_dates": as_int(metric_value(path, "phase203_max_candidate_trade_dates", 0)),
            "adverse_selection_ceiling_met": as_int(metric_value(path, "phase203_adverse_selection_ceiling_met", 0)),
            "candidate_gate_open": candidate_gate,
            "strategy_replay_allowed": as_int(metric_value(path, "phase203_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase203_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase203_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase203_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase203_next_best_action", ""),
        }
    if phase == 204:
        complete = as_int(metric_value(path, "phase204_closure_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "passive_redesign_closed_for_replay_material_new_source_or_label_breadth_pending_no_replay" if complete else "passive_redesign_closure_decision_gated",
            "closure_decision_complete": complete,
            "current_passive_redesign_closed_for_replay": as_int(metric_value(path, "phase204_current_passive_redesign_closed_for_replay", 0)),
            "material_new_source_required": as_int(metric_value(path, "phase204_material_new_source_required", 0)),
            "broader_label_materialization_allowed": as_int(metric_value(path, "phase204_broader_label_materialization_allowed", 0)),
            "threshold_widening_allowed": as_int(metric_value(path, "phase204_threshold_widening_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase204_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase204_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase204_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase204_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase204_next_best_action", ""),
        }
    if phase == 205:
        complete = as_int(metric_value(path, "phase205_material_new_source_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "material_new_source_precommitted_phase206_contract_pending_no_replay" if complete else "material_new_source_precommit_gated",
            "material_new_source_precommit_complete": complete,
            "selected_route_id": metric_value(path, "phase205_selected_route_id", ""),
            "route_scorecard_rows": as_int(metric_value(path, "phase205_route_scorecard_rows", 0)),
            "phase206_work_order_rows": as_int(metric_value(path, "phase205_phase206_work_order_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase205_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase205_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase205_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase205_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase205_next_best_action", ""),
        }
    if phase == 206:
        complete = as_int(metric_value(path, "phase206_nonoverlap_feature_contract_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "selected_source_nonoverlap_feature_contract_complete_phase207_matrix_pending_no_replay" if complete else "selected_source_nonoverlap_feature_contract_gated",
            "nonoverlap_feature_contract_complete": complete,
            "feature_catalog_rows": as_int(metric_value(path, "phase206_feature_catalog_rows", 0)),
            "blocked_reference_rows": as_int(metric_value(path, "phase206_blocked_reference_rows", 0)),
            "nonoverlap_pass_rows": as_int(metric_value(path, "phase206_nonoverlap_pass_rows", 0)),
            "phase207_work_order_rows": as_int(metric_value(path, "phase206_phase207_work_order_rows", 0)),
            "model_fit_allowed": as_int(metric_value(path, "phase206_model_fit_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase206_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase206_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase206_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase206_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase206_next_best_action", ""),
        }
    if phase == 207:
        complete = as_int(metric_value(path, "phase207_feature_matrix_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "allowed_feature_matrix_precommitted_phase208_quality_gate_pending_no_model_no_replay" if complete else "allowed_feature_matrix_precommit_gated",
            "feature_matrix_precommit_complete": complete,
            "feature_matrix_rows": as_int(metric_value(path, "phase207_feature_matrix_rows", 0)),
            "feature_available_rows": as_int(metric_value(path, "phase207_feature_available_rows", 0)),
            "trade_dates_max": as_int(metric_value(path, "phase207_trade_dates_max", 0)),
            "symbols_max": as_int(metric_value(path, "phase207_symbols_max", 0)),
            "model_fit_allowed": as_int(metric_value(path, "phase207_model_fit_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase207_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase207_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase207_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase207_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase207_next_best_action", ""),
        }
    if phase == 208:
        complete = as_int(metric_value(path, "phase208_feature_matrix_quality_gate_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "feature_matrix_quality_gate_complete_phase209_model_precommit_pending_no_execution_no_replay" if complete else "feature_matrix_quality_gate_blocked",
            "feature_matrix_quality_gate_complete": complete,
            "quality_summary_rows": as_int(metric_value(path, "phase208_quality_summary_rows", 0)),
            "quality_pass_rows": as_int(metric_value(path, "phase208_quality_pass_rows", 0)),
            "blocking_gap_rows": as_int(metric_value(path, "phase208_blocking_gap_rows", 0)),
            "trade_dates_max": as_int(metric_value(path, "phase208_trade_dates_max", 0)),
            "symbols_max": as_int(metric_value(path, "phase208_symbols_max", 0)),
            "model_fit_allowed": as_int(metric_value(path, "phase208_model_fit_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase208_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase208_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase208_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase208_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase208_next_best_action", ""),
        }
    if phase == 209:
        complete = as_int(metric_value(path, "phase209_model_fit_precommit_spec_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "model_fit_precommit_spec_complete_phase210_train_validation_fit_dry_run_pending_no_replay_no_test" if complete else "model_fit_precommit_spec_gated",
            "model_fit_precommit_spec_complete": complete,
            "model_spec_rows": as_int(metric_value(path, "phase209_model_spec_rows", 0)),
            "feature_set_rows": as_int(metric_value(path, "phase209_feature_set_rows", 0)),
            "allowed_feature_set_rows": as_int(metric_value(path, "phase209_allowed_feature_set_rows", 0)),
            "label_target_rows": as_int(metric_value(path, "phase209_label_target_rows", 0)),
            "split_control_rows": as_int(metric_value(path, "phase209_split_control_rows", 0)),
            "forbidden_execution_rows": as_int(metric_value(path, "phase209_forbidden_execution_rows", 0)),
            "model_fit_execution_allowed": as_int(metric_value(path, "phase209_model_fit_execution_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase209_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase209_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase209_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase209_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase209_next_best_action", ""),
        }
    if phase == 210:
        complete = as_int(metric_value(path, "phase210_train_validation_model_fit_dry_run_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "train_validation_model_fit_dry_run_complete_phase211_validation_interpretation_pending_no_replay_no_test" if complete else "train_validation_model_fit_dry_run_gated",
            "train_validation_model_fit_dry_run_complete": complete,
            "design_matrix_partition_rows": as_int(metric_value(path, "phase210_design_matrix_partition_rows", 0)),
            "design_matrix_joined_rows": as_int(metric_value(path, "phase210_design_matrix_joined_rows", 0)),
            "model_fit_rows": as_int(metric_value(path, "phase210_model_fit_rows", 0)),
            "validation_metric_rows": as_int(metric_value(path, "phase210_validation_metric_rows", 0)),
            "negative_control_rows": as_int(metric_value(path, "phase210_negative_control_rows", 0)),
            "coefficient_rows": as_int(metric_value(path, "phase210_coefficient_rows", 0)),
            "model_fit_execution": as_int(metric_value(path, "phase210_model_fit_execution", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase210_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase210_test_replay_allowed_next", 0)),
            "test_rows_used": as_int(metric_value(path, "phase210_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase210_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase210_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase210_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase210_next_best_action", ""),
        }
    if phase == 211:
        complete = as_int(metric_value(path, "phase211_model_fit_validation_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "model_fit_validation_interpretation_complete_phase212_closure_or_redesign_pending_no_replay_no_test" if complete else "model_fit_validation_interpretation_gated",
            "model_fit_validation_interpretation_complete": complete,
            "interpretation_rows": as_int(metric_value(path, "phase211_interpretation_rows", 0)),
            "family_summary_rows": as_int(metric_value(path, "phase211_family_summary_rows", 0)),
            "passing_interpretation_rows": as_int(metric_value(path, "phase211_passing_interpretation_rows", 0)),
            "best_mse_improvement_pct_vs_control": metric_value(path, "phase211_best_mse_improvement_pct_vs_control", 0),
            "best_abs_validation_correlation": metric_value(path, "phase211_best_abs_validation_correlation", 0),
            "best_binary_accuracy_lift_vs_control": metric_value(path, "phase211_best_binary_accuracy_lift_vs_control", 0),
            "candidate_opened_for_replay": as_int(metric_value(path, "phase211_candidate_opened_for_replay", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase211_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase211_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase211_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase211_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase211_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase211_next_best_action", ""),
        }
    if phase == 212:
        complete = as_int(metric_value(path, "phase212_model_family_closure_or_redesign_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "model_family_closure_or_redesign_precommit_complete_phase213_material_new_source_pending_no_replay_no_test" if complete else "model_family_closure_or_redesign_precommit_gated",
            "model_family_closure_or_redesign_precommit_complete": complete,
            "family_closure_rows": as_int(metric_value(path, "phase212_family_closure_rows", 0)),
            "families_closed_for_replay": as_int(metric_value(path, "phase212_families_closed_for_replay", 0)),
            "reuse_without_redesign_allowed": as_int(metric_value(path, "phase212_reuse_without_redesign_allowed", 0)),
            "failure_mode_rows": as_int(metric_value(path, "phase212_failure_mode_rows", 0)),
            "redesign_precommit_rows": as_int(metric_value(path, "phase212_redesign_precommit_rows", 0)),
            "action_queue_rows": as_int(metric_value(path, "phase212_action_queue_rows", 0)),
            "candidate_opened_for_replay": as_int(metric_value(path, "phase212_candidate_opened_for_replay", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase212_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase212_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase212_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase212_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase212_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase212_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase212_next_best_action", ""),
        }
    if phase == 213:
        complete = as_int(metric_value(path, "phase213_material_new_model_source_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "material_new_model_source_precommit_complete_phase214_event_surprise_label_materialization_pending_no_model_no_replay_no_test" if complete else "material_new_model_source_precommit_gated",
            "material_new_model_source_precommit_complete": complete,
            "source_selection_rows": as_int(metric_value(path, "phase213_source_selection_rows", 0)),
            "selected_source_id": metric_value(path, "phase213_selected_source_id", ""),
            "label_contract_rows": as_int(metric_value(path, "phase213_label_contract_rows", 0)),
            "feature_requirement_rows": as_int(metric_value(path, "phase213_feature_requirement_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase213_control_contract_rows", 0)),
            "phase214_work_order_rows": as_int(metric_value(path, "phase213_phase214_work_order_rows", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase213_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase213_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase213_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase213_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase213_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase213_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase213_next_best_action", ""),
        }
    if phase == 214:
        complete = as_int(metric_value(path, "phase214_event_surprise_label_materialization_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_surprise_label_materialization_complete_phase215_quality_interpretation_pending_no_model_no_replay_no_test" if complete else "event_surprise_label_materialization_gated",
            "event_surprise_label_materialization_complete": complete,
            "label_partition_rows": as_int(metric_value(path, "phase214_label_partition_rows", 0)),
            "label_rows": as_int(metric_value(path, "phase214_label_rows", 0)),
            "event_surprise_rows": as_int(metric_value(path, "phase214_event_surprise_rows", 0)),
            "quality_rows": as_int(metric_value(path, "phase214_quality_rows", 0)),
            "quality_pass_rows": as_int(metric_value(path, "phase214_quality_pass_rows", 0)),
            "split_balance_rows": as_int(metric_value(path, "phase214_split_balance_rows", 0)),
            "sealed_test_inventory_rows": as_int(metric_value(path, "phase214_sealed_test_inventory_rows", 0)),
            "sealed_test_rows_used": as_int(metric_value(path, "phase214_sealed_test_rows_used", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase214_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase214_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase214_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase214_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase214_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase214_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase214_next_best_action", ""),
        }
    if phase == 215:
        complete = as_int(metric_value(path, "phase215_event_surprise_label_quality_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_surprise_label_quality_interpretation_complete_phase216_event_only_target_precommit_pending_no_model_no_replay_no_test" if complete else "event_surprise_label_quality_interpretation_gated",
            "event_surprise_label_quality_interpretation_complete": complete,
            "interpretation_rows": as_int(metric_value(path, "phase215_interpretation_rows", 0)),
            "passing_interpretation_rows": as_int(metric_value(path, "phase215_passing_interpretation_rows", 0)),
            "label_family_summary_rows": as_int(metric_value(path, "phase215_label_family_summary_rows", 0)),
            "label_families_with_interpretable_rows": as_int(metric_value(path, "phase215_label_families_with_interpretable_rows", 0)),
            "phase216_work_order_rows": as_int(metric_value(path, "phase215_phase216_work_order_rows", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase215_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase215_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase215_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase215_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase215_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase215_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase215_next_best_action", ""),
        }
    if phase == 216:
        complete = as_int(metric_value(path, "phase216_event_surprise_event_only_target_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_surprise_event_only_target_precommit_complete_phase217_design_matrix_precommit_pending_no_model_no_replay_no_test" if complete else "event_surprise_event_only_target_precommit_gated",
            "event_surprise_event_only_target_precommit_complete": complete,
            "event_only_target_rows": as_int(metric_value(path, "phase216_event_only_target_rows", 0)),
            "full_train_validation_target_rows": as_int(metric_value(path, "phase216_full_train_validation_target_rows", 0)),
            "excluded_target_rows": as_int(metric_value(path, "phase216_excluded_target_rows", 0)),
            "event_only_contract_rows": as_int(metric_value(path, "phase216_event_only_contract_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase216_control_contract_rows", 0)),
            "phase217_work_order_rows": as_int(metric_value(path, "phase216_phase217_work_order_rows", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase216_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase216_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase216_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase216_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase216_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase216_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase216_next_best_action", ""),
        }
    if phase == 217:
        complete = as_int(metric_value(path, "phase217_event_only_design_matrix_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_design_matrix_precommit_complete_phase218_model_fit_precommit_or_stop_pending_no_replay_no_test" if complete else "event_only_design_matrix_precommit_gated",
            "event_only_design_matrix_precommit_complete": complete,
            "target_scope_rows": as_int(metric_value(path, "phase217_target_scope_rows", 0)),
            "feature_binding_rows": as_int(metric_value(path, "phase217_feature_binding_rows", 0)),
            "control_plan_rows": as_int(metric_value(path, "phase217_control_plan_rows", 0)),
            "design_matrix_contract_rows": as_int(metric_value(path, "phase217_design_matrix_contract_rows", 0)),
            "phase218_work_order_rows": as_int(metric_value(path, "phase217_phase218_work_order_rows", 0)),
            "target_row_observation_scope": as_int(metric_value(path, "phase217_target_row_observation_scope", 0)),
            "row_level_design_matrix_export_allowed": as_int(metric_value(path, "phase217_row_level_design_matrix_export_allowed", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase217_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase217_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase217_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase217_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase217_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase217_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase217_next_best_action", ""),
        }
    if phase == 218:
        complete = as_int(metric_value(path, "phase218_event_only_model_fit_precommit_or_stop_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_model_fit_precommit_complete_phase219_train_validation_fit_dry_run_pending_no_replay_no_test" if complete else "event_only_model_fit_precommit_or_stop_gated",
            "event_only_model_fit_precommit_or_stop_complete": complete,
            "decision_rows": as_int(metric_value(path, "phase218_decision_rows", 0)),
            "model_spec_rows": as_int(metric_value(path, "phase218_model_spec_rows", 0)),
            "target_contract_rows": as_int(metric_value(path, "phase218_target_contract_rows", 0)),
            "feature_contract_rows": as_int(metric_value(path, "phase218_feature_contract_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase218_control_contract_rows", 0)),
            "phase219_work_order_rows": as_int(metric_value(path, "phase218_phase219_work_order_rows", 0)),
            "model_fit_dry_run_precommitted_for_phase219": as_int(metric_value(path, "phase218_model_fit_dry_run_precommitted_for_phase219", 0)),
            "model_fit_execution_allowed": as_int(metric_value(path, "phase218_model_fit_execution_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase218_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase218_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase218_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase218_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase218_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase218_next_best_action", ""),
        }
    if phase == 219:
        complete = as_int(metric_value(path, "phase219_event_only_train_validation_model_fit_dry_run_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_train_validation_model_fit_dry_run_complete_phase220_validation_interpretation_pending_no_replay_no_test" if complete else "event_only_train_validation_model_fit_dry_run_gated",
            "event_only_train_validation_model_fit_dry_run_complete": complete,
            "event_only_partition_rows": as_int(metric_value(path, "phase219_event_only_partition_rows", 0)),
            "event_only_joined_rows": as_int(metric_value(path, "phase219_event_only_joined_rows", 0)),
            "model_fit_rows": as_int(metric_value(path, "phase219_model_fit_rows", 0)),
            "metric_rows": as_int(metric_value(path, "phase219_metric_rows", 0)),
            "validation_metric_rows": as_int(metric_value(path, "phase219_validation_metric_rows", 0)),
            "coefficient_rows": as_int(metric_value(path, "phase219_coefficient_rows", 0)),
            "control_rows": as_int(metric_value(path, "phase219_control_rows", 0)),
            "model_fit_execution": as_int(metric_value(path, "phase219_model_fit_execution", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase219_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase219_test_replay_allowed_next", 0)),
            "test_rows_used": as_int(metric_value(path, "phase219_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase219_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase219_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase219_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase219_next_best_action", ""),
        }
    if phase == 220:
        complete = as_int(metric_value(path, "phase220_event_only_model_fit_validation_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_model_fit_validation_interpretation_complete_phase221_signal_replay_precommit_or_stop_pending_no_replay_no_test" if complete else "event_only_model_fit_validation_interpretation_gated",
            "event_only_model_fit_validation_interpretation_complete": complete,
            "interpretation_rows": as_int(metric_value(path, "phase220_interpretation_rows", 0)),
            "passing_candidate_rows": as_int(metric_value(path, "phase220_passing_candidate_rows", 0)),
            "candidate_family_rows": as_int(metric_value(path, "phase220_candidate_family_rows", 0)),
            "best_mse_improvement_vs_base": metric_value(path, "phase220_best_mse_improvement_vs_base", 0),
            "best_improvement_vs_shuffle": metric_value(path, "phase220_best_improvement_vs_shuffle", 0),
            "best_validation_correlation": metric_value(path, "phase220_best_validation_correlation", 0),
            "phase221_work_order_rows": as_int(metric_value(path, "phase220_phase221_work_order_rows", 0)),
            "candidate_opened_for_phase221_precommit": as_int(metric_value(path, "phase220_candidate_opened_for_phase221_precommit", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase220_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase220_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase220_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase220_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase220_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase220_next_best_action", ""),
        }
    if phase == 221:
        complete = as_int(metric_value(path, "phase221_event_only_signal_replay_precommit_or_stop_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_signal_replay_precommit_complete_phase222_train_validation_replay_dry_run_pending_no_test" if complete else "event_only_signal_replay_precommit_or_stop_gated",
            "event_only_signal_replay_precommit_or_stop_complete": complete,
            "decision_rows": as_int(metric_value(path, "phase221_decision_rows", 0)),
            "candidate_rows": as_int(metric_value(path, "phase221_candidate_rows", 0)),
            "signal_rule_rows": as_int(metric_value(path, "phase221_signal_rule_rows", 0)),
            "replay_contract_rows": as_int(metric_value(path, "phase221_replay_contract_rows", 0)),
            "phase222_work_order_rows": as_int(metric_value(path, "phase221_phase222_work_order_rows", 0)),
            "phase222_replay_dry_run_precommitted": as_int(metric_value(path, "phase221_phase222_replay_dry_run_precommitted", 0)),
            "strategy_replay_execution_allowed": as_int(metric_value(path, "phase221_strategy_replay_execution_allowed", 0)),
            "strategy_replay_allowed_next": as_int(metric_value(path, "phase221_strategy_replay_allowed_next", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase221_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase221_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase221_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase221_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase221_next_best_action", ""),
        }
    if phase == 222:
        complete = as_int(metric_value(path, "phase222_event_only_train_validation_signal_replay_dry_run_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_train_validation_signal_replay_dry_run_complete_phase223_validation_interpretation_pending_no_test" if complete else "event_only_train_validation_signal_replay_dry_run_gated",
            "event_only_train_validation_signal_replay_dry_run_complete": complete,
            "event_only_partition_rows": as_int(metric_value(path, "phase222_event_only_partition_rows", 0)),
            "event_only_joined_rows": as_int(metric_value(path, "phase222_event_only_joined_rows", 0)),
            "threshold_activation_rows": as_int(metric_value(path, "phase222_threshold_activation_rows", 0)),
            "replay_summary_rows": as_int(metric_value(path, "phase222_replay_summary_rows", 0)),
            "control_rows": as_int(metric_value(path, "phase222_control_rows", 0)),
            "validation_screen_rows": as_int(metric_value(path, "phase222_validation_screen_rows", 0)),
            "validation_decision_events": as_int(metric_value(path, "phase222_validation_decision_events", 0)),
            "best_validation_net_after_cost_bps_proxy": metric_value(path, "phase222_best_validation_net_after_cost_bps_proxy", ""),
            "worst_validation_net_after_cost_bps_proxy": metric_value(path, "phase222_worst_validation_net_after_cost_bps_proxy", ""),
            "strategy_replay_execution": as_int(metric_value(path, "phase222_strategy_replay_execution", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase222_test_replay_allowed_next", 0)),
            "test_rows_used": as_int(metric_value(path, "phase222_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase222_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase222_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase222_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase222_next_best_action", ""),
        }
    if phase == 223:
        complete = as_int(metric_value(path, "phase223_event_only_signal_replay_validation_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_signal_replay_validation_interpretation_complete_phase224_closure_or_redesign_precommit_pending_no_test" if complete else "event_only_signal_replay_validation_interpretation_gated",
            "event_only_signal_replay_validation_interpretation_complete": complete,
            "interpretation_rows": as_int(metric_value(path, "phase223_interpretation_rows", 0)),
            "profile_summary_rows": as_int(metric_value(path, "phase223_profile_summary_rows", 0)),
            "target_summary_rows": as_int(metric_value(path, "phase223_target_summary_rows", 0)),
            "validation_decision_events": as_int(metric_value(path, "phase223_validation_decision_events", 0)),
            "positive_net_validation_rows": as_int(metric_value(path, "phase223_positive_net_validation_rows", 0)),
            "passing_interpretation_rows": as_int(metric_value(path, "phase223_passing_interpretation_rows", 0)),
            "cost_dominates_rows": as_int(metric_value(path, "phase223_cost_dominates_rows", 0)),
            "best_validation_net_after_cost_bps_proxy": metric_value(path, "phase223_best_validation_net_after_cost_bps_proxy", ""),
            "worst_validation_net_after_cost_bps_proxy": metric_value(path, "phase223_worst_validation_net_after_cost_bps_proxy", ""),
            "best_actual_vs_shuffle_net_edge_bps": metric_value(path, "phase223_best_actual_vs_shuffle_net_edge_bps", ""),
            "phase224_work_order_rows": as_int(metric_value(path, "phase223_phase224_work_order_rows", 0)),
            "broader_replay_allowed_next": as_int(metric_value(path, "phase223_broader_replay_allowed_next", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase223_test_replay_allowed_next", 0)),
            "test_rows_used": as_int(metric_value(path, "phase223_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase223_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase223_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase223_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase223_next_best_action", ""),
        }
    if phase == 224:
        complete = as_int(metric_value(path, "phase224_event_only_signal_replay_closure_or_redesign_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "event_only_signal_replay_candidate_set_closed_phase225_cost_aware_redesign_precommit_pending_no_fit_no_replay_no_test" if complete else "event_only_signal_replay_closure_or_redesign_precommit_gated",
            "event_only_signal_replay_closure_or_redesign_precommit_complete": complete,
            "closure_rows": as_int(metric_value(path, "phase224_closure_rows", 0)),
            "current_candidate_set_closed_for_broader_replay": as_int(metric_value(path, "phase224_current_candidate_set_closed_for_broader_replay", 0)),
            "current_candidate_set_closed_for_test": as_int(metric_value(path, "phase224_current_candidate_set_closed_for_test", 0)),
            "reuse_without_material_redesign_allowed": as_int(metric_value(path, "phase224_reuse_without_material_redesign_allowed", 0)),
            "failure_mode_rows": as_int(metric_value(path, "phase224_failure_mode_rows", 0)),
            "redesign_route_rows": as_int(metric_value(path, "phase224_redesign_route_rows", 0)),
            "phase225_work_order_rows": as_int(metric_value(path, "phase224_phase225_work_order_rows", 0)),
            "selected_redesign_route": metric_value(path, "phase224_selected_redesign_route", ""),
            "phase223_positive_net_validation_rows": as_int(metric_value(path, "phase224_phase223_positive_net_validation_rows", 0)),
            "phase223_passing_interpretation_rows": as_int(metric_value(path, "phase224_phase223_passing_interpretation_rows", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase224_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase224_strategy_replay_allowed", 0)),
            "broader_replay_allowed_next": as_int(metric_value(path, "phase224_broader_replay_allowed_next", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase224_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase224_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase224_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase224_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase224_next_best_action", ""),
        }
    if phase == 225:
        complete = as_int(metric_value(path, "phase225_cost_aware_event_source_redesign_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_aware_event_source_redesign_precommit_complete_phase226_label_materialization_pending_no_fit_no_replay_no_test" if complete else "cost_aware_event_source_redesign_precommit_gated",
            "cost_aware_event_source_redesign_precommit_complete": complete,
            "cost_hurdle_rows": as_int(metric_value(path, "phase225_cost_hurdle_rows", 0)),
            "label_contract_rows": as_int(metric_value(path, "phase225_label_contract_rows", 0)),
            "negative_control_rows": as_int(metric_value(path, "phase225_negative_control_rows", 0)),
            "phase226_work_order_rows": as_int(metric_value(path, "phase225_phase226_work_order_rows", 0)),
            "selected_route_id": metric_value(path, "phase225_selected_route_id", ""),
            "label_materialization_allowed_next": as_int(metric_value(path, "phase225_label_materialization_allowed_next", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase225_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase225_strategy_replay_allowed", 0)),
            "broader_replay_allowed_next": as_int(metric_value(path, "phase225_broader_replay_allowed_next", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase225_test_replay_allowed_next", 0)),
            "test_rows_used": as_int(metric_value(path, "phase225_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase225_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase225_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase225_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase225_next_best_action", ""),
        }
    if phase == 226:
        complete = as_int(metric_value(path, "phase226_cost_aware_event_label_materialization_dry_run_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_aware_event_label_materialization_complete_phase227_quality_interpretation_pending_no_fit_no_replay_no_test" if complete else "cost_aware_event_label_materialization_gated",
            "cost_aware_event_label_materialization_dry_run_complete": complete,
            "horizon_availability_rows": as_int(metric_value(path, "phase226_horizon_availability_rows", 0)),
            "available_horizon_rows": as_int(metric_value(path, "phase226_available_horizon_rows", 0)),
            "blocked_horizon_rows": as_int(metric_value(path, "phase226_blocked_horizon_rows", 0)),
            "label_partition_rows": as_int(metric_value(path, "phase226_label_partition_rows", 0)),
            "materialized_horizons": as_int(metric_value(path, "phase226_materialized_horizons", 0)),
            "total_label_rows": as_int(metric_value(path, "phase226_total_label_rows", 0)),
            "cost_aware_actionable_rows": as_int(metric_value(path, "phase226_cost_aware_actionable_rows", 0)),
            "cost_aware_up_rows": as_int(metric_value(path, "phase226_cost_aware_up_rows", 0)),
            "cost_aware_down_rows": as_int(metric_value(path, "phase226_cost_aware_down_rows", 0)),
            "split_summary_rows": as_int(metric_value(path, "phase226_split_summary_rows", 0)),
            "quality_pass_rows": as_int(metric_value(path, "phase226_quality_pass_rows", 0)),
            "negative_control_summary_rows": as_int(metric_value(path, "phase226_negative_control_summary_rows", 0)),
            "sealed_test_rows_available": as_int(metric_value(path, "phase226_sealed_test_rows_available", 0)),
            "test_rows_used": as_int(metric_value(path, "phase226_test_rows_used", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase226_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase226_strategy_replay_allowed", 0)),
            "broader_replay_allowed_next": as_int(metric_value(path, "phase226_broader_replay_allowed_next", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase226_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase226_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase226_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase226_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase226_next_best_action", ""),
        }
    if phase == 227:
        complete = as_int(metric_value(path, "phase227_cost_aware_event_label_quality_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_aware_event_label_quality_interpretation_complete_phase228_closure_or_redesign_pending_no_fit_no_replay_no_test" if complete else "cost_aware_event_label_quality_interpretation_gated",
            "cost_aware_event_label_quality_interpretation_complete": complete,
            "quality_interpretation_rows": as_int(metric_value(path, "phase227_quality_interpretation_rows", 0)),
            "horizon_interpretation_rows": as_int(metric_value(path, "phase227_horizon_interpretation_rows", 0)),
            "failure_mode_rows": as_int(metric_value(path, "phase227_failure_mode_rows", 0)),
            "phase228_work_order_rows": as_int(metric_value(path, "phase227_phase228_work_order_rows", 0)),
            "actionable_rows": as_int(metric_value(path, "phase227_actionable_rows", 0)),
            "quality_pass_rows": as_int(metric_value(path, "phase227_quality_pass_rows", 0)),
            "fit_precommit_candidate_rows": as_int(metric_value(path, "phase227_fit_precommit_candidate_rows", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase227_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase227_strategy_replay_allowed", 0)),
            "broader_replay_allowed_next": as_int(metric_value(path, "phase227_broader_replay_allowed_next", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase227_test_replay_allowed_next", 0)),
            "test_rows_used": as_int(metric_value(path, "phase227_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase227_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase227_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase227_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase227_next_best_action", ""),
        }
    if phase == 228:
        complete = as_int(metric_value(path, "phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_aware_label_set_closed_phase229_source_expansion_precommit_pending_no_materialization_no_fit_no_replay_no_test" if complete else "cost_aware_label_redesign_closure_or_relaxation_precommit_gated",
            "cost_aware_label_redesign_closure_or_relaxation_precommit_complete": complete,
            "closure_rows": as_int(metric_value(path, "phase228_closure_rows", 0)),
            "current_label_set_closed_for_fit": as_int(metric_value(path, "phase228_current_label_set_closed_for_fit", 0)),
            "current_label_set_closed_for_replay": as_int(metric_value(path, "phase228_current_label_set_closed_for_replay", 0)),
            "redesign_route_rows": as_int(metric_value(path, "phase228_redesign_route_rows", 0)),
            "guardrail_rows": as_int(metric_value(path, "phase228_guardrail_rows", 0)),
            "phase229_work_order_rows": as_int(metric_value(path, "phase228_phase229_work_order_rows", 0)),
            "selected_route_id": metric_value(path, "phase228_selected_route_id", ""),
            "label_materialization_allowed_next": as_int(metric_value(path, "phase228_label_materialization_allowed_next", 0)),
            "model_fit_allowed_next": as_int(metric_value(path, "phase228_model_fit_allowed_next", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase228_strategy_replay_allowed", 0)),
            "broader_replay_allowed_next": as_int(metric_value(path, "phase228_broader_replay_allowed_next", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase228_test_replay_allowed_next", 0)),
            "test_rows_used": as_int(metric_value(path, "phase228_test_rows_used", 0)),
            "threshold_widening_allowed": as_int(metric_value(path, "phase228_threshold_widening_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase228_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase228_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase228_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase228_next_best_action", ""),
        }
    if phase == 229:
        complete = as_int(metric_value(path, "phase229_multi_strategy_profitability_search_complete", 0))
        positive_realistic = as_int(metric_value(path, "phase229_positive_realistic_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "multi_strategy_profitability_search_complete" if complete else "multi_strategy_profitability_search_gated",
            "multi_strategy_profitability_search_complete": complete,
            "source_summary_rows": as_int(metric_value(path, "phase229_source_summary_rows", 0)),
            "distinct_strategy_ids": as_int(metric_value(path, "phase229_distinct_strategy_ids", 0)),
            "realistic_profile_rows": as_int(metric_value(path, "phase229_realistic_profile_rows", 0)),
            "positive_realistic_candidate_rows": positive_realistic,
            "positive_any_profile_rows": as_int(metric_value(path, "phase229_positive_any_profile_rows", 0)),
            "best_strategy_id": metric_value(path, "phase229_best_strategy_id", ""),
            "best_execution_profile": metric_value(path, "phase229_best_execution_profile", ""),
            "best_annual_net_pnl_inr": metric_value(path, "phase229_best_annual_net_pnl_inr", 0),
            "strategy_replay_allowed": int(positive_realistic > 0),
            "promotion_allowed": as_int(metric_value(path, "phase229_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase229_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase229_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase229_next_best_action", ""),
        }
    if phase == 230:
        complete = as_int(metric_value(path, "phase230_low_turnover_high_edge_search_complete", 0))
        positive_expanded = as_int(metric_value(path, "phase230_positive_expanded_group_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "low_turnover_high_edge_expansion_complete" if complete else "low_turnover_high_edge_expansion_gated",
            "low_turnover_high_edge_search_complete": complete,
            "phase164_ledger_rows": as_int(metric_value(path, "phase230_phase164_ledger_rows", 0)),
            "realistic_ledger_rows": as_int(metric_value(path, "phase230_realistic_ledger_rows", 0)),
            "group_scope_rows": as_int(metric_value(path, "phase230_group_scope_rows", 0)),
            "variant_group_rows": as_int(metric_value(path, "phase230_variant_group_rows", 0)),
            "positive_expanded_group_rows": positive_expanded,
            "positive_oracle_signed_group_rows": as_int(metric_value(path, "phase230_positive_oracle_signed_group_rows", 0)),
            "best_scope": metric_value(path, "phase230_best_scope", ""),
            "best_strategy_id": metric_value(path, "phase230_best_strategy_id", ""),
            "best_execution_profile": metric_value(path, "phase230_best_execution_profile", ""),
            "best_expanded_variant": metric_value(path, "phase230_best_expanded_variant", ""),
            "best_expanded_net_pnl_inr": metric_value(path, "phase230_best_expanded_net_pnl_inr", 0),
            "strategy_replay_allowed": int(positive_expanded > 0),
            "promotion_allowed": as_int(metric_value(path, "phase230_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase230_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase230_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase230_next_best_action", ""),
        }
    if phase == 231:
        complete = as_int(metric_value(path, "phase231_material_new_strategy_forms_complete", 0))
        synthetic_candidates = as_int(metric_value(path, "phase231_synthetic_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "material_new_strategy_forms_positive_synthetic_candidates_found" if synthetic_candidates > 0 else ("material_new_strategy_forms_complete_no_candidates" if complete else "material_new_strategy_forms_gated"),
            "material_new_strategy_forms_complete": complete,
            "event_bar_rows": as_int(metric_value(path, "phase231_event_bar_rows", 0)),
            "candidate_rows": as_int(metric_value(path, "phase231_candidate_rows", 0)),
            "trade_ledger_rows": as_int(metric_value(path, "phase231_trade_ledger_rows", 0)),
            "train_pass_candidates": as_int(metric_value(path, "phase231_train_pass_candidates", 0)),
            "test_pass_candidates": as_int(metric_value(path, "phase231_test_pass_candidates", 0)),
            "synthetic_candidate_rows": synthetic_candidates,
            "best_candidate_id": metric_value(path, "phase231_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase231_best_family_id", ""),
            "best_train_net_pnl_inr": metric_value(path, "phase231_best_train_net_pnl_inr", 0),
            "best_test_net_pnl_inr": metric_value(path, "phase231_best_test_net_pnl_inr", 0),
            "best_test_precision_cost_clear": metric_value(path, "phase231_best_test_precision_cost_clear", 0),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase231_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase231_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase231_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase231_next_best_action", ""),
        }
    if phase == 232:
        complete = as_int(metric_value(path, "phase232_validate_phase231_candidates_complete", 0))
        validated = as_int(metric_value(path, "phase232_validated_synthetic_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "phase231_candidate_validated_by_stricter_controls" if validated > 0 else ("phase231_candidates_failed_stricter_controls" if complete else "phase231_validation_gated"),
            "validate_phase231_candidates_complete": complete,
            "phase231_candidate_rows": as_int(metric_value(path, "phase232_phase231_candidate_rows", 0)),
            "negative_control_pass_rows": as_int(metric_value(path, "phase232_negative_control_pass_rows", 0)),
            "cost_stress_pass_rows": as_int(metric_value(path, "phase232_cost_stress_pass_rows", 0)),
            "holdout_stability_pass_rows": as_int(metric_value(path, "phase232_holdout_stability_pass_rows", 0)),
            "validated_synthetic_candidate_rows": validated,
            "best_candidate_id": metric_value(path, "phase232_best_candidate_id", ""),
            "best_test_net_pnl_inr": metric_value(path, "phase232_best_test_net_pnl_inr", 0),
            "best_test_random_side_beat_fraction": metric_value(path, "phase232_best_test_random_side_beat_fraction", 0),
            "best_test_leave_one_month_min_net_pnl_inr": metric_value(path, "phase232_best_test_leave_one_month_min_net_pnl_inr", 0),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase232_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase232_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase232_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase232_next_best_action", ""),
        }
    if phase == 233:
        complete = as_int(metric_value(path, "phase233_fragility_realism_validation_complete", 0))
        passed = as_int(metric_value(path, "phase233_fragility_realism_pass", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "phase232_candidate_passed_fragility_realism_validation" if passed else ("phase232_candidate_failed_fragility_realism_validation" if complete else "fragility_realism_validation_gated"),
            "fragility_realism_validation_complete": complete,
            "phase232_survivor_rows": as_int(metric_value(path, "phase233_phase232_survivor_rows", 0)),
            "parent_candidate_id": metric_value(path, "phase233_parent_candidate_id", ""),
            "neighbor_candidate_rows": as_int(metric_value(path, "phase233_neighbor_candidate_rows", 0)),
            "neighbor_pass_rows": as_int(metric_value(path, "phase233_neighbor_pass_rows", 0)),
            "parent_test_2x_cost_net_pnl_inr": metric_value(path, "phase233_parent_test_2x_cost_net_pnl_inr", 0),
            "gate_pass_rows": as_int(metric_value(path, "phase233_gate_pass_rows", 0)),
            "gate_rows": as_int(metric_value(path, "phase233_gate_rows", 0)),
            "fragility_realism_pass": passed,
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase233_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase233_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase233_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase233_next_best_action", ""),
        }
    if phase == 234:
        complete = as_int(metric_value(path, "phase234_holdout_preparation_complete", 0))
        route_ready = as_int(metric_value(path, "phase234_real_anchor_route_ready", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "phase233_candidate_prepared_for_real_anchor_adapter" if route_ready else ("phase233_candidate_prepared_for_sealed_holdout" if complete else "holdout_preparation_gated"),
            "holdout_preparation_complete": complete,
            "parent_candidate_id": metric_value(path, "phase234_parent_candidate_id", ""),
            "phase233_fragility_realism_pass": as_int(metric_value(path, "phase234_phase233_fragility_realism_pass", 0)),
            "required_schema_rows": as_int(metric_value(path, "phase234_required_schema_rows", 0)),
            "required_schema_present_rows": as_int(metric_value(path, "phase234_required_schema_present_rows", 0)),
            "real_anchor_route_ready": route_ready,
            "selected_route_id": metric_value(path, "phase234_selected_route_id", ""),
            "phase235_work_order_rows": as_int(metric_value(path, "phase234_phase235_work_order_rows", 0)),
            "gate_pass_rows": as_int(metric_value(path, "phase234_hard_gate_pass_rows", 0)),
            "gate_rows": as_int(metric_value(path, "phase234_hard_gate_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase234_strategy_replay_execution_allowed_now", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase234_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase234_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase234_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase234_next_best_action", ""),
        }
    if phase == 235:
        complete = as_int(metric_value(path, "phase235_real_anchor_microprice_replay_complete", 0))
        real_pass = as_int(metric_value(path, "phase235_real_anchor_replay_pass", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "phase233_candidate_passed_real_anchor_adapter" if real_pass else ("phase233_candidate_failed_real_anchor_breadth_on_adapter" if complete else "real_anchor_adapter_replay_gated"),
            "real_anchor_microprice_replay_complete": complete,
            "parent_candidate_id": metric_value(path, "phase235_parent_candidate_id", ""),
            "source_feature_rows": as_int(metric_value(path, "phase235_source_feature_rows", 0)),
            "real_event_bar_rows": as_int(metric_value(path, "phase235_real_event_bar_rows", 0)),
            "real_anchor_trade_rows": as_int(metric_value(path, "phase235_real_anchor_trade_rows", 0)),
            "real_anchor_net_pnl_inr": metric_value(path, "phase235_real_anchor_net_pnl_inr", 0),
            "real_anchor_dates": as_int(metric_value(path, "phase235_real_anchor_dates", 0)),
            "real_anchor_symbols": as_int(metric_value(path, "phase235_real_anchor_symbols", 0)),
            "control_pass_rows": as_int(metric_value(path, "phase235_control_pass_rows", 0)),
            "control_rows": as_int(metric_value(path, "phase235_control_rows", 0)),
            "gate_pass_rows": as_int(metric_value(path, "phase235_hard_gate_pass_rows", 0)),
            "gate_rows": as_int(metric_value(path, "phase235_hard_gate_rows", 0)),
            "real_anchor_replay_pass": real_pass,
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase235_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase235_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase235_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase235_next_best_action", ""),
        }
    if phase == 236:
        complete = as_int(metric_value(path, "phase236_real_anchor_neighbor_search_complete", 0))
        search_pass = as_int(metric_value(path, "phase236_real_anchor_neighbor_search_pass", 0))
        positive = as_int(metric_value(path, "phase236_positive_real_anchor_variant_rows", 0))
        breadth = as_int(metric_value(path, "phase236_breadth_passing_variant_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "real_anchor_neighbor_positive_breadth_candidate_found" if search_pass else ("real_anchor_neighbor_positive_pockets_breadth_failed" if complete and positive > 0 else ("real_anchor_neighbor_search_no_positive_variants" if complete else "real_anchor_neighbor_search_gated")),
            "real_anchor_neighbor_search_complete": complete,
            "neighbor_variant_rows": as_int(metric_value(path, "phase236_neighbor_variant_rows", 0)),
            "positive_real_anchor_variant_rows": positive,
            "breadth_passing_variant_rows": breadth,
            "best_candidate_id": metric_value(path, "phase236_best_candidate_id", ""),
            "best_real_anchor_net_pnl_inr": metric_value(path, "phase236_best_real_anchor_net_pnl_inr", 0),
            "best_real_anchor_trade_rows": as_int(metric_value(path, "phase236_best_real_anchor_trade_rows", 0)),
            "best_real_anchor_dates": as_int(metric_value(path, "phase236_best_real_anchor_dates", 0)),
            "best_real_anchor_symbols": as_int(metric_value(path, "phase236_best_real_anchor_symbols", 0)),
            "gate_pass_rows": as_int(metric_value(path, "phase236_hard_gate_pass_rows", 0)),
            "gate_rows": as_int(metric_value(path, "phase236_hard_gate_rows", 0)),
            "real_anchor_neighbor_search_pass": search_pass,
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase236_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase236_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase236_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase236_next_best_action", ""),
        }
    if phase == 237:
        complete = as_int(metric_value(path, "phase237_threshold_transfer_search_complete", 0))
        opened = as_int(metric_value(path, "phase237_candidate_opened_for_phase238", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "real_anchor_threshold_transfer_candidate_opened_for_validation" if opened else ("real_anchor_threshold_transfer_search_failed" if complete else "real_anchor_threshold_transfer_search_gated"),
            "threshold_transfer_search_complete": complete,
            "expanded_variant_rows": as_int(metric_value(path, "phase237_expanded_variant_rows", 0)),
            "positive_variant_rows": as_int(metric_value(path, "phase237_positive_variant_rows", 0)),
            "breadth_positive_candidate_rows": as_int(metric_value(path, "phase237_breadth_positive_candidate_rows", 0)),
            "best_candidate_id": metric_value(path, "phase237_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase237_best_family_id", ""),
            "best_real_anchor_net_pnl_inr": metric_value(path, "phase237_best_real_anchor_net_pnl_inr", 0),
            "best_real_anchor_trade_rows": as_int(metric_value(path, "phase237_best_real_anchor_trade_rows", 0)),
            "best_real_anchor_dates": as_int(metric_value(path, "phase237_best_real_anchor_dates", 0)),
            "best_real_anchor_symbols": as_int(metric_value(path, "phase237_best_real_anchor_symbols", 0)),
            "best_control_pass_rows": as_int(metric_value(path, "phase237_best_control_pass_rows", 0)),
            "best_control_rows": as_int(metric_value(path, "phase237_best_control_rows", 0)),
            "gate_pass_rows": as_int(metric_value(path, "phase237_hard_gate_pass_rows", 0)),
            "gate_rows": as_int(metric_value(path, "phase237_hard_gate_rows", 0)),
            "candidate_opened_for_phase238": opened,
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase237_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase237_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase237_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase237_next_best_action", ""),
        }
    if phase == 238:
        complete = as_int(metric_value(path, "phase238_validation_precommit_complete", 0))
        unseen_available = as_int(metric_value(path, "phase238_local_unseen_validation_dates_available", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "phase237_candidate_validation_precommitted_unseen_dates_needed" if complete and unseen_available == 0 else ("phase237_candidate_validation_precommitted_unseen_dates_available" if complete else "phase237_validation_precommit_gated"),
            "validation_precommit_complete": complete,
            "candidate_id": metric_value(path, "phase238_candidate_id", ""),
            "phase237_net_pnl_inr": metric_value(path, "phase238_phase237_net_pnl_inr", 0),
            "phase237_trade_rows": as_int(metric_value(path, "phase238_phase237_trade_rows", 0)),
            "phase237_dates": as_int(metric_value(path, "phase238_phase237_dates", 0)),
            "phase237_symbols": as_int(metric_value(path, "phase238_phase237_symbols", 0)),
            "primary_validation_contract_rows": as_int(metric_value(path, "phase238_primary_validation_contract_rows", 0)),
            "walk_forward_diagnostic_contract_rows": as_int(metric_value(path, "phase238_walk_forward_diagnostic_contract_rows", 0)),
            "local_unseen_validation_dates_available": unseen_available,
            "min_unseen_validation_dates_required": as_int(metric_value(path, "phase238_min_unseen_validation_dates_required", 0)),
            "phase239_work_order_rows": as_int(metric_value(path, "phase238_phase239_work_order_rows", 0)),
            "gate_pass_rows": as_int(metric_value(path, "phase238_hard_gate_pass_rows", 0)),
            "gate_rows": as_int(metric_value(path, "phase238_hard_gate_rows", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase238_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase238_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase238_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase238_next_best_action", ""),
        }
    if phase == 239:
        complete = as_int(metric_value(path, "phase239_unseen_date_acquisition_audit_complete", 0))
        azure_ready = as_int(metric_value(path, "phase239_azure_storage_listing_ready", 0))
        local_unseen = as_int(metric_value(path, "phase239_local_unseen_candidate_dates", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "unseen_real_l2_dates_available_for_download" if complete and azure_ready else ("unseen_real_l2_download_preflight_blocked" if complete else "unseen_date_acquisition_audit_gated"),
            "unseen_date_acquisition_audit_complete": complete,
            "local_unseen_candidate_dates": local_unseen,
            "min_unseen_validation_dates_required": as_int(metric_value(path, "phase239_min_unseen_validation_dates_required", 0)),
            "target_unseen_date_rows": as_int(metric_value(path, "phase239_target_unseen_date_rows", 0)),
            "az_cli_available": as_int(metric_value(path, "phase239_az_cli_available", 0)),
            "azcopy_available": as_int(metric_value(path, "phase239_azcopy_available", 0)),
            "azure_storage_listing_ready": azure_ready,
            "download_plan_rows": as_int(metric_value(path, "phase239_download_plan_rows", 0)),
            "gate_pass_rows": as_int(metric_value(path, "phase239_hard_gate_pass_rows", 0)),
            "gate_rows": as_int(metric_value(path, "phase239_hard_gate_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase239_validation_execution_allowed_now", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase239_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase239_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase239_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase239_next_best_action", ""),
        }
    if phase == 240:
        complete = as_int(metric_value(path, "phase240_unseen_raw_l2_download_complete", 0))
        partial = as_int(metric_value(path, "phase240_partial_attempt", 0))
        completed_files = as_int(metric_value(path, "phase240_completed_files", 0))
        failed_files = as_int(metric_value(path, "phase240_failed_files", 0))
        completed_dates = as_int(metric_value(path, "phase240_completed_dates", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "unseen_raw_l2_download_complete_ready_for_materialization" if complete else ("unseen_raw_l2_download_partial_or_in_progress" if partial or completed_files > 0 else "unseen_raw_l2_download_gated"),
            "unseen_raw_l2_download_complete": complete,
            "partial_attempt": partial,
            "target_trade_dates": metric_value(path, "phase240_target_trade_dates", ""),
            "remote_manifest_files": as_int(metric_value(path, "phase240_remote_manifest_files", 0)),
            "remote_manifest_bytes": as_int(metric_value(path, "phase240_remote_manifest_bytes", 0)),
            "completed_files": completed_files,
            "failed_files": failed_files,
            "completed_dates": completed_dates,
            "strategy_replay_allowed": as_int(metric_value(path, "phase240_validation_execution_allowed_now", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase240_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase240_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase240_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase240_next_best_action", ""),
        }
    if phase == 241:
        survived = as_int(metric_value(path, "phase241_one_date_diagnostic_candidate_survived", 0))
        complete = as_int(metric_value(path, "phase241_one_date_unseen_diagnostic_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "one_date_unseen_diagnostic_positive_but_fragile" if complete and not survived else ("one_date_unseen_diagnostic_survived_not_acceptance" if survived else "one_date_unseen_diagnostic_gated"),
            "one_date_unseen_diagnostic_complete": complete,
            "candidate_id": metric_value(path, "phase241_candidate_id", ""),
            "trade_date": metric_value(path, "phase241_trade_date", ""),
            "source_feature_rows_15s": as_int(metric_value(path, "phase241_source_feature_rows_15s", 0)),
            "real_event_bar_rows": as_int(metric_value(path, "phase241_real_event_bar_rows", 0)),
            "raw_symbols": as_int(metric_value(path, "phase241_raw_symbols", 0)),
            "raw_parquet_files": as_int(metric_value(path, "phase241_raw_parquet_files", 0)),
            "trade_rows": as_int(metric_value(path, "phase241_trade_rows", 0)),
            "net_pnl_inr": metric_value(path, "phase241_net_pnl_inr", 0),
            "symbols": as_int(metric_value(path, "phase241_symbols", 0)),
            "control_pass_rows": as_int(metric_value(path, "phase241_control_pass_rows", 0)),
            "control_rows": as_int(metric_value(path, "phase241_control_rows", 0)),
            "diagnostic_gate_pass_rows": as_int(metric_value(path, "phase241_diagnostic_gate_pass_rows", 0)),
            "diagnostic_gate_rows": as_int(metric_value(path, "phase241_diagnostic_gate_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase241_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase241_hard_gate_rows", 0)),
            "one_date_diagnostic_candidate_survived": survived,
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase241_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase241_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase241_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase241_next_best_action", ""),
        }
    if phase == 242:
        complete = as_int(metric_value(path, "phase242_closure_or_redesign_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "phase237_candidate_closed_redesign_queue_opened" if complete else "phase242_closure_redesign_gated",
            "closure_or_redesign_complete": complete,
            "closed_candidate_id": metric_value(path, "phase242_closed_candidate_id", ""),
            "one_date_net_pnl_inr": metric_value(path, "phase242_one_date_net_pnl_inr", 0),
            "control_pass_rows": as_int(metric_value(path, "phase242_control_pass_rows", 0)),
            "control_rows": as_int(metric_value(path, "phase242_control_rows", 0)),
            "redesign_queue_rows": as_int(metric_value(path, "phase242_redesign_queue_rows", 0)),
            "download_more_dates_for_closed_candidate_allowed": as_int(metric_value(path, "phase242_download_more_dates_for_closed_candidate_allowed", 0)),
            "holdout_parameter_tuning_allowed": as_int(metric_value(path, "phase242_holdout_parameter_tuning_allowed", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase242_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase242_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase242_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase242_next_best_action", ""),
        }
    if phase == 243:
        complete = as_int(metric_value(path, "phase243_cost_stress_first_redesign_complete", 0))
        survivors = as_int(metric_value(path, "phase243_survivor_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_stress_first_redesign_candidate_found_future_holdout_precommit_open" if complete and survivors > 0 else ("cost_stress_first_redesign_no_survivors" if complete else "phase243_redesign_gated"),
            "cost_stress_first_redesign_complete": complete,
            "expanded_variant_rows": as_int(metric_value(path, "phase243_expanded_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase243_cost200_positive_variant_rows", 0)),
            "controlled_candidate_rows": as_int(metric_value(path, "phase243_controlled_candidate_rows", 0)),
            "survivor_candidate_rows": survivors,
            "best_candidate_id": metric_value(path, "phase243_best_candidate_id", ""),
            "best_training_net_pnl_inr": metric_value(path, "phase243_best_training_net_pnl_inr", 0),
            "best_cost200_net_pnl_inr": metric_value(path, "phase243_best_cost200_net_pnl_inr", 0),
            "best_random_beat_fraction": metric_value(path, "phase243_best_random_beat_fraction", 0),
            "best_trade_rows": as_int(metric_value(path, "phase243_best_trade_rows", 0)),
            "best_dates": as_int(metric_value(path, "phase243_best_dates", 0)),
            "best_symbols": as_int(metric_value(path, "phase243_best_symbols", 0)),
            "future_holdout_precommit_allowed": as_int(metric_value(path, "phase243_future_holdout_precommit_allowed", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase243_download_more_dates_now_allowed", 0)),
            "holdout_parameter_tuning_allowed": as_int(metric_value(path, "phase243_holdout_parameter_tuning_allowed", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase243_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase243_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase243_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase243_next_best_action", ""),
        }
    if phase == 244:
        complete = as_int(metric_value(path, "phase244_future_holdout_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "future_holdout_precommitted_storage_decision_required" if complete else "phase244_precommit_gated",
            "future_holdout_precommit_complete": complete,
            "candidate_id": metric_value(path, "phase244_candidate_id", ""),
            "best_training_net_pnl_inr": metric_value(path, "phase244_best_training_net_pnl_inr", 0),
            "best_cost200_net_pnl_inr": metric_value(path, "phase244_best_cost200_net_pnl_inr", 0),
            "best_random_beat_fraction": metric_value(path, "phase244_best_random_beat_fraction", 0),
            "min_holdout_dates_required": as_int(metric_value(path, "phase244_min_holdout_dates_required", 0)),
            "target_holdout_dates": as_int(metric_value(path, "phase244_target_holdout_dates", 0)),
            "min_holdout_trades_required": as_int(metric_value(path, "phase244_min_holdout_trades_required", 0)),
            "min_holdout_symbols_required": as_int(metric_value(path, "phase244_min_holdout_symbols_required", 0)),
            "storage_decision_required": as_int(metric_value(path, "phase244_storage_decision_required", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase244_download_more_dates_now_allowed", 0)),
            "holdout_parameter_tuning_allowed": as_int(metric_value(path, "phase244_holdout_parameter_tuning_allowed", 0)),
            "future_holdout_execution_allowed_now": as_int(metric_value(path, "phase244_future_holdout_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase244_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase244_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase244_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase244_next_best_action", ""),
        }
    if phase == 245:
        complete = as_int(metric_value(path, "phase245_storage_decision_audit_complete", 0))
        feasible = as_int(metric_value(path, "phase245_local_download_feasible_by_space_only", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "storage_audit_local_space_feasible_policy_choice_required" if complete and feasible else ("storage_audit_external_or_cleanup_required" if complete else "phase245_storage_audit_gated"),
            "storage_decision_audit_complete": complete,
            "free_gb_now": metric_value(path, "phase245_free_gb_now", 0),
            "inventory_rows": as_int(metric_value(path, "phase245_inventory_rows", 0)),
            "cleanup_candidate_rows": as_int(metric_value(path, "phase245_cleanup_candidate_rows", 0)),
            "target_holdout_dates": as_int(metric_value(path, "phase245_target_holdout_dates", 0)),
            "projected_required_gb": metric_value(path, "phase245_projected_required_gb", 0),
            "projected_free_gb_after_target": metric_value(path, "phase245_projected_free_gb_after_target", 0),
            "local_download_feasible_by_space_only": feasible,
            "destructive_cleanup_allowed_now": as_int(metric_value(path, "phase245_destructive_cleanup_allowed_now", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase245_download_more_dates_now_allowed", 0)),
            "holdout_execution_allowed_now": as_int(metric_value(path, "phase245_holdout_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase245_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase245_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase245_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase245_next_best_action", ""),
        }
    if phase == 246:
        complete = as_int(metric_value(path, "phase246_fresh_one_date_holdout_diagnostic_complete", 0))
        survived = as_int(metric_value(path, "phase246_one_date_diagnostic_candidate_survived", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "phase244_candidate_failed_one_fresh_date_diagnostic_redesign_required" if complete and not survived else ("phase244_candidate_survived_one_fresh_date_continue_date_by_date" if complete else "phase246_fresh_one_date_diagnostic_gated"),
            "fresh_one_date_holdout_diagnostic_complete": complete,
            "trade_date": metric_value(path, "phase246_trade_date", ""),
            "candidate_id": metric_value(path, "phase246_candidate_id", ""),
            "raw_parquet_files": as_int(metric_value(path, "phase246_raw_parquet_files", 0)),
            "source_feature_rows_15s": as_int(metric_value(path, "phase246_source_feature_rows_15s", 0)),
            "real_event_bar_rows": as_int(metric_value(path, "phase246_real_event_bar_rows", 0)),
            "trade_rows": as_int(metric_value(path, "phase246_trade_rows", 0)),
            "net_pnl_inr": metric_value(path, "phase246_net_pnl_inr", 0),
            "symbols": as_int(metric_value(path, "phase246_symbols", 0)),
            "control_pass_rows": as_int(metric_value(path, "phase246_control_pass_rows", 0)),
            "control_rows": as_int(metric_value(path, "phase246_control_rows", 0)),
            "diagnostic_gate_pass_rows": as_int(metric_value(path, "phase246_diagnostic_gate_pass_rows", 0)),
            "diagnostic_gate_rows": as_int(metric_value(path, "phase246_diagnostic_gate_rows", 0)),
            "one_date_diagnostic_candidate_survived": survived,
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase246_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase246_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase246_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase246_next_best_action", ""),
        }
    if phase == 247:
        complete = as_int(metric_value(path, "phase247_l2_imbalance_regime_filter_redesign_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "l2_imbalance_regime_filter_training_search_precommitted" if complete else "phase247_redesign_precommit_gated",
            "l2_imbalance_regime_filter_redesign_precommit_complete": complete,
            "parent_candidate_id": metric_value(path, "phase247_parent_candidate_id", ""),
            "failure_attribution_rows": as_int(metric_value(path, "phase247_failure_attribution_rows", 0)),
            "feature_filter_rows": as_int(metric_value(path, "phase247_feature_filter_rows", 0)),
            "redesign_candidate_rows": as_int(metric_value(path, "phase247_redesign_candidate_rows", 0)),
            "acceptance_contract_rows": as_int(metric_value(path, "phase247_acceptance_contract_rows", 0)),
            "forbidden_tuning_dates": metric_value(path, "phase247_forbidden_tuning_dates", ""),
            "l2_imbalance_filter_required": as_int(metric_value(path, "phase247_l2_imbalance_filter_required", 0)),
            "range_or_market_veto_required": as_int(metric_value(path, "phase247_range_or_market_veto_required", 0)),
            "cost_stress_first_objective": as_int(metric_value(path, "phase247_cost_stress_first_objective", 0)),
            "training_search_allowed_next": as_int(metric_value(path, "phase247_training_search_allowed_next", 0)),
            "holdout_execution_allowed_now": as_int(metric_value(path, "phase247_holdout_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase247_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase247_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase247_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase247_next_best_action", ""),
        }
    if phase == 248:
        complete = as_int(metric_value(path, "phase248_l2_imbalance_regime_filtered_search_complete", 0))
        survivors = as_int(metric_value(path, "phase248_survivor_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "l2_imbalance_regime_filtered_search_no_survivor_broaden_or_close" if complete and survivors == 0 else ("l2_imbalance_regime_filtered_candidate_found_future_holdout_precommit_open" if complete else "phase248_search_gated"),
            "l2_imbalance_regime_filtered_search_complete": complete,
            "training_event_bar_rows": as_int(metric_value(path, "phase248_training_event_bar_rows", 0)),
            "training_dates": as_int(metric_value(path, "phase248_training_dates", 0)),
            "training_symbols": as_int(metric_value(path, "phase248_training_symbols", 0)),
            "forbidden_tuning_dates": metric_value(path, "phase248_forbidden_tuning_dates", ""),
            "variant_rows": as_int(metric_value(path, "phase248_variant_rows", 0)),
            "l2_filtered_variant_rows": as_int(metric_value(path, "phase248_l2_filtered_variant_rows", 0)),
            "net_positive_variant_rows": as_int(metric_value(path, "phase248_net_positive_variant_rows", 0)),
            "cost150_positive_variant_rows": as_int(metric_value(path, "phase248_cost150_positive_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase248_cost200_positive_variant_rows", 0)),
            "controlled_candidate_rows": as_int(metric_value(path, "phase248_controlled_candidate_rows", 0)),
            "survivor_candidate_rows": survivors,
            "best_candidate_id": metric_value(path, "phase248_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase248_best_family_id", ""),
            "best_training_net_pnl_inr": metric_value(path, "phase248_best_training_net_pnl_inr", 0),
            "best_cost200_net_pnl_inr": metric_value(path, "phase248_best_cost200_net_pnl_inr", 0),
            "best_random_beat_fraction": metric_value(path, "phase248_best_random_beat_fraction", 0),
            "best_trade_rows": as_int(metric_value(path, "phase248_best_trade_rows", 0)),
            "best_dates": as_int(metric_value(path, "phase248_best_dates", 0)),
            "best_symbols": as_int(metric_value(path, "phase248_best_symbols", 0)),
            "future_holdout_precommit_allowed": as_int(metric_value(path, "phase248_future_holdout_precommit_allowed", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase248_download_more_dates_now_allowed", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase248_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase248_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase248_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase248_next_best_action", ""),
        }
    if phase == 249:
        complete = as_int(metric_value(path, "phase249_close_or_broaden_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "single_name_reversal_closed_pair_basket_precommit_open" if complete else "phase249_close_or_broaden_gated",
            "close_or_broaden_complete": complete,
            "closed_scope": metric_value(path, "phase249_closed_scope", ""),
            "phase248_variant_rows": as_int(metric_value(path, "phase249_phase248_variant_rows", 0)),
            "phase248_cost200_positive_rows": as_int(metric_value(path, "phase249_phase248_cost200_positive_rows", 0)),
            "phase248_survivor_rows": as_int(metric_value(path, "phase249_phase248_survivor_rows", 0)),
            "closure_rows": as_int(metric_value(path, "phase249_closure_rows", 0)),
            "failure_attribution_rows": as_int(metric_value(path, "phase249_failure_attribution_rows", 0)),
            "broaden_queue_rows": as_int(metric_value(path, "phase249_broaden_queue_rows", 0)),
            "selected_next_route": metric_value(path, "phase249_selected_next_route", ""),
            "threshold_relaxation_only_allowed": as_int(metric_value(path, "phase249_threshold_relaxation_only_allowed", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase249_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase249_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase249_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase249_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase249_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase249_next_best_action", ""),
        }
    if phase == 250:
        complete = as_int(metric_value(path, "phase250_pair_basket_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "pair_basket_relative_value_training_search_precommitted" if complete else "phase250_pair_basket_precommit_gated",
            "pair_basket_precommit_complete": complete,
            "selected_route": metric_value(path, "phase250_selected_route", ""),
            "training_event_bar_rows": as_int(metric_value(path, "phase250_training_event_bar_rows", 0)),
            "training_dates": as_int(metric_value(path, "phase250_training_dates", 0)),
            "training_symbols": as_int(metric_value(path, "phase250_training_symbols", 0)),
            "forbidden_tuning_dates": metric_value(path, "phase250_forbidden_tuning_dates", ""),
            "pair_group_rows": as_int(metric_value(path, "phase250_pair_group_rows", 0)),
            "grouped_symbols": as_int(metric_value(path, "phase250_grouped_symbols", 0)),
            "candidate_family_rows": as_int(metric_value(path, "phase250_candidate_family_rows", 0)),
            "feature_contract_rows": as_int(metric_value(path, "phase250_feature_contract_rows", 0)),
            "required_input_features_present": as_int(metric_value(path, "phase250_required_input_features_present", 0)),
            "acceptance_contract_rows": as_int(metric_value(path, "phase250_acceptance_contract_rows", 0)),
            "phase251_training_search_allowed_next": as_int(metric_value(path, "phase250_phase251_training_search_allowed_next", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase250_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase250_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase250_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase250_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase250_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase250_next_best_action", ""),
        }
    if phase == 251:
        complete = as_int(metric_value(path, "phase251_pair_basket_search_complete", 0))
        survivors = as_int(metric_value(path, "phase251_survivor_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "pair_basket_relative_value_no_survivor_broaden_or_close" if complete and survivors == 0 else ("pair_basket_relative_value_candidate_found_future_holdout_precommit_open" if complete else "phase251_pair_basket_search_gated"),
            "pair_basket_search_complete": complete,
            "training_event_bar_rows": as_int(metric_value(path, "phase251_training_event_bar_rows", 0)),
            "training_dates": as_int(metric_value(path, "phase251_training_dates", 0)),
            "training_symbols": as_int(metric_value(path, "phase251_training_symbols", 0)),
            "forbidden_tuning_dates": metric_value(path, "phase251_forbidden_tuning_dates", ""),
            "variant_rows": as_int(metric_value(path, "phase251_variant_rows", 0)),
            "full_top_five_depth_variant_rows": as_int(metric_value(path, "phase251_full_top_five_depth_variant_rows", 0)),
            "depth_beyond_l1_variant_rows": as_int(metric_value(path, "phase251_depth_beyond_l1_variant_rows", 0)),
            "net_positive_variant_rows": as_int(metric_value(path, "phase251_net_positive_variant_rows", 0)),
            "cost150_positive_variant_rows": as_int(metric_value(path, "phase251_cost150_positive_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase251_cost200_positive_variant_rows", 0)),
            "controlled_candidate_rows": as_int(metric_value(path, "phase251_controlled_candidate_rows", 0)),
            "survivor_candidate_rows": survivors,
            "best_candidate_id": metric_value(path, "phase251_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase251_best_family_id", ""),
            "best_training_net_pnl_inr": metric_value(path, "phase251_best_training_net_pnl_inr", 0),
            "best_cost200_net_pnl_inr": metric_value(path, "phase251_best_cost200_net_pnl_inr", 0),
            "best_trade_rows": as_int(metric_value(path, "phase251_best_trade_rows", 0)),
            "future_holdout_precommit_allowed": as_int(metric_value(path, "phase251_future_holdout_precommit_allowed", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase251_download_more_dates_now_allowed", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase251_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase251_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase251_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase251_next_best_action", ""),
        }
    if phase == 252:
        complete = as_int(metric_value(path, "phase252_close_or_broaden_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "aggregate_pair_basket_closed_richer_raw_depth_precommit_open" if complete else "phase252_close_or_broaden_gated",
            "close_or_broaden_complete": complete,
            "closed_scope": metric_value(path, "phase252_closed_scope", ""),
            "phase251_variant_rows": as_int(metric_value(path, "phase252_phase251_variant_rows", 0)),
            "phase251_base_positive_rows": as_int(metric_value(path, "phase252_phase251_base_positive_rows", 0)),
            "phase251_cost200_positive_rows": as_int(metric_value(path, "phase252_phase251_cost200_positive_rows", 0)),
            "phase251_survivor_rows": as_int(metric_value(path, "phase252_phase251_survivor_rows", 0)),
            "raw_depth_schema_present_rows": as_int(metric_value(path, "phase252_raw_depth_schema_present_rows", 0)),
            "raw_depth_schema_rows": as_int(metric_value(path, "phase252_raw_depth_schema_rows", 0)),
            "closure_rows": as_int(metric_value(path, "phase252_closure_rows", 0)),
            "failure_attribution_rows": as_int(metric_value(path, "phase252_failure_attribution_rows", 0)),
            "broaden_queue_rows": as_int(metric_value(path, "phase252_broaden_queue_rows", 0)),
            "selected_next_route": metric_value(path, "phase252_selected_next_route", ""),
            "threshold_relaxation_only_allowed": as_int(metric_value(path, "phase252_threshold_relaxation_only_allowed", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase252_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase252_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase252_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase252_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase252_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase252_next_best_action", ""),
        }
    if phase == 253:
        complete = as_int(metric_value(path, "phase253_richer_raw_depth_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "richer_raw_top5_depth_materialization_precommitted" if complete else "phase253_richer_raw_depth_precommit_gated",
            "richer_raw_depth_precommit_complete": complete,
            "raw_root_rows": as_int(metric_value(path, "phase253_raw_root_rows", 0)),
            "usable_raw_root_rows": as_int(metric_value(path, "phase253_usable_raw_root_rows", 0)),
            "schema_present_rows": as_int(metric_value(path, "phase253_schema_present_rows", 0)),
            "schema_rows": as_int(metric_value(path, "phase253_schema_rows", 0)),
            "raw_depth_level_columns": as_int(metric_value(path, "phase253_raw_depth_level_columns", 0)),
            "feature_catalog_rows": as_int(metric_value(path, "phase253_feature_catalog_rows", 0)),
            "materialization_contract_rows": as_int(metric_value(path, "phase253_materialization_contract_rows", 0)),
            "phase254_materialization_allowed_next": as_int(metric_value(path, "phase253_phase254_materialization_allowed_next", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase253_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase253_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase253_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase253_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase253_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase253_next_best_action", ""),
        }
    if phase == 254:
        complete = as_int(metric_value(path, "phase254_richer_raw_depth_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "richer_raw_top5_depth_materialized_quality_interpretation_open" if complete else "phase254_richer_raw_depth_materialization_gated",
            "richer_raw_depth_materialization_complete": complete,
            "raw_root_used": metric_value(path, "phase254_raw_root_used", ""),
            "events_per_bar": as_int(metric_value(path, "phase254_events_per_bar", 0)),
            "max_files_per_symbol": as_int(metric_value(path, "phase254_max_files_per_symbol", 0)),
            "source_parquet_files_read": as_int(metric_value(path, "phase254_source_parquet_files_read", 0)),
            "excluded_invalid_source_tick_rows": as_int(metric_value(path, "phase254_excluded_invalid_source_tick_rows", 0)),
            "event_bar_rows": as_int(metric_value(path, "phase254_event_bar_rows", 0)),
            "trade_dates": as_int(metric_value(path, "phase254_trade_dates", 0)),
            "symbols": as_int(metric_value(path, "phase254_symbols", 0)),
            "source_tick_rows": as_int(metric_value(path, "phase254_source_tick_rows", 0)),
            "crossed_or_locked_tick_rows": as_int(metric_value(path, "phase254_crossed_or_locked_tick_rows", 0)),
            "nonpositive_depth_tick_rows": as_int(metric_value(path, "phase254_nonpositive_depth_tick_rows", 0)),
            "missing_level_tick_rows": as_int(metric_value(path, "phase254_missing_level_tick_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase254_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase254_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase254_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase254_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase254_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase254_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase254_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase254_next_best_action", ""),
        }
    if phase == 255:
        complete = as_int(metric_value(path, "phase255_feature_quality_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "richer_raw_top5_depth_quality_passed_strategy_search_open" if complete else "phase255_richer_raw_depth_quality_gated",
            "feature_quality_interpretation_complete": complete,
            "input_event_bar_rows": as_int(metric_value(path, "phase255_input_event_bar_rows", 0)),
            "trade_dates": as_int(metric_value(path, "phase255_trade_dates", 0)),
            "symbols": as_int(metric_value(path, "phase255_symbols", 0)),
            "source_tick_rows": as_int(metric_value(path, "phase255_source_tick_rows", 0)),
            "feature_rows": as_int(metric_value(path, "phase255_feature_rows", 0)),
            "full_depth_feature_rows": as_int(metric_value(path, "phase255_full_depth_feature_rows", 0)),
            "healthy_feature_rows": as_int(metric_value(path, "phase255_healthy_feature_rows", 0)),
            "healthy_full_depth_feature_rows": as_int(metric_value(path, "phase255_healthy_full_depth_feature_rows", 0)),
            "max_abs_spearman_ic": metric_value(path, "phase255_max_abs_spearman_ic", ""),
            "max_abs_full_depth_spearman_ic": metric_value(path, "phase255_max_abs_full_depth_spearman_ic", ""),
            "top_full_depth_feature": metric_value(path, "phase255_top_full_depth_feature", ""),
            "top_full_depth_label": metric_value(path, "phase255_top_full_depth_label", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase255_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase255_hard_gate_rows", 0)),
            "strategy_search_allowed_next": as_int(metric_value(path, "phase255_strategy_search_allowed_next", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase255_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase255_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase255_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase255_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase255_next_best_action", ""),
        }
    if phase == 256:
        complete = as_int(metric_value(path, "phase256_strategy_search_complete", 0))
        survivor_rows = as_int(metric_value(path, "phase256_survivor_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "richer_raw_top5_depth_taker_search_no_survivor_interpretation_open" if complete and survivor_rows == 0 else "richer_raw_top5_depth_training_candidate_interpretation_open",
            "strategy_search_complete": complete,
            "input_event_bar_rows": as_int(metric_value(path, "phase256_input_event_bar_rows", 0)),
            "symbols": as_int(metric_value(path, "phase256_symbols", 0)),
            "trade_dates": as_int(metric_value(path, "phase256_trade_dates", 0)),
            "variant_rows": as_int(metric_value(path, "phase256_variant_rows", 0)),
            "full_top_five_depth_variant_rows": as_int(metric_value(path, "phase256_full_top_five_depth_variant_rows", 0)),
            "depth_beyond_l1_variant_rows": as_int(metric_value(path, "phase256_depth_beyond_l1_variant_rows", 0)),
            "cost100_positive_variant_rows": as_int(metric_value(path, "phase256_cost100_positive_variant_rows", 0)),
            "cost150_positive_variant_rows": as_int(metric_value(path, "phase256_cost150_positive_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase256_cost200_positive_variant_rows", 0)),
            "survivor_candidate_rows": survivor_rows,
            "best_candidate_id": metric_value(path, "phase256_best_candidate_id", ""),
            "best_feature": metric_value(path, "phase256_best_feature", ""),
            "best_cost100_net_pnl_inr": metric_value(path, "phase256_best_cost100_net_pnl_inr", ""),
            "best_cost200_net_pnl_inr": metric_value(path, "phase256_best_cost200_net_pnl_inr", ""),
            "best_trade_rows": as_int(metric_value(path, "phase256_best_trade_rows", 0)),
            "best_symbols": as_int(metric_value(path, "phase256_best_symbols", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase256_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase256_hard_gate_rows", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase256_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase256_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase256_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase256_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase256_next_best_action", ""),
        }
    if phase == 257:
        complete = as_int(metric_value(path, "phase257_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_queue_aware_spread_capture_precommit_open" if complete else "phase257_interpretation_gated",
            "interpretation_complete": complete,
            "phase256_variant_rows": as_int(metric_value(path, "phase257_phase256_variant_rows", 0)),
            "phase256_full_depth_variant_rows": as_int(metric_value(path, "phase257_phase256_full_depth_variant_rows", 0)),
            "phase256_survivor_candidate_rows": as_int(metric_value(path, "phase257_phase256_survivor_candidate_rows", 0)),
            "phase256_cost100_positive_variant_rows": as_int(metric_value(path, "phase257_phase256_cost100_positive_variant_rows", 0)),
            "closed_taker_threshold_route": as_int(metric_value(path, "phase257_closed_taker_threshold_route", 0)),
            "full_top_five_depth_preserved": as_int(metric_value(path, "phase257_full_top_five_depth_preserved", 0)),
            "threshold_relaxation_only_allowed": as_int(metric_value(path, "phase257_threshold_relaxation_only_allowed", 0)),
            "selected_next_route": metric_value(path, "phase257_selected_next_route", ""),
            "next_route_contract_rows": as_int(metric_value(path, "phase257_next_route_contract_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase257_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase257_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase257_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase257_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase257_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase257_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase257_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase257_next_best_action", ""),
        }
    if phase == 258:
        complete = as_int(metric_value(path, "phase258_passive_queue_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_queue_aware_spread_capture_training_search_open" if complete else "phase258_passive_queue_precommit_gated",
            "passive_queue_precommit_complete": complete,
            "selected_route": metric_value(path, "phase258_selected_route", ""),
            "input_event_bar_rows": as_int(metric_value(path, "phase258_input_event_bar_rows", 0)),
            "input_symbols": as_int(metric_value(path, "phase258_input_symbols", 0)),
            "input_trade_dates": as_int(metric_value(path, "phase258_input_trade_dates", 0)),
            "mean_spread_bps": metric_value(path, "phase258_mean_spread_bps", ""),
            "mean_l2_l5_bid_share": metric_value(path, "phase258_mean_l2_l5_bid_share", ""),
            "mean_l2_l5_ask_share": metric_value(path, "phase258_mean_l2_l5_ask_share", ""),
            "order_model_contract_rows": as_int(metric_value(path, "phase258_order_model_contract_rows", 0)),
            "feature_contract_rows": as_int(metric_value(path, "phase258_feature_contract_rows", 0)),
            "candidate_family_rows": as_int(metric_value(path, "phase258_candidate_family_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase258_control_contract_rows", 0)),
            "full_top_five_depth_required": as_int(metric_value(path, "phase258_full_top_five_depth_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase258_l1_only_candidate_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase258_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase258_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase258_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase258_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase258_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase258_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase258_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase258_next_best_action", ""),
        }
    if phase == 259:
        complete = as_int(metric_value(path, "phase259_passive_training_search_complete", 0))
        survivor_rows = as_int(metric_value(path, "phase259_survivor_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_queue_aware_training_search_no_survivor_interpretation_open" if complete and survivor_rows == 0 else "passive_queue_aware_training_candidate_interpretation_open",
            "passive_training_search_complete": complete,
            "input_event_bar_rows": as_int(metric_value(path, "phase259_input_event_bar_rows", 0)),
            "symbols": as_int(metric_value(path, "phase259_symbols", 0)),
            "trade_dates": as_int(metric_value(path, "phase259_trade_dates", 0)),
            "variant_rows": as_int(metric_value(path, "phase259_variant_rows", 0)),
            "full_top_five_depth_variant_rows": as_int(metric_value(path, "phase259_full_top_five_depth_variant_rows", 0)),
            "depth_beyond_l1_variant_rows": as_int(metric_value(path, "phase259_depth_beyond_l1_variant_rows", 0)),
            "cost100_positive_variant_rows": as_int(metric_value(path, "phase259_cost100_positive_variant_rows", 0)),
            "cost150_positive_variant_rows": as_int(metric_value(path, "phase259_cost150_positive_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase259_cost200_positive_variant_rows", 0)),
            "survivor_candidate_rows": survivor_rows,
            "best_candidate_id": metric_value(path, "phase259_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase259_best_family_id", ""),
            "best_cost100_expected_net_pnl_inr": metric_value(path, "phase259_best_cost100_expected_net_pnl_inr", ""),
            "best_cost200_expected_net_pnl_inr": metric_value(path, "phase259_best_cost200_expected_net_pnl_inr", ""),
            "best_opportunity_rows": as_int(metric_value(path, "phase259_best_opportunity_rows", 0)),
            "best_symbols": as_int(metric_value(path, "phase259_best_symbols", 0)),
            "best_realized_fill_equivalent_rows": metric_value(path, "phase259_best_realized_fill_equivalent_rows", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase259_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase259_hard_gate_rows", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase259_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase259_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase259_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase259_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase259_next_best_action", ""),
        }
    if phase == 260:
        complete = as_int(metric_value(path, "phase260_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_opportunity_breadth_fill_model_repair_precommit_open" if complete else "phase260_interpretation_gated",
            "interpretation_complete": complete,
            "phase259_variant_rows": as_int(metric_value(path, "phase260_phase259_variant_rows", 0)),
            "phase259_full_depth_variant_rows": as_int(metric_value(path, "phase260_phase259_full_depth_variant_rows", 0)),
            "phase259_cost100_positive_variant_rows": as_int(metric_value(path, "phase260_phase259_cost100_positive_variant_rows", 0)),
            "phase259_cost200_positive_variant_rows": as_int(metric_value(path, "phase260_phase259_cost200_positive_variant_rows", 0)),
            "phase259_survivor_candidate_rows": as_int(metric_value(path, "phase260_phase259_survivor_candidate_rows", 0)),
            "phase259_best_opportunity_rows": as_int(metric_value(path, "phase260_phase259_best_opportunity_rows", 0)),
            "close_phase259_for_promotion": as_int(metric_value(path, "phase260_close_phase259_for_promotion", 0)),
            "full_passive_route_closed": as_int(metric_value(path, "phase260_full_passive_route_closed", 0)),
            "full_top_five_depth_preserved": as_int(metric_value(path, "phase260_full_top_five_depth_preserved", 0)),
            "selected_next_route": metric_value(path, "phase260_selected_next_route", ""),
            "next_route_contract_rows": as_int(metric_value(path, "phase260_next_route_contract_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase260_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase260_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase260_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase260_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase260_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase260_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase260_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase260_next_best_action", ""),
        }
    if phase == 261:
        complete = as_int(metric_value(path, "phase261_passive_repair_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_opportunity_breadth_fill_model_training_search_open" if complete else "phase261_passive_repair_precommit_gated",
            "passive_repair_precommit_complete": complete,
            "selected_route": metric_value(path, "phase261_selected_route", ""),
            "input_event_bar_rows": as_int(metric_value(path, "phase261_input_event_bar_rows", 0)),
            "input_symbols": as_int(metric_value(path, "phase261_input_symbols", 0)),
            "input_trade_dates": as_int(metric_value(path, "phase261_input_trade_dates", 0)),
            "mean_l2_l5_bid_share": metric_value(path, "phase261_mean_l2_l5_bid_share", ""),
            "mean_l2_l5_ask_share": metric_value(path, "phase261_mean_l2_l5_ask_share", ""),
            "repair_contract_rows": as_int(metric_value(path, "phase261_repair_contract_rows", 0)),
            "fill_probability_grid_rows": as_int(metric_value(path, "phase261_fill_probability_grid_rows", 0)),
            "candidate_family_rows": as_int(metric_value(path, "phase261_candidate_family_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase261_control_contract_rows", 0)),
            "full_top_five_depth_required": as_int(metric_value(path, "phase261_full_top_five_depth_required", 0)),
            "levels_2_to_5_materiality_required": as_int(metric_value(path, "phase261_levels_2_to_5_materiality_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase261_l1_only_candidate_allowed", 1)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase261_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase261_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase261_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase261_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase261_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase261_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase261_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase261_next_best_action", ""),
        }
    if phase == 262:
        complete = as_int(metric_value(path, "phase262_passive_training_search_complete", 0))
        survivor_rows = as_int(metric_value(path, "phase262_survivor_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_opportunity_breadth_fill_model_training_no_survivor_interpretation_open" if complete and survivor_rows == 0 else ("passive_opportunity_breadth_fill_model_training_survivor_interpretation_open" if complete else "phase262_passive_training_search_gated"),
            "passive_training_search_complete": complete,
            "input_event_bar_rows": as_int(metric_value(path, "phase262_input_event_bar_rows", 0)),
            "symbols": as_int(metric_value(path, "phase262_symbols", 0)),
            "trade_dates": as_int(metric_value(path, "phase262_trade_dates", 0)),
            "variant_rows": as_int(metric_value(path, "phase262_variant_rows", 0)),
            "full_top_five_depth_variant_rows": as_int(metric_value(path, "phase262_full_top_five_depth_variant_rows", 0)),
            "depth_beyond_l1_variant_rows": as_int(metric_value(path, "phase262_depth_beyond_l1_variant_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase262_l1_only_variant_rows", 0)),
            "fill_model_rows_used": as_int(metric_value(path, "phase262_fill_model_rows_used", 0)),
            "cost100_positive_variant_rows": as_int(metric_value(path, "phase262_cost100_positive_variant_rows", 0)),
            "cost150_positive_variant_rows": as_int(metric_value(path, "phase262_cost150_positive_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase262_cost200_positive_variant_rows", 0)),
            "survivor_candidate_rows": survivor_rows,
            "best_candidate_id": metric_value(path, "phase262_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase262_best_family_id", ""),
            "best_fill_model_id": metric_value(path, "phase262_best_fill_model_id", ""),
            "best_cost100_expected_net_pnl_inr": metric_value(path, "phase262_best_cost100_expected_net_pnl_inr", ""),
            "best_cost200_expected_net_pnl_inr": metric_value(path, "phase262_best_cost200_expected_net_pnl_inr", ""),
            "best_opportunity_rows": as_int(metric_value(path, "phase262_best_opportunity_rows", 0)),
            "best_symbols": as_int(metric_value(path, "phase262_best_symbols", 0)),
            "best_realized_fill_equivalent_rows": metric_value(path, "phase262_best_realized_fill_equivalent_rows", ""),
            "best_side_flip_degrades": as_int(metric_value(path, "phase262_best_side_flip_degrades", 0)),
            "best_random_side_beat": as_int(metric_value(path, "phase262_best_random_side_beat", 0)),
            "best_queue_adversity_survives": as_int(metric_value(path, "phase262_best_queue_adversity_survives", 0)),
            "best_nonfill_stress_survives": as_int(metric_value(path, "phase262_best_nonfill_stress_survives", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase262_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase262_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase262_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase262_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase262_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase262_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase262_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase262_next_best_action", ""),
        }
    if phase == 263:
        complete = as_int(metric_value(path, "phase263_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_shock_absorption_event_precommit_open" if complete else "phase263_interpretation_gated",
            "interpretation_complete": complete,
            "phase262_variant_rows": as_int(metric_value(path, "phase263_phase262_variant_rows", 0)),
            "phase262_full_depth_variant_rows": as_int(metric_value(path, "phase263_phase262_full_depth_variant_rows", 0)),
            "phase262_l2_l5_variant_rows": as_int(metric_value(path, "phase263_phase262_l2_l5_variant_rows", 0)),
            "phase262_l1_only_variant_rows": as_int(metric_value(path, "phase263_phase262_l1_only_variant_rows", 0)),
            "phase262_cost100_positive_variant_rows": as_int(metric_value(path, "phase263_phase262_cost100_positive_variant_rows", 0)),
            "phase262_cost200_positive_variant_rows": as_int(metric_value(path, "phase263_phase262_cost200_positive_variant_rows", 0)),
            "phase262_survivor_candidate_rows": as_int(metric_value(path, "phase263_phase262_survivor_candidate_rows", 0)),
            "phase262_best_cost100_expected_net_pnl_inr": metric_value(path, "phase263_phase262_best_cost100_expected_net_pnl_inr", ""),
            "phase262_best_cost200_expected_net_pnl_inr": metric_value(path, "phase263_phase262_best_cost200_expected_net_pnl_inr", ""),
            "close_phase262_for_promotion": as_int(metric_value(path, "phase263_close_phase262_for_promotion", 0)),
            "close_passive_spread_capture_fill_model_route": as_int(metric_value(path, "phase263_close_passive_spread_capture_fill_model_route", 0)),
            "full_top_five_depth_preserved": as_int(metric_value(path, "phase263_full_top_five_depth_preserved", 0)),
            "threshold_relaxation_only_allowed": as_int(metric_value(path, "phase263_threshold_relaxation_only_allowed", 1)),
            "selected_next_route": metric_value(path, "phase263_selected_next_route", ""),
            "next_route_contract_rows": as_int(metric_value(path, "phase263_next_route_contract_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase263_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase263_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase263_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase263_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase263_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase263_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase263_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase263_next_best_action", ""),
        }
    if phase == 264:
        complete = as_int(metric_value(path, "phase264_liquidity_shock_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_shock_absorption_event_training_search_open" if complete else "phase264_liquidity_shock_precommit_gated",
            "liquidity_shock_precommit_complete": complete,
            "selected_route": metric_value(path, "phase264_selected_route", ""),
            "input_event_bar_rows": as_int(metric_value(path, "phase264_input_event_bar_rows", 0)),
            "input_symbols": as_int(metric_value(path, "phase264_input_symbols", 0)),
            "input_trade_dates": as_int(metric_value(path, "phase264_input_trade_dates", 0)),
            "mean_l2_l5_bid_share": metric_value(path, "phase264_mean_l2_l5_bid_share", ""),
            "mean_l2_l5_ask_share": metric_value(path, "phase264_mean_l2_l5_ask_share", ""),
            "mean_abs_l2_l5_imbalance": metric_value(path, "phase264_mean_abs_l2_l5_imbalance", ""),
            "feature_catalog_rows": as_int(metric_value(path, "phase264_feature_catalog_rows", 0)),
            "event_family_rows": as_int(metric_value(path, "phase264_event_family_rows", 0)),
            "label_contract_rows": as_int(metric_value(path, "phase264_label_contract_rows", 0)),
            "search_grid_contract_rows": as_int(metric_value(path, "phase264_search_grid_contract_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase264_control_contract_rows", 0)),
            "full_top_five_depth_required": as_int(metric_value(path, "phase264_full_top_five_depth_required", 0)),
            "levels_2_to_5_materiality_required": as_int(metric_value(path, "phase264_levels_2_to_5_materiality_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase264_l1_only_candidate_allowed", 1)),
            "threshold_relaxation_only_allowed": as_int(metric_value(path, "phase264_threshold_relaxation_only_allowed", 1)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase264_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase264_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase264_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase264_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase264_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase264_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase264_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase264_next_best_action", ""),
        }
    if phase == 265:
        complete = as_int(metric_value(path, "phase265_liquidity_shock_training_search_complete", 0))
        survivor_rows = as_int(metric_value(path, "phase265_survivor_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_shock_training_no_survivor_interpretation_open" if complete and survivor_rows == 0 else ("full_depth_liquidity_shock_training_survivor_interpretation_open" if complete else "phase265_liquidity_shock_training_search_gated"),
            "liquidity_shock_training_search_complete": complete,
            "input_event_bar_rows": as_int(metric_value(path, "phase265_input_event_bar_rows", 0)),
            "symbols": as_int(metric_value(path, "phase265_symbols", 0)),
            "trade_dates": as_int(metric_value(path, "phase265_trade_dates", 0)),
            "variant_rows": as_int(metric_value(path, "phase265_variant_rows", 0)),
            "full_top_five_depth_variant_rows": as_int(metric_value(path, "phase265_full_top_five_depth_variant_rows", 0)),
            "depth_beyond_l1_variant_rows": as_int(metric_value(path, "phase265_depth_beyond_l1_variant_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase265_l1_only_variant_rows", 0)),
            "cost100_positive_variant_rows": as_int(metric_value(path, "phase265_cost100_positive_variant_rows", 0)),
            "cost150_positive_variant_rows": as_int(metric_value(path, "phase265_cost150_positive_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase265_cost200_positive_variant_rows", 0)),
            "survivor_candidate_rows": survivor_rows,
            "best_candidate_id": metric_value(path, "phase265_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase265_best_family_id", ""),
            "best_cost100_net_pnl_inr": metric_value(path, "phase265_best_cost100_net_pnl_inr", ""),
            "best_cost200_net_pnl_inr": metric_value(path, "phase265_best_cost200_net_pnl_inr", ""),
            "best_event_rows": as_int(metric_value(path, "phase265_best_event_rows", 0)),
            "best_symbols": as_int(metric_value(path, "phase265_best_symbols", 0)),
            "best_trade_dates": as_int(metric_value(path, "phase265_best_trade_dates", 0)),
            "best_side_flip_degrades": as_int(metric_value(path, "phase265_best_side_flip_degrades", 0)),
            "best_random_side_beat": as_int(metric_value(path, "phase265_best_random_side_beat", 0)),
            "best_shuffle_label_beat": as_int(metric_value(path, "phase265_best_shuffle_label_beat", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase265_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase265_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase265_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase265_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase265_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase265_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase265_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase265_next_best_action", ""),
        }
    if phase == 266:
        complete = as_int(metric_value(path, "phase266_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_shock_breadth_shuffle_repair_precommit_open" if complete else "phase266_liquidity_shock_interpretation_gated",
            "interpretation_complete": complete,
            "phase265_variant_rows": as_int(metric_value(path, "phase266_phase265_variant_rows", 0)),
            "phase265_full_depth_variant_rows": as_int(metric_value(path, "phase266_phase265_full_depth_variant_rows", 0)),
            "phase265_l2_l5_variant_rows": as_int(metric_value(path, "phase266_phase265_l2_l5_variant_rows", 0)),
            "phase265_l1_only_variant_rows": as_int(metric_value(path, "phase266_phase265_l1_only_variant_rows", 0)),
            "phase265_cost100_positive_variant_rows": as_int(metric_value(path, "phase266_phase265_cost100_positive_variant_rows", 0)),
            "phase265_cost150_positive_variant_rows": as_int(metric_value(path, "phase266_phase265_cost150_positive_variant_rows", 0)),
            "phase265_cost200_positive_variant_rows": as_int(metric_value(path, "phase266_phase265_cost200_positive_variant_rows", 0)),
            "phase265_survivor_candidate_rows": as_int(metric_value(path, "phase266_phase265_survivor_candidate_rows", 0)),
            "best_candidate_id": metric_value(path, "phase266_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase266_best_family_id", ""),
            "best_cost100_net_pnl_inr": metric_value(path, "phase266_best_cost100_net_pnl_inr", ""),
            "best_cost200_net_pnl_inr": metric_value(path, "phase266_best_cost200_net_pnl_inr", ""),
            "best_cost200_avg_net_per_event_inr": metric_value(path, "phase266_best_cost200_avg_net_per_event_inr", ""),
            "best_event_rows": as_int(metric_value(path, "phase266_best_event_rows", 0)),
            "best_symbols": as_int(metric_value(path, "phase266_best_symbols", 0)),
            "best_trade_dates": as_int(metric_value(path, "phase266_best_trade_dates", 0)),
            "best_shuffle_label_margin_inr": metric_value(path, "phase266_best_shuffle_label_margin_inr", ""),
            "close_phase265_for_promotion": as_int(metric_value(path, "phase266_close_phase265_for_promotion", 0)),
            "close_phase265_for_replay": as_int(metric_value(path, "phase266_close_phase265_for_replay", 0)),
            "recognize_promising_but_unaccepted_2x_pocket": as_int(metric_value(path, "phase266_recognize_promising_but_unaccepted_2x_pocket", 0)),
            "close_current_narrow_liquidity_shock_candidate": as_int(metric_value(path, "phase266_close_current_narrow_liquidity_shock_candidate", 0)),
            "full_top_five_depth_preserved": as_int(metric_value(path, "phase266_full_top_five_depth_preserved", 0)),
            "threshold_relaxation_only_allowed": as_int(metric_value(path, "phase266_threshold_relaxation_only_allowed", 1)),
            "selected_next_route": metric_value(path, "phase266_selected_next_route", ""),
            "next_route_contract_rows": as_int(metric_value(path, "phase266_next_route_contract_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase266_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase266_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase266_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase266_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase266_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase266_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase266_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase266_next_best_action", ""),
        }
    if phase == 267:
        complete = as_int(metric_value(path, "phase267_breadth_shuffle_repair_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_shock_two_lane_training_search_open" if complete else "phase267_breadth_shuffle_repair_precommit_gated",
            "breadth_shuffle_repair_precommit_complete": complete,
            "selected_route": metric_value(path, "phase267_selected_route", ""),
            "phase266_interpretation_complete": as_int(metric_value(path, "phase267_phase266_interpretation_complete", 0)),
            "phase266_full_depth_preserved": as_int(metric_value(path, "phase267_phase266_full_depth_preserved", 0)),
            "phase266_close_phase265_for_replay": as_int(metric_value(path, "phase267_phase266_close_phase265_for_replay", 0)),
            "phase266_best_cost200_avg_net_per_event_inr": metric_value(path, "phase267_phase266_best_cost200_avg_net_per_event_inr", ""),
            "phase266_best_shuffle_label_margin_inr": metric_value(path, "phase267_phase266_best_shuffle_label_margin_inr", ""),
            "repair_feature_catalog_rows": as_int(metric_value(path, "phase267_repair_feature_catalog_rows", 0)),
            "candidate_family_rows": as_int(metric_value(path, "phase267_candidate_family_rows", 0)),
            "acceptance_floor_rows": as_int(metric_value(path, "phase267_acceptance_floor_rows", 0)),
            "search_grid_contract_rows": as_int(metric_value(path, "phase267_search_grid_contract_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase267_control_contract_rows", 0)),
            "exploratory_lane_enabled": as_int(metric_value(path, "phase267_exploratory_lane_enabled", 0)),
            "exploratory_controls_are_filters": as_int(metric_value(path, "phase267_exploratory_controls_are_filters", 1)),
            "exploratory_min_event_rows": as_int(metric_value(path, "phase267_exploratory_min_event_rows", 0)),
            "exploratory_min_symbols": as_int(metric_value(path, "phase267_exploratory_min_symbols", 0)),
            "acceptance_min_event_rows": as_int(metric_value(path, "phase267_acceptance_min_event_rows", 0)),
            "acceptance_min_symbols": as_int(metric_value(path, "phase267_acceptance_min_symbols", 0)),
            "acceptance_min_cost200_avg_net_per_event_inr": metric_value(path, "phase267_acceptance_min_cost200_avg_net_per_event_inr", ""),
            "acceptance_min_shuffle_label_margin_inr": metric_value(path, "phase267_acceptance_min_shuffle_label_margin_inr", ""),
            "full_top_five_depth_required": as_int(metric_value(path, "phase267_full_top_five_depth_required", 0)),
            "levels_2_to_5_materiality_required": as_int(metric_value(path, "phase267_levels_2_to_5_materiality_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase267_l1_only_candidate_allowed", 1)),
            "threshold_relaxation_only_allowed": as_int(metric_value(path, "phase267_threshold_relaxation_only_allowed", 1)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase267_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase267_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase267_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase267_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase267_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase267_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase267_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase267_next_best_action", ""),
        }
    if phase == 268:
        complete = as_int(metric_value(path, "phase268_two_lane_training_search_complete", 0))
        acceptance_rows = as_int(metric_value(path, "phase268_acceptance_grade_candidate_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_shock_two_lane_training_no_acceptance_interpretation_open" if complete and acceptance_rows == 0 else ("full_depth_liquidity_shock_two_lane_acceptance_interpretation_open" if complete else "phase268_two_lane_training_search_gated"),
            "two_lane_training_search_complete": complete,
            "input_event_bar_rows": as_int(metric_value(path, "phase268_input_event_bar_rows", 0)),
            "symbols": as_int(metric_value(path, "phase268_symbols", 0)),
            "trade_dates": as_int(metric_value(path, "phase268_trade_dates", 0)),
            "variant_rows": as_int(metric_value(path, "phase268_variant_rows", 0)),
            "full_top_five_depth_variant_rows": as_int(metric_value(path, "phase268_full_top_five_depth_variant_rows", 0)),
            "depth_beyond_l1_variant_rows": as_int(metric_value(path, "phase268_depth_beyond_l1_variant_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase268_l1_only_variant_rows", 0)),
            "exploratory_candidate_rows": as_int(metric_value(path, "phase268_exploratory_candidate_rows", 0)),
            "annualized_profitable_research_lead_rows": as_int(metric_value(path, "phase268_annualized_profitable_research_lead_rows", 0)),
            "cost200_annualized_profitable_research_lead_rows": as_int(metric_value(path, "phase268_cost200_annualized_profitable_research_lead_rows", 0)),
            "acceptance_grade_candidate_rows": acceptance_rows,
            "cost100_positive_variant_rows": as_int(metric_value(path, "phase268_cost100_positive_variant_rows", 0)),
            "cost150_positive_variant_rows": as_int(metric_value(path, "phase268_cost150_positive_variant_rows", 0)),
            "cost200_positive_variant_rows": as_int(metric_value(path, "phase268_cost200_positive_variant_rows", 0)),
            "best_candidate_id": metric_value(path, "phase268_best_candidate_id", ""),
            "best_family_id": metric_value(path, "phase268_best_family_id", ""),
            "best_exploratory_candidate": as_int(metric_value(path, "phase268_best_exploratory_candidate", 0)),
            "best_acceptance_grade_candidate": as_int(metric_value(path, "phase268_best_acceptance_grade_candidate", 0)),
            "best_cost100_net_pnl_inr": metric_value(path, "phase268_best_cost100_net_pnl_inr", ""),
            "best_cost100_annualized_return_pct": metric_value(path, "phase268_best_cost100_annualized_return_pct", ""),
            "best_cost200_net_pnl_inr": metric_value(path, "phase268_best_cost200_net_pnl_inr", ""),
            "best_cost200_annualized_return_pct": metric_value(path, "phase268_best_cost200_annualized_return_pct", ""),
            "best_cost200_avg_net_per_event_inr": metric_value(path, "phase268_best_cost200_avg_net_per_event_inr", ""),
            "best_event_rows": as_int(metric_value(path, "phase268_best_event_rows", 0)),
            "best_symbols": as_int(metric_value(path, "phase268_best_symbols", 0)),
            "best_trade_dates": as_int(metric_value(path, "phase268_best_trade_dates", 0)),
            "best_shuffle_label_margin_inr": metric_value(path, "phase268_best_shuffle_label_margin_inr", ""),
            "best_side_flip_degrades": as_int(metric_value(path, "phase268_best_side_flip_degrades", 0)),
            "best_random_side_beat": as_int(metric_value(path, "phase268_best_random_side_beat", 0)),
            "exploratory_controls_are_filters": as_int(metric_value(path, "phase268_exploratory_controls_are_filters", 1)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase268_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase268_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase268_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase268_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase268_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase268_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase268_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase268_next_best_action", ""),
        }
    if phase == 269:
        complete = as_int(metric_value(path, "phase269_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "fixed_capital_concurrency_capacity_return_precommit_open" if complete else "phase269_two_lane_interpretation_gated",
            "interpretation_complete": complete,
            "phase268_variant_rows": as_int(metric_value(path, "phase269_phase268_variant_rows", 0)),
            "phase268_full_depth_variant_rows": as_int(metric_value(path, "phase269_phase268_full_depth_variant_rows", 0)),
            "phase268_l2_l5_variant_rows": as_int(metric_value(path, "phase269_phase268_l2_l5_variant_rows", 0)),
            "phase268_l1_only_variant_rows": as_int(metric_value(path, "phase269_phase268_l1_only_variant_rows", 0)),
            "phase268_exploratory_candidate_rows": as_int(metric_value(path, "phase269_phase268_exploratory_candidate_rows", 0)),
            "phase268_annualized_profitable_research_lead_rows": as_int(metric_value(path, "phase269_phase268_annualized_profitable_research_lead_rows", 0)),
            "phase268_cost200_annualized_profitable_research_lead_rows": as_int(metric_value(path, "phase269_phase268_cost200_annualized_profitable_research_lead_rows", 0)),
            "phase268_acceptance_grade_candidate_rows": as_int(metric_value(path, "phase269_phase268_acceptance_grade_candidate_rows", 0)),
            "annualization_notional_inr": metric_value(path, "phase269_annualization_notional_inr", ""),
            "annualization_formula": metric_value(path, "phase269_annualization_formula", ""),
            "annualization_is_portfolio_return": as_int(metric_value(path, "phase269_annualization_is_portfolio_return", 1)),
            "best_research_lead_candidate_id": metric_value(path, "phase269_best_research_lead_candidate_id", ""),
            "best_research_lead_family_id": metric_value(path, "phase269_best_research_lead_family_id", ""),
            "best_research_lead_cost100_annualized_return_pct": metric_value(path, "phase269_best_research_lead_cost100_annualized_return_pct", ""),
            "best_research_lead_cost200_annualized_return_pct": metric_value(path, "phase269_best_research_lead_cost200_annualized_return_pct", ""),
            "best_research_lead_events": as_int(metric_value(path, "phase269_best_research_lead_events", 0)),
            "best_research_lead_symbols": as_int(metric_value(path, "phase269_best_research_lead_symbols", 0)),
            "best_research_lead_shuffle_margin_inr": metric_value(path, "phase269_best_research_lead_shuffle_margin_inr", ""),
            "preserve_research_leads": as_int(metric_value(path, "phase269_preserve_research_leads", 0)),
            "do_not_claim_portfolio_annual_return": as_int(metric_value(path, "phase269_do_not_claim_portfolio_annual_return", 0)),
            "do_not_promote_or_replay_phase268": as_int(metric_value(path, "phase269_do_not_promote_or_replay_phase268", 0)),
            "selected_next_route": metric_value(path, "phase269_selected_next_route", ""),
            "next_route_contract_rows": as_int(metric_value(path, "phase269_next_route_contract_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase269_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase269_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase269_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase269_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase269_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase269_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase269_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase269_next_best_action", ""),
        }
    if phase == 270:
        complete = as_int(metric_value(path, "phase270_fixed_capital_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "fixed_capital_concurrency_capacity_return_analysis_open" if complete else "phase270_fixed_capital_precommit_gated",
            "fixed_capital_precommit_complete": complete,
            "selected_route": metric_value(path, "phase270_selected_route", ""),
            "phase269_interpretation_complete": as_int(metric_value(path, "phase270_phase269_interpretation_complete", 0)),
            "phase269_research_leads_preserved": as_int(metric_value(path, "phase270_phase269_research_leads_preserved", 0)),
            "phase269_do_not_claim_portfolio_annual_return": as_int(metric_value(path, "phase270_phase269_do_not_claim_portfolio_annual_return", 0)),
            "phase269_do_not_promote_or_replay": as_int(metric_value(path, "phase270_phase269_do_not_promote_or_replay", 0)),
            "capital_model_contract_rows": as_int(metric_value(path, "phase270_capital_model_contract_rows", 0)),
            "concurrency_capacity_contract_rows": as_int(metric_value(path, "phase270_concurrency_capacity_contract_rows", 0)),
            "candidate_input_contract_rows": as_int(metric_value(path, "phase270_candidate_input_contract_rows", 0)),
            "return_output_contract_rows": as_int(metric_value(path, "phase270_return_output_contract_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase270_control_contract_rows", 0)),
            "full_top_five_depth_required": as_int(metric_value(path, "phase270_full_top_five_depth_required", 0)),
            "levels_2_to_5_materiality_required": as_int(metric_value(path, "phase270_levels_2_to_5_materiality_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase270_l1_only_candidate_allowed", 1)),
            "unlimited_capital_assumption_allowed": as_int(metric_value(path, "phase270_unlimited_capital_assumption_allowed", 1)),
            "portfolio_return_claim_without_scheduler_allowed": as_int(metric_value(path, "phase270_portfolio_return_claim_without_scheduler_allowed", 1)),
            "fixed_notional_proxy_as_portfolio_return_allowed": as_int(metric_value(path, "phase270_fixed_notional_proxy_as_portfolio_return_allowed", 1)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase270_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase270_hard_gate_rows", 0)),
            "download_more_dates_now_allowed": as_int(metric_value(path, "phase270_download_more_dates_now_allowed", 0)),
            "replay_execution_allowed_now": as_int(metric_value(path, "phase270_replay_execution_allowed_now", 0)),
            "strategy_replay_allowed": 0,
            "promotion_allowed": as_int(metric_value(path, "phase270_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase270_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase270_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase270_next_best_action", ""),
        }
    if phase == 271:
        complete = as_int(metric_value(path, "phase271_fixed_capital_analysis_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "fixed_capital_capacity_return_interpretation_open" if complete else "phase271_fixed_capital_analysis_gated",
            "fixed_capital_analysis_complete": complete,
            "selected_route": metric_value(path, "phase271_selected_route", ""),
            "phase269_research_lead_rows": as_int(metric_value(path, "phase271_phase269_research_lead_rows", 0)),
            "input_event_rows": as_int(metric_value(path, "phase271_input_event_rows", 0)),
            "input_symbols": as_int(metric_value(path, "phase271_input_symbols", 0)),
            "observed_trade_dates": as_int(metric_value(path, "phase271_observed_trade_dates", 0)),
            "scenario_rows": as_int(metric_value(path, "phase271_scenario_rows", 0)),
            "scope_rows": as_int(metric_value(path, "phase271_scope_rows", 0)),
            "cost100_annualized_above_12pct_scenario_rows": as_int(metric_value(path, "phase271_cost100_annualized_above_12pct_scenario_rows", 0)),
            "cost150_annualized_above_12pct_scenario_rows": as_int(metric_value(path, "phase271_cost150_annualized_above_12pct_scenario_rows", 0)),
            "cost200_annualized_above_12pct_scenario_rows": as_int(metric_value(path, "phase271_cost200_annualized_above_12pct_scenario_rows", 0)),
            "best_scenario_id": metric_value(path, "phase271_best_scenario_id", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase271_best_realized_net_pnl_inr", ""),
            "best_portfolio_return_pct": metric_value(path, "phase271_best_portfolio_return_pct", ""),
            "best_mechanical_one_date_annualized_portfolio_return_pct": metric_value(path, "phase271_best_mechanical_one_date_annualized_portfolio_return_pct", ""),
            "portfolio_claim_allowed": as_int(metric_value(path, "phase271_portfolio_claim_allowed", 0)),
            "unlimited_capital_assumption_allowed": as_int(metric_value(path, "phase271_unlimited_capital_assumption_allowed", 1)),
            "fixed_notional_proxy_as_portfolio_return_allowed": as_int(metric_value(path, "phase271_fixed_notional_proxy_as_portfolio_return_allowed", 1)),
            "full_top_five_depth_required": as_int(metric_value(path, "phase271_full_top_five_depth_required", 0)),
            "levels_2_to_5_materiality_required": as_int(metric_value(path, "phase271_levels_2_to_5_materiality_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase271_l1_only_candidate_allowed", 1)),
            "acceptance_grade_scenario_rows": as_int(metric_value(path, "phase271_acceptance_grade_scenario_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase271_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase271_hard_gate_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase271_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase271_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase271_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase271_deployable_profitability_claim_allowed", 0)),
            "next_action": metric_value(path, "phase271_next_best_action", ""),
        }
    if phase == 272:
        complete = as_int(metric_value(path, "phase272_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "focused_capital_aware_candidate_followthrough_search_open" if complete else "phase272_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase272_selected_next_route", ""),
            "phase271_scenario_rows": as_int(metric_value(path, "phase272_phase271_scenario_rows", 0)),
            "phase271_scope_rows": as_int(metric_value(path, "phase272_phase271_scope_rows", 0)),
            "phase271_observed_trade_dates": as_int(metric_value(path, "phase272_phase271_observed_trade_dates", 0)),
            "ranked_capital_candidate_rows": as_int(metric_value(path, "phase272_ranked_capital_candidate_rows", 0)),
            "followthrough_priority_candidate_rows": as_int(metric_value(path, "phase272_followthrough_priority_candidate_rows", 0)),
            "pooled_above12_scenario_rows": as_int(metric_value(path, "phase272_pooled_above12_scenario_rows", 0)),
            "best_candidate_id": metric_value(path, "phase272_best_candidate_id", ""),
            "best_scenario_id": metric_value(path, "phase272_best_scenario_id", ""),
            "best_cost_profile": metric_value(path, "phase272_best_cost_profile", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase272_best_realized_net_pnl_inr", ""),
            "best_mechanical_one_date_annualized_portfolio_return_pct": metric_value(path, "phase272_best_mechanical_one_date_annualized_portfolio_return_pct", ""),
            "best_cost200_above12_scenario_rows": as_int(metric_value(path, "phase272_best_cost200_above12_scenario_rows", 0)),
            "portfolio_claim_allowed": as_int(metric_value(path, "phase272_portfolio_claim_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase272_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase272_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase272_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase272_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase272_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase272_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase272_next_best_action", ""),
        }
    if phase == 273:
        complete = as_int(metric_value(path, "phase273_followthrough_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "focused_capital_followthrough_interpretation_open" if complete else "phase273_followthrough_search_gated",
            "followthrough_search_complete": complete,
            "selected_route": metric_value(path, "phase273_selected_route", ""),
            "priority_candidate_rows": as_int(metric_value(path, "phase273_priority_candidate_rows", 0)),
            "priority_candidates": metric_value(path, "phase273_priority_candidates", ""),
            "scope_rows": as_int(metric_value(path, "phase273_scope_rows", 0)),
            "order_policy_rows": as_int(metric_value(path, "phase273_order_policy_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase273_scenario_rows", 0)),
            "cost100_above12_scenario_rows": as_int(metric_value(path, "phase273_cost100_above12_scenario_rows", 0)),
            "cost200_above12_scenario_rows": as_int(metric_value(path, "phase273_cost200_above12_scenario_rows", 0)),
            "cost200_positive_scope_profile_rows": as_int(metric_value(path, "phase273_cost200_positive_scope_profile_rows", 0)),
            "best_scenario_id": metric_value(path, "phase273_best_scenario_id", ""),
            "best_scope_id": metric_value(path, "phase273_best_scope_id", ""),
            "best_scope_candidate_id": metric_value(path, "phase273_best_scope_candidate_id", ""),
            "best_order_policy": metric_value(path, "phase273_best_order_policy", ""),
            "best_cost_profile": metric_value(path, "phase273_best_cost_profile", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase273_best_realized_net_pnl_inr", ""),
            "best_mechanical_one_date_annualized_portfolio_return_pct": metric_value(path, "phase273_best_mechanical_one_date_annualized_portfolio_return_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase273_best_scheduled_event_rows", 0)),
            "best_notional_turnover_x_initial_capital": metric_value(path, "phase273_best_notional_turnover_x_initial_capital", ""),
            "portfolio_claim_allowed": as_int(metric_value(path, "phase273_portfolio_claim_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase273_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase273_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase273_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase273_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase273_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase273_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase273_next_best_action", ""),
        }
    if phase == 274:
        complete = as_int(metric_value(path, "phase274_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "focused_capital_multiday_synthetic_followthrough_search_open" if complete else "phase274_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase274_selected_next_route", ""),
            "phase273_scenario_rows": as_int(metric_value(path, "phase274_phase273_scenario_rows", 0)),
            "phase273_cost100_above12_scenario_rows": as_int(metric_value(path, "phase274_phase273_cost100_above12_scenario_rows", 0)),
            "phase273_cost200_above12_scenario_rows": as_int(metric_value(path, "phase274_phase273_cost200_above12_scenario_rows", 0)),
            "ranked_scope_profile_rows": as_int(metric_value(path, "phase274_ranked_scope_profile_rows", 0)),
            "cost200_survivor_scope_profile_rows": as_int(metric_value(path, "phase274_cost200_survivor_scope_profile_rows", 0)),
            "median_positive_scope_profile_rows": as_int(metric_value(path, "phase274_median_positive_scope_profile_rows", 0)),
            "worst_case_positive_scope_profile_rows": as_int(metric_value(path, "phase274_worst_case_positive_scope_profile_rows", 0)),
            "best_scope_profile": metric_value(path, "phase274_best_scope_profile", ""),
            "best_scenario_id": metric_value(path, "phase274_best_scenario_id", ""),
            "best_order_policy": metric_value(path, "phase274_best_order_policy", ""),
            "best_max_annualized_pct": metric_value(path, "phase274_best_max_annualized_pct", ""),
            "best_median_annualized_pct": metric_value(path, "phase274_best_median_annualized_pct", ""),
            "portfolio_claim_allowed": as_int(metric_value(path, "phase274_portfolio_claim_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase274_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase274_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase274_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase274_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase274_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase274_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase274_next_best_action", ""),
        }
    if phase == 275:
        complete = as_int(metric_value(path, "phase275_multiday_synthetic_followthrough_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "multiday_synthetic_followthrough_interpretation_open" if complete else "phase275_multiday_synthetic_followthrough_search_gated",
            "multiday_synthetic_followthrough_search_complete": complete,
            "selected_route": metric_value(path, "phase275_selected_route", ""),
            "scenario_rows": as_int(metric_value(path, "phase275_scenario_rows", 0)),
            "scope_profile_rows": as_int(metric_value(path, "phase275_scope_profile_rows", 0)),
            "order_policy_rows": as_int(metric_value(path, "phase275_order_policy_rows", 0)),
            "synthetic_seed_rows": as_int(metric_value(path, "phase275_synthetic_seed_rows", 0)),
            "synthetic_regime_rows": as_int(metric_value(path, "phase275_synthetic_regime_rows", 0)),
            "synthetic_date_rows": as_int(metric_value(path, "phase275_synthetic_date_rows", 0)),
            "cost100_above12_scenario_rows": as_int(metric_value(path, "phase275_cost100_above12_scenario_rows", 0)),
            "cost200_above12_scenario_rows": as_int(metric_value(path, "phase275_cost200_above12_scenario_rows", 0)),
            "cost200_median_above12_scope_profile_rows": as_int(metric_value(path, "phase275_cost200_median_above12_scope_profile_rows", 0)),
            "cost200_worst_case_above12_scope_profile_rows": as_int(metric_value(path, "phase275_cost200_worst_case_above12_scope_profile_rows", 0)),
            "best_scenario_id": metric_value(path, "phase275_best_scenario_id", ""),
            "best_scope_profile": metric_value(path, "phase275_best_scope_profile", ""),
            "best_order_policy": metric_value(path, "phase275_best_order_policy", ""),
            "best_synthetic_regime": metric_value(path, "phase275_best_synthetic_regime", ""),
            "best_synthetic_seed": metric_value(path, "phase275_best_synthetic_seed", ""),
            "best_cost_profile": metric_value(path, "phase275_best_cost_profile", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase275_best_realized_net_pnl_inr", ""),
            "best_synthetic_multiday_annualized_portfolio_return_pct": metric_value(path, "phase275_best_synthetic_multiday_annualized_portfolio_return_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase275_best_scheduled_event_rows", 0)),
            "synthetic_multiday_diagnostic_allowed": as_int(metric_value(path, "phase275_synthetic_multiday_diagnostic_allowed", 0)),
            "portfolio_claim_allowed": as_int(metric_value(path, "phase275_portfolio_claim_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase275_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase275_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase275_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase275_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase275_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase275_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase275_next_best_action", ""),
        }
    if phase == 276:
        complete = as_int(metric_value(path, "phase276_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_robust_full_depth_redesign_search_open" if complete else "phase276_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase276_selected_next_route", ""),
            "phase275_scenario_rows": as_int(metric_value(path, "phase276_phase275_scenario_rows", 0)),
            "phase275_synthetic_date_rows": as_int(metric_value(path, "phase276_phase275_synthetic_date_rows", 0)),
            "phase275_cost100_above12_scenario_rows": as_int(metric_value(path, "phase276_phase275_cost100_above12_scenario_rows", 0)),
            "phase275_cost200_above12_scenario_rows": as_int(metric_value(path, "phase276_phase275_cost200_above12_scenario_rows", 0)),
            "phase275_best_synthetic_multiday_annualized_pct": metric_value(path, "phase276_phase275_best_synthetic_multiday_annualized_pct", ""),
            "ranked_profile_rows": as_int(metric_value(path, "phase276_ranked_profile_rows", 0)),
            "normal_cost_sparse_positive_profile_rows": as_int(metric_value(path, "phase276_normal_cost_sparse_positive_profile_rows", 0)),
            "cost200_failed_profile_rows": as_int(metric_value(path, "phase276_cost200_failed_profile_rows", 0)),
            "best_redesign_anchor_profile": metric_value(path, "phase276_best_redesign_anchor_profile", ""),
            "best_redesign_anchor_max_annualized_pct": metric_value(path, "phase276_best_redesign_anchor_max_annualized_pct", ""),
            "as_is_promotion_allowed": as_int(metric_value(path, "phase276_phase275_as_is_promotion_allowed", 0)),
            "portfolio_claim_allowed": as_int(metric_value(path, "phase276_portfolio_claim_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase276_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase276_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase276_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase276_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase276_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase276_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase276_next_best_action", ""),
        }
    if phase == 277:
        complete = as_int(metric_value(path, "phase277_cost_robust_redesign_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_robust_redesign_interpretation_open" if complete else "phase277_cost_robust_redesign_search_gated",
            "cost_robust_redesign_search_complete": complete,
            "selected_route": metric_value(path, "phase277_selected_route", ""),
            "variant_rows": as_int(metric_value(path, "phase277_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase277_scenario_rows", 0)),
            "full_depth_variant_rows": as_int(metric_value(path, "phase277_full_depth_variant_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase277_l1_only_variant_rows", 0)),
            "cost200_above12_scenario_rows": as_int(metric_value(path, "phase277_cost200_above12_scenario_rows", 0)),
            "cost200_median_above12_variant_rows": as_int(metric_value(path, "phase277_cost200_median_above12_variant_rows", 0)),
            "cost200_worst_case_above12_variant_rows": as_int(metric_value(path, "phase277_cost200_worst_case_above12_variant_rows", 0)),
            "best_variant_id": metric_value(path, "phase277_best_variant_id", ""),
            "best_redesign_family": metric_value(path, "phase277_best_redesign_family", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase277_best_realized_net_pnl_inr", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase277_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase277_best_scheduled_event_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase277_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase277_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase277_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase277_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase277_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase277_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase277_next_best_action", ""),
        }
    if phase == 278:
        complete = as_int(metric_value(path, "phase278_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "material_new_target_construction_precommit_open" if complete else "phase278_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase278_selected_next_route", ""),
            "phase277_variant_rows": as_int(metric_value(path, "phase278_phase277_variant_rows", 0)),
            "phase277_scenario_rows": as_int(metric_value(path, "phase278_phase277_scenario_rows", 0)),
            "phase277_cost200_above12_scenario_rows": as_int(metric_value(path, "phase278_phase277_cost200_above12_scenario_rows", 0)),
            "phase277_best_cost200_annualized_pct": metric_value(path, "phase278_phase277_best_cost200_annualized_pct", ""),
            "material_clue_variant_rows": as_int(metric_value(path, "phase278_material_clue_variant_rows", 0)),
            "close_filter_redesign_for_acceptance": as_int(metric_value(path, "phase278_close_filter_redesign_for_acceptance", 0)),
            "best_preserved_clue_variant": metric_value(path, "phase278_best_preserved_clue_variant", ""),
            "best_preserved_clue_family": metric_value(path, "phase278_best_preserved_clue_family", ""),
            "do_not_relax_cost_threshold": as_int(metric_value(path, "phase278_do_not_relax_cost_threshold", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase278_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase278_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase278_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase278_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase278_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase278_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase278_next_best_action", ""),
        }
    if phase == 279:
        complete = as_int(metric_value(path, "phase279_target_construction_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "material_new_target_construction_search_open" if complete else "phase279_target_construction_precommit_gated",
            "target_construction_precommit_complete": complete,
            "selected_route": metric_value(path, "phase279_selected_route", ""),
            "target_family_rows": as_int(metric_value(path, "phase279_target_family_rows", 0)),
            "phase280_allowed_target_family_rows": as_int(metric_value(path, "phase279_phase280_allowed_target_family_rows", 0)),
            "preserved_clue_rows": as_int(metric_value(path, "phase279_preserved_clue_rows", 0)),
            "phase280_anchor_clue_rows": as_int(metric_value(path, "phase279_phase280_anchor_clue_rows", 0)),
            "cost200_required": as_int(metric_value(path, "phase279_cost200_required", 0)),
            "full_depth_required": as_int(metric_value(path, "phase279_full_depth_required", 0)),
            "l1_only_allowed": as_int(metric_value(path, "phase279_l1_only_allowed", 1)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase279_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase279_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase279_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase279_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase279_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase279_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase279_next_best_action", ""),
        }
    if phase == 280:
        complete = as_int(metric_value(path, "phase280_material_new_target_construction_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "material_new_target_construction_interpretation_open" if complete else "phase280_material_new_target_construction_search_gated",
            "material_new_target_construction_search_complete": complete,
            "selected_route": metric_value(path, "phase280_selected_route", ""),
            "target_family_rows": as_int(metric_value(path, "phase280_target_family_rows", 0)),
            "variant_rows": as_int(metric_value(path, "phase280_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase280_scenario_rows", 0)),
            "cost200_above12_scenario_rows": as_int(metric_value(path, "phase280_cost200_above12_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase280_best_variant_id", ""),
            "best_target_family": metric_value(path, "phase280_best_target_family", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase280_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase280_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase280_best_scheduled_event_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase280_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase280_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase280_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase280_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase280_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase280_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase280_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase280_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase280_next_best_action", ""),
        }
    if phase == 281:
        complete = as_int(metric_value(path, "phase281_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "regime_conditioned_full_depth_ensemble_precommit_open" if complete else "phase281_material_target_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase281_selected_next_route", ""),
            "phase280_target_family_rows": as_int(metric_value(path, "phase281_phase280_target_family_rows", 0)),
            "phase280_variant_rows": as_int(metric_value(path, "phase281_phase280_variant_rows", 0)),
            "phase280_scenario_rows": as_int(metric_value(path, "phase281_phase280_scenario_rows", 0)),
            "phase280_cost200_above12_scenario_rows": as_int(metric_value(path, "phase281_phase280_cost200_above12_scenario_rows", 0)),
            "phase280_best_cost200_annualized_pct": metric_value(path, "phase281_phase280_best_cost200_annualized_pct", ""),
            "phase280_best_scheduled_event_rows": as_int(metric_value(path, "phase281_phase280_best_scheduled_event_rows", 0)),
            "material_clue_variant_rows": as_int(metric_value(path, "phase281_material_clue_variant_rows", 0)),
            "near_miss_variant_rows": as_int(metric_value(path, "phase281_near_miss_variant_rows", 0)),
            "close_phase280_for_acceptance": as_int(metric_value(path, "phase281_close_phase280_for_acceptance", 0)),
            "best_preserved_clue_variant": metric_value(path, "phase281_best_preserved_clue_variant", ""),
            "best_preserved_clue_family": metric_value(path, "phase281_best_preserved_clue_family", ""),
            "do_not_relax_cost_threshold": as_int(metric_value(path, "phase281_do_not_relax_cost_threshold", 0)),
            "do_not_claim_portfolio_return": as_int(metric_value(path, "phase281_do_not_claim_portfolio_return", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase281_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase281_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase281_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase281_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase281_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase281_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase281_next_best_action", ""),
        }
    if phase == 282:
        complete = as_int(metric_value(path, "phase282_regime_conditioned_ensemble_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "regime_conditioned_full_depth_ensemble_search_open" if complete else "phase282_regime_conditioned_ensemble_precommit_gated",
            "regime_conditioned_ensemble_precommit_complete": complete,
            "selected_route": metric_value(path, "phase282_selected_route", ""),
            "preserved_clue_rows": as_int(metric_value(path, "phase282_preserved_clue_rows", 0)),
            "phase283_search_seed_rows": as_int(metric_value(path, "phase282_phase283_search_seed_rows", 0)),
            "ensemble_family_rows": as_int(metric_value(path, "phase282_ensemble_family_rows", 0)),
            "phase283_allowed_ensemble_rows": as_int(metric_value(path, "phase282_phase283_allowed_ensemble_rows", 0)),
            "regime_bucket_rows": as_int(metric_value(path, "phase282_regime_bucket_rows", 0)),
            "min_event_floor_diagnostic": as_int(metric_value(path, "phase282_min_event_floor_diagnostic", 0)),
            "min_events_for_robust_portfolio_claim": as_int(metric_value(path, "phase282_min_events_for_robust_portfolio_claim", 0)),
            "cost200_required": as_int(metric_value(path, "phase282_cost200_required", 0)),
            "fixed_capital_required": as_int(metric_value(path, "phase282_fixed_capital_required", 0)),
            "full_depth_required": as_int(metric_value(path, "phase282_full_depth_required", 0)),
            "l1_only_allowed": as_int(metric_value(path, "phase282_l1_only_allowed", 1)),
            "net_edge_live_mask_allowed": as_int(metric_value(path, "phase282_net_edge_live_mask_allowed", 1)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase282_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase282_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase282_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase282_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase282_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase282_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase282_next_best_action", ""),
        }
    if phase == 283:
        complete = as_int(metric_value(path, "phase283_regime_conditioned_ensemble_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "regime_conditioned_full_depth_ensemble_interpretation_open" if complete else "phase283_regime_conditioned_ensemble_search_gated",
            "regime_conditioned_ensemble_search_complete": complete,
            "selected_route": metric_value(path, "phase283_selected_route", ""),
            "seed_rows": as_int(metric_value(path, "phase283_seed_rows", 0)),
            "variant_rows": as_int(metric_value(path, "phase283_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase283_scenario_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase283_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase283_robust_portfolio_floor_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase283_best_variant_id", ""),
            "best_ensemble_family": metric_value(path, "phase283_best_ensemble_family", ""),
            "best_bucket_id": metric_value(path, "phase283_best_bucket_id", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase283_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase283_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase283_best_scheduled_event_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase283_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase283_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase283_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase283_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase283_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase283_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase283_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase283_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase283_next_best_action", ""),
        }
    if phase == 284:
        complete = as_int(metric_value(path, "phase284_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_lifecycle_exit_side_redesign_precommit_open" if complete else "phase284_ensemble_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase284_selected_next_route", ""),
            "phase283_seed_rows": as_int(metric_value(path, "phase284_phase283_seed_rows", 0)),
            "phase283_variant_rows": as_int(metric_value(path, "phase284_phase283_variant_rows", 0)),
            "phase283_scenario_rows": as_int(metric_value(path, "phase284_phase283_scenario_rows", 0)),
            "phase283_sparse_above12_scenario_rows": as_int(metric_value(path, "phase284_phase283_sparse_above12_scenario_rows", 0)),
            "phase283_robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase284_phase283_robust_portfolio_floor_scenario_rows", 0)),
            "phase283_best_cost200_annualized_pct": metric_value(path, "phase284_phase283_best_cost200_annualized_pct", ""),
            "phase283_best_realized_net_pnl_inr": metric_value(path, "phase284_phase283_best_realized_net_pnl_inr", ""),
            "phase283_best_scheduled_event_rows": as_int(metric_value(path, "phase284_phase283_best_scheduled_event_rows", 0)),
            "positive_full_depth_clue_variant_rows": as_int(metric_value(path, "phase284_positive_full_depth_clue_variant_rows", 0)),
            "near_miss_variant_rows": as_int(metric_value(path, "phase284_near_miss_variant_rows", 0)),
            "close_phase283_for_acceptance": as_int(metric_value(path, "phase284_close_phase283_for_acceptance", 0)),
            "best_preserved_clue_variant": metric_value(path, "phase284_best_preserved_clue_variant", ""),
            "best_preserved_clue_family": metric_value(path, "phase284_best_preserved_clue_family", ""),
            "best_preserved_clue_bucket": metric_value(path, "phase284_best_preserved_clue_bucket", ""),
            "do_not_relax_cost_threshold": as_int(metric_value(path, "phase284_do_not_relax_cost_threshold", 0)),
            "do_not_claim_portfolio_return": as_int(metric_value(path, "phase284_do_not_claim_portfolio_return", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase284_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase284_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase284_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase284_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase284_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase284_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase284_next_best_action", ""),
        }
    if phase == 285:
        complete = as_int(metric_value(path, "phase285_lifecycle_redesign_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_lifecycle_exit_side_redesign_search_open" if complete else "phase285_lifecycle_redesign_precommit_gated",
            "lifecycle_redesign_precommit_complete": complete,
            "selected_route": metric_value(path, "phase285_selected_route", ""),
            "preserved_phase283_clue_rows": as_int(metric_value(path, "phase285_preserved_phase283_clue_rows", 0)),
            "phase286_lifecycle_seed_rows": as_int(metric_value(path, "phase285_phase286_lifecycle_seed_rows", 0)),
            "event_universe_rows": as_int(metric_value(path, "phase285_event_universe_rows", 0)),
            "event_universe_dates": as_int(metric_value(path, "phase285_event_universe_dates", 0)),
            "event_universe_symbols": as_int(metric_value(path, "phase285_event_universe_symbols", 0)),
            "phase283_scheduled_rows": as_int(metric_value(path, "phase285_phase283_scheduled_rows", 0)),
            "phase283_rejected_same_symbol_overlap_rows": as_int(metric_value(path, "phase285_phase283_rejected_same_symbol_overlap_rows", 0)),
            "phase283_rejected_max_concurrent_rows": as_int(metric_value(path, "phase285_phase283_rejected_max_concurrent_rows", 0)),
            "lifecycle_family_rows": as_int(metric_value(path, "phase285_lifecycle_family_rows", 0)),
            "phase286_allowed_lifecycle_family_rows": as_int(metric_value(path, "phase285_phase286_allowed_lifecycle_family_rows", 0)),
            "entry_exit_grid_rows": as_int(metric_value(path, "phase285_entry_exit_grid_rows", 0)),
            "capital_cost_contract_rows": as_int(metric_value(path, "phase285_capital_cost_contract_rows", 0)),
            "cost200_required": as_int(metric_value(path, "phase285_cost200_required", 0)),
            "fixed_capital_required": as_int(metric_value(path, "phase285_fixed_capital_required", 0)),
            "sparse_diagnostic_event_floor": as_int(metric_value(path, "phase285_sparse_diagnostic_event_floor", 0)),
            "robust_portfolio_event_floor": as_int(metric_value(path, "phase285_robust_portfolio_event_floor", 0)),
            "full_depth_required": as_int(metric_value(path, "phase285_full_depth_required", 0)),
            "beyond_l1_features_required": as_int(metric_value(path, "phase285_beyond_l1_features_required", 0)),
            "l1_only_allowed": as_int(metric_value(path, "phase285_l1_only_allowed", 0)),
            "net_edge_live_mask_allowed": as_int(metric_value(path, "phase285_net_edge_live_mask_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase285_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase285_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase285_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase285_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase285_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase285_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase285_next_best_action", ""),
        }
    if phase == 286:
        complete = as_int(metric_value(path, "phase286_lifecycle_redesign_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_lifecycle_exit_side_redesign_interpretation_open" if complete else "phase286_lifecycle_redesign_search_gated",
            "lifecycle_redesign_search_complete": complete,
            "selected_route": metric_value(path, "phase286_selected_route", ""),
            "variant_rows": as_int(metric_value(path, "phase286_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase286_scenario_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase286_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase286_robust_portfolio_floor_scenario_rows", 0)),
            "robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase286_robust_portfolio_above12_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase286_best_variant_id", ""),
            "best_lifecycle_family": metric_value(path, "phase286_best_lifecycle_family", ""),
            "best_grid_id": metric_value(path, "phase286_best_grid_id", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase286_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase286_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase286_best_scheduled_event_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase286_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase286_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase286_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase286_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase286_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase286_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase286_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase286_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase286_next_best_action", ""),
        }
    if phase == 287:
        complete = as_int(metric_value(path, "phase287_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_pressure_strategy_search_open" if complete else "phase287_lifecycle_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase287_selected_next_route", ""),
            "phase286_variant_rows": as_int(metric_value(path, "phase287_phase286_variant_rows", 0)),
            "phase286_scenario_rows": as_int(metric_value(path, "phase287_phase286_scenario_rows", 0)),
            "phase286_sparse_above12_scenario_rows": as_int(metric_value(path, "phase287_phase286_sparse_above12_scenario_rows", 0)),
            "phase286_robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase287_phase286_robust_portfolio_floor_scenario_rows", 0)),
            "phase286_robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase287_phase286_robust_portfolio_above12_scenario_rows", 0)),
            "best_phase286_variant_id": metric_value(path, "phase287_best_phase286_variant_id", ""),
            "best_lifecycle_family": metric_value(path, "phase287_best_lifecycle_family", ""),
            "best_grid_id": metric_value(path, "phase287_best_grid_id", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase287_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase287_best_scheduled_event_rows", 0)),
            "positive_full_depth_clue_variant_rows": as_int(metric_value(path, "phase287_positive_full_depth_clue_variant_rows", 0)),
            "close_phase286_for_acceptance": as_int(metric_value(path, "phase287_close_phase286_for_acceptance", 0)),
            "do_not_relax_annualized_denominator": as_int(metric_value(path, "phase287_do_not_relax_annualized_denominator", 0)),
            "do_not_claim_portfolio_return": as_int(metric_value(path, "phase287_do_not_claim_portfolio_return", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase287_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase287_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase287_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase287_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase287_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase287_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase287_next_best_action", ""),
        }
    if phase == 288:
        complete = as_int(metric_value(path, "phase288_liquidity_pressure_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_liquidity_pressure_interpretation_open" if complete else "phase288_liquidity_pressure_search_gated",
            "liquidity_pressure_search_complete": complete,
            "selected_route": metric_value(path, "phase288_selected_route", ""),
            "variant_rows": as_int(metric_value(path, "phase288_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase288_scenario_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase288_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase288_robust_portfolio_floor_scenario_rows", 0)),
            "robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase288_robust_portfolio_above12_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase288_best_variant_id", ""),
            "best_liquidity_family": metric_value(path, "phase288_best_liquidity_family", ""),
            "best_pressure_column": metric_value(path, "phase288_best_pressure_column", ""),
            "best_side_mode": metric_value(path, "phase288_best_side_mode", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase288_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase288_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase288_best_scheduled_event_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase288_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase288_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase288_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase288_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase288_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase288_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase288_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase288_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase288_next_best_action", ""),
        }
    if phase == 289:
        complete = as_int(metric_value(path, "phase289_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "adaptive_full_depth_liquidity_pressure_expansion_search_open" if complete else "phase289_liquidity_pressure_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase289_selected_next_route", ""),
            "phase288_variant_rows": as_int(metric_value(path, "phase289_phase288_variant_rows", 0)),
            "phase288_scenario_rows": as_int(metric_value(path, "phase289_phase288_scenario_rows", 0)),
            "phase288_sparse_above12_scenario_rows": as_int(metric_value(path, "phase289_phase288_sparse_above12_scenario_rows", 0)),
            "phase288_robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase289_phase288_robust_portfolio_floor_scenario_rows", 0)),
            "phase288_robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase289_phase288_robust_portfolio_above12_scenario_rows", 0)),
            "best_phase288_variant_id": metric_value(path, "phase289_best_phase288_variant_id", ""),
            "best_liquidity_family": metric_value(path, "phase289_best_liquidity_family", ""),
            "best_pressure_column": metric_value(path, "phase289_best_pressure_column", ""),
            "best_side_mode": metric_value(path, "phase289_best_side_mode", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase289_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase289_best_scheduled_event_rows", 0)),
            "positive_full_depth_clue_variant_rows": as_int(metric_value(path, "phase289_positive_full_depth_clue_variant_rows", 0)),
            "close_phase288_for_acceptance": as_int(metric_value(path, "phase289_close_phase288_for_acceptance", 0)),
            "do_not_relax_annualized_denominator": as_int(metric_value(path, "phase289_do_not_relax_annualized_denominator", 0)),
            "do_not_claim_portfolio_return": as_int(metric_value(path, "phase289_do_not_claim_portfolio_return", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase289_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase289_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase289_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase289_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase289_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase289_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase289_next_best_action", ""),
        }
    if phase == 290:
        complete = as_int(metric_value(path, "phase290_adaptive_liquidity_pressure_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "adaptive_full_depth_liquidity_pressure_interpretation_open" if complete else "phase290_adaptive_liquidity_pressure_search_gated",
            "adaptive_liquidity_pressure_search_complete": complete,
            "selected_route": metric_value(path, "phase290_selected_route", ""),
            "variant_rows": as_int(metric_value(path, "phase290_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase290_scenario_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase290_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase290_robust_portfolio_floor_scenario_rows", 0)),
            "robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase290_robust_portfolio_above12_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase290_best_variant_id", ""),
            "best_adaptive_family": metric_value(path, "phase290_best_adaptive_family", ""),
            "best_primary_pressure_column": metric_value(path, "phase290_best_primary_pressure_column", ""),
            "best_interaction_column": metric_value(path, "phase290_best_interaction_column", ""),
            "best_side_mode": metric_value(path, "phase290_best_side_mode", ""),
            "best_market_bucket": metric_value(path, "phase290_best_market_bucket", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase290_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase290_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase290_best_scheduled_event_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase290_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase290_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase290_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase290_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase290_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase290_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase290_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase290_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase290_next_best_action", ""),
        }
    if phase == 291:
        complete = as_int(metric_value(path, "phase291_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "adaptive_pressure_breadth_repair_search_open" if complete else "phase291_adaptive_pressure_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase291_selected_next_route", ""),
            "phase290_variant_rows": as_int(metric_value(path, "phase291_phase290_variant_rows", 0)),
            "phase290_scenario_rows": as_int(metric_value(path, "phase291_phase290_scenario_rows", 0)),
            "phase290_sparse_above12_scenario_rows": as_int(metric_value(path, "phase291_phase290_sparse_above12_scenario_rows", 0)),
            "phase290_robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase291_phase290_robust_portfolio_floor_scenario_rows", 0)),
            "phase290_robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase291_phase290_robust_portfolio_above12_scenario_rows", 0)),
            "best_phase290_variant_id": metric_value(path, "phase291_best_phase290_variant_id", ""),
            "best_adaptive_family": metric_value(path, "phase291_best_adaptive_family", ""),
            "best_primary_pressure_column": metric_value(path, "phase291_best_primary_pressure_column", ""),
            "best_interaction_column": metric_value(path, "phase291_best_interaction_column", ""),
            "best_side_mode": metric_value(path, "phase291_best_side_mode", ""),
            "best_market_bucket": metric_value(path, "phase291_best_market_bucket", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase291_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase291_best_scheduled_event_rows", 0)),
            "above12_but_too_sparse_variant_rows": as_int(metric_value(path, "phase291_above12_but_too_sparse_variant_rows", 0)),
            "close_phase290_for_acceptance": as_int(metric_value(path, "phase291_close_phase290_for_acceptance", 0)),
            "do_not_relax_annualized_denominator": as_int(metric_value(path, "phase291_do_not_relax_annualized_denominator", 0)),
            "do_not_claim_portfolio_return": as_int(metric_value(path, "phase291_do_not_claim_portfolio_return", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase291_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase291_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase291_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase291_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase291_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase291_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase291_next_best_action", ""),
        }
    if phase == 292:
        complete = as_int(metric_value(path, "phase292_breadth_repair_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "adaptive_pressure_breadth_repair_interpretation_open" if complete else "phase292_breadth_repair_search_gated",
            "breadth_repair_search_complete": complete,
            "selected_route": metric_value(path, "phase292_selected_route", ""),
            "variant_rows": as_int(metric_value(path, "phase292_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase292_scenario_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase292_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase292_robust_portfolio_floor_scenario_rows", 0)),
            "robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase292_robust_portfolio_above12_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase292_best_variant_id", ""),
            "best_repair_family": metric_value(path, "phase292_best_repair_family", ""),
            "best_side_mode": metric_value(path, "phase292_best_side_mode", ""),
            "best_market_bucket": metric_value(path, "phase292_best_market_bucket", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase292_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase292_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase292_best_scheduled_event_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase292_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase292_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase292_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase292_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase292_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase292_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase292_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase292_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase292_next_best_action", ""),
        }
    if phase == 293:
        complete = as_int(metric_value(path, "phase293_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_pressure_absorption_continuation_search_open" if complete else "phase293_breadth_repair_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase293_selected_next_route", ""),
            "phase292_variant_rows": as_int(metric_value(path, "phase293_phase292_variant_rows", 0)),
            "phase292_scenario_rows": as_int(metric_value(path, "phase293_phase292_scenario_rows", 0)),
            "phase292_sparse_above12_scenario_rows": as_int(metric_value(path, "phase293_phase292_sparse_above12_scenario_rows", 0)),
            "phase292_robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase293_phase292_robust_portfolio_floor_scenario_rows", 0)),
            "phase292_robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase293_phase292_robust_portfolio_above12_scenario_rows", 0)),
            "best_phase292_variant_id": metric_value(path, "phase293_best_phase292_variant_id", ""),
            "best_repair_family": metric_value(path, "phase293_best_repair_family", ""),
            "best_side_mode": metric_value(path, "phase293_best_side_mode", ""),
            "best_market_bucket": metric_value(path, "phase293_best_market_bucket", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase293_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase293_best_scheduled_event_rows", 0)),
            "positive_but_below12_variant_rows": as_int(metric_value(path, "phase293_positive_but_below12_variant_rows", 0)),
            "close_phase292_for_acceptance": as_int(metric_value(path, "phase293_close_phase292_for_acceptance", 0)),
            "close_same_contrarian_repair_family": as_int(metric_value(path, "phase293_close_same_contrarian_repair_family", 0)),
            "do_not_relax_annualized_denominator": as_int(metric_value(path, "phase293_do_not_relax_annualized_denominator", 0)),
            "do_not_lower_cost_or_event_floor": as_int(metric_value(path, "phase293_do_not_lower_cost_or_event_floor", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase293_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase293_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase293_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase293_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase293_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase293_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase293_next_best_action", ""),
        }
    if phase == 294:
        complete = as_int(metric_value(path, "phase294_continuation_search_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_depth_pressure_absorption_continuation_interpretation_open" if complete else "phase294_continuation_search_gated",
            "continuation_search_complete": complete,
            "selected_route": metric_value(path, "phase294_selected_route", ""),
            "variant_rows": as_int(metric_value(path, "phase294_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase294_scenario_rows", 0)),
            "family_rows": as_int(metric_value(path, "phase294_family_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase294_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase294_robust_portfolio_floor_scenario_rows", 0)),
            "robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase294_robust_portfolio_above12_scenario_rows", 0)),
            "discovery_survivor_variant_rows": as_int(metric_value(path, "phase294_discovery_survivor_variant_rows", 0)),
            "robust_survivor_variant_rows": as_int(metric_value(path, "phase294_robust_survivor_variant_rows", 0)),
            "best_variant_id": metric_value(path, "phase294_best_variant_id", ""),
            "best_continuation_family": metric_value(path, "phase294_best_continuation_family", ""),
            "best_side_mode": metric_value(path, "phase294_best_side_mode", ""),
            "best_market_bucket": metric_value(path, "phase294_best_market_bucket", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase294_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase294_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase294_best_scheduled_event_rows", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase294_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase294_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase294_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase294_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase294_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase294_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase294_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase294_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase294_next_best_action", ""),
        }
    if phase == 295:
        complete = as_int(metric_value(path, "phase295_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_year_top5_depth_strategy_family_sweep_open" if complete else "phase295_continuation_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase295_selected_next_route", ""),
            "phase294_variant_rows": as_int(metric_value(path, "phase295_phase294_variant_rows", 0)),
            "phase294_scenario_rows": as_int(metric_value(path, "phase295_phase294_scenario_rows", 0)),
            "phase294_family_rows": as_int(metric_value(path, "phase295_phase294_family_rows", 0)),
            "phase294_sparse_above12_scenario_rows": as_int(metric_value(path, "phase295_phase294_sparse_above12_scenario_rows", 0)),
            "phase294_robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase295_phase294_robust_portfolio_floor_scenario_rows", 0)),
            "phase294_robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase295_phase294_robust_portfolio_above12_scenario_rows", 0)),
            "best_phase294_variant_id": metric_value(path, "phase295_best_phase294_variant_id", ""),
            "best_continuation_family": metric_value(path, "phase295_best_continuation_family", ""),
            "best_side_mode": metric_value(path, "phase295_best_side_mode", ""),
            "best_market_bucket": metric_value(path, "phase295_best_market_bucket", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase295_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase295_best_scheduled_event_rows", 0)),
            "positive_but_below12_variant_rows": as_int(metric_value(path, "phase295_positive_but_below12_variant_rows", 0)),
            "close_phase294_for_acceptance": as_int(metric_value(path, "phase295_close_phase294_for_acceptance", 0)),
            "close_phase277_event_universe_for_minor_repairs": as_int(metric_value(path, "phase295_close_phase277_event_universe_for_minor_repairs", 0)),
            "do_not_relax_annualized_denominator": as_int(metric_value(path, "phase295_do_not_relax_annualized_denominator", 0)),
            "do_not_lower_cost_or_event_floor": as_int(metric_value(path, "phase295_do_not_lower_cost_or_event_floor", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase295_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase295_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase295_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase295_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase295_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase295_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase295_next_best_action", ""),
        }
    if phase == 296:
        complete = as_int(metric_value(path, "phase296_full_year_sweep_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "full_year_top5_depth_strategy_family_sweep_interpretation_open" if complete else "phase296_full_year_top5_depth_strategy_family_sweep_gated",
            "full_year_sweep_complete": complete,
            "selected_route": metric_value(path, "phase296_selected_route", ""),
            "input_rows": as_int(metric_value(path, "phase296_input_rows", 0)),
            "input_trade_dates": as_int(metric_value(path, "phase296_input_trade_dates", 0)),
            "input_symbols": as_int(metric_value(path, "phase296_input_symbols", 0)),
            "input_feed_profiles": as_int(metric_value(path, "phase296_input_feed_profiles", 0)),
            "variant_rows": as_int(metric_value(path, "phase296_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase296_scenario_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase296_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase296_robust_portfolio_floor_scenario_rows", 0)),
            "robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase296_robust_portfolio_above12_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase296_best_variant_id", ""),
            "best_strategy_family": metric_value(path, "phase296_best_strategy_family", ""),
            "best_feed_profile": metric_value(path, "phase296_best_feed_profile", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase296_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase296_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase296_best_scheduled_event_rows", 0)),
            "best_observed_trade_dates": as_int(metric_value(path, "phase296_best_observed_trade_dates", 0)),
            "annualized_denominator": metric_value(path, "phase296_annualized_denominator", ""),
            "l1_only_variant_rows": as_int(metric_value(path, "phase296_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase296_net_edge_live_mask_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase296_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase296_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase296_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase296_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase296_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase296_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase296_next_best_action", ""),
        }
    if phase == 297:
        complete = as_int(metric_value(path, "phase297_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "raw_dense_top5_book_state_strategy_sweep_open" if complete else "phase297_full_year_top5_depth_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase297_selected_next_route", ""),
            "phase296_input_rows": as_int(metric_value(path, "phase297_phase296_input_rows", 0)),
            "phase296_variant_rows": as_int(metric_value(path, "phase297_phase296_variant_rows", 0)),
            "phase296_scenario_rows": as_int(metric_value(path, "phase297_phase296_scenario_rows", 0)),
            "phase296_sparse_above12_scenario_rows": as_int(metric_value(path, "phase297_phase296_sparse_above12_scenario_rows", 0)),
            "phase296_robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase297_phase296_robust_portfolio_floor_scenario_rows", 0)),
            "phase296_robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase297_phase296_robust_portfolio_above12_scenario_rows", 0)),
            "best_phase296_variant_id": metric_value(path, "phase297_best_phase296_variant_id", ""),
            "best_strategy_family": metric_value(path, "phase297_best_strategy_family", ""),
            "best_feed_profile": metric_value(path, "phase297_best_feed_profile", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase297_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase297_best_scheduled_event_rows", 0)),
            "positive_but_below12_variant_rows": as_int(metric_value(path, "phase297_positive_but_below12_variant_rows", 0)),
            "raw_book_state_clue_variant_rows": as_int(metric_value(path, "phase297_raw_book_state_clue_variant_rows", 0)),
            "family_rows": as_int(metric_value(path, "phase297_family_rows", 0)),
            "close_phase296_for_acceptance": as_int(metric_value(path, "phase297_close_phase296_for_acceptance", 0)),
            "close_phase42_proxy_sweep_for_direct_acceptance": as_int(metric_value(path, "phase297_close_phase42_proxy_sweep_for_direct_acceptance", 0)),
            "do_not_claim_portfolio_return": as_int(metric_value(path, "phase297_do_not_claim_portfolio_return", 0)),
            "do_not_relax_annualized_denominator": as_int(metric_value(path, "phase297_do_not_relax_annualized_denominator", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase297_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase297_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase297_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase297_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase297_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase297_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase297_next_best_action", ""),
        }
    if phase == 298:
        complete = as_int(metric_value(path, "phase298_raw_dense_sweep_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "raw_dense_top5_book_state_strategy_sweep_interpretation_open" if complete else "phase298_raw_dense_top5_book_state_strategy_sweep_gated",
            "raw_dense_sweep_complete": complete,
            "selected_route": metric_value(path, "phase298_selected_route", ""),
            "symbol_rows": as_int(metric_value(path, "phase298_symbol_rows", 0)),
            "trade_month_rows": as_int(metric_value(path, "phase298_trade_month_rows", 0)),
            "source_file_rows": as_int(metric_value(path, "phase298_source_file_rows", 0)),
            "sample_stride": as_int(metric_value(path, "phase298_sample_stride", 0)),
            "sampled_dense_rows": as_int(metric_value(path, "phase298_sampled_dense_rows", 0)),
            "shard_trade_date_rows": as_int(metric_value(path, "phase298_shard_trade_date_rows", 0)),
            "raw_event_rows": as_int(metric_value(path, "phase298_raw_event_rows", 0)),
            "variant_rows": as_int(metric_value(path, "phase298_variant_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase298_scenario_rows", 0)),
            "sparse_above12_scenario_rows": as_int(metric_value(path, "phase298_sparse_above12_scenario_rows", 0)),
            "robust_portfolio_floor_scenario_rows": as_int(metric_value(path, "phase298_robust_portfolio_floor_scenario_rows", 0)),
            "robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase298_robust_portfolio_above12_scenario_rows", 0)),
            "best_variant_id": metric_value(path, "phase298_best_variant_id", ""),
            "best_strategy_family": metric_value(path, "phase298_best_strategy_family", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase298_best_cost200_annualized_pct", ""),
            "best_realized_net_pnl_inr": metric_value(path, "phase298_best_realized_net_pnl_inr", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase298_best_scheduled_event_rows", 0)),
            "best_observed_trade_dates": as_int(metric_value(path, "phase298_best_observed_trade_dates", 0)),
            "raw_book_state_l1_l5_required": as_int(metric_value(path, "phase298_raw_book_state_l1_l5_required", 0)),
            "levels_2_to_5_required": as_int(metric_value(path, "phase298_levels_2_to_5_required", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase298_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase298_net_edge_live_mask_rows", 0)),
            "annualized_denominator": metric_value(path, "phase298_annualized_denominator", ""),
            "strategy_replay_allowed": as_int(metric_value(path, "phase298_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase298_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase298_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase298_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase298_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase298_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase298_next_best_action", ""),
        }
    if phase == 299:
        complete = as_int(metric_value(path, "phase299_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_aware_execution_hybrid_precommit_open" if complete else "phase299_raw_dense_top5_book_state_interpretation_gated",
            "interpretation_complete": complete,
            "selected_next_route": metric_value(path, "phase299_selected_next_route", ""),
            "phase298_variant_rows": as_int(metric_value(path, "phase299_phase298_variant_rows", 0)),
            "phase298_scenario_rows": as_int(metric_value(path, "phase299_phase298_scenario_rows", 0)),
            "phase298_sparse_above12_scenario_rows": as_int(metric_value(path, "phase299_phase298_sparse_above12_scenario_rows", 0)),
            "phase298_robust_portfolio_above12_scenario_rows": as_int(metric_value(path, "phase299_phase298_robust_portfolio_above12_scenario_rows", 0)),
            "best_phase298_variant_id": metric_value(path, "phase299_best_phase298_variant_id", ""),
            "best_strategy_family": metric_value(path, "phase299_best_strategy_family", ""),
            "best_cost200_annualized_pct": metric_value(path, "phase299_best_cost200_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase299_best_scheduled_event_rows", 0)),
            "above12_below_30_event_variant_rows": as_int(metric_value(path, "phase299_above12_below_30_event_variant_rows", 0)),
            "directional_signal_seed_rows": as_int(metric_value(path, "phase299_directional_signal_seed_rows", 0)),
            "close_phase298_for_direct_acceptance": as_int(metric_value(path, "phase299_close_phase298_for_direct_acceptance", 0)),
            "do_not_add_new_alpha_search_in_phase300": as_int(metric_value(path, "phase299_do_not_add_new_alpha_search_in_phase300", 0)),
            "require_passive_fill_model": as_int(metric_value(path, "phase299_require_passive_fill_model", 0)),
            "require_adverse_selection_penalty": as_int(metric_value(path, "phase299_require_adverse_selection_penalty", 0)),
            "require_forced_flatten_cost": as_int(metric_value(path, "phase299_require_forced_flatten_cost", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase299_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase299_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase299_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase299_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase299_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase299_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase299_next_best_action", ""),
        }
    if phase == 300:
        complete = as_int(metric_value(path, "phase300_precommit_complete", 0))
        execution_complete = as_int(metric_value(path, "phase300_execution_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "passive_aware_execution_hybrid_interpretation_open" if execution_complete else ("passive_aware_execution_hybrid_execution_open" if complete else "phase300_passive_aware_execution_precommit_gated"),
            "precommit_complete": complete,
            "execution_complete": execution_complete,
            "selected_route": metric_value(path, "phase300_selected_route", ""),
            "charter_rows": as_int(metric_value(path, "phase300_charter_rows", 0)),
            "input_registry_rows": as_int(metric_value(path, "phase300_input_registry_rows", 0)),
            "execution_work_order_rows": as_int(metric_value(path, "phase300_execution_work_order_rows", 0)),
            "directional_signal_seed_rows": as_int(metric_value(path, "phase300_directional_signal_seed_rows", 0)),
            "seed_variant_rows": as_int(metric_value(path, "phase300_seed_variant_rows", 0)),
            "seed_event_rows": as_int(metric_value(path, "phase300_seed_event_rows", 0)),
            "scenario_rows": as_int(metric_value(path, "phase300_scenario_rows", 0)),
            "fill_model_rows": as_int(metric_value(path, "phase300_fill_model_rows", 0)),
            "execution_policy_rows": as_int(metric_value(path, "phase300_execution_policy_rows", 0)),
            "raw_depth_schema_columns_present": as_int(metric_value(path, "phase300_raw_depth_schema_columns_present", 0)),
            "l1_only_variant_rows": as_int(metric_value(path, "phase300_l1_only_variant_rows", 0)),
            "net_edge_live_mask_rows": as_int(metric_value(path, "phase300_net_edge_live_mask_rows", 0)),
            "fill_model_required": as_int(metric_value(path, "phase300_fill_model_required", 0)),
            "adverse_selection_required": as_int(metric_value(path, "phase300_adverse_selection_required", 0)),
            "forced_flatten_cost_required": as_int(metric_value(path, "phase300_forced_flatten_cost_required", 0)),
            "cost200_required": as_int(metric_value(path, "phase300_cost200_required", 0)),
            "fixed_capital_required": as_int(metric_value(path, "phase300_fixed_capital_required", 0)),
            "results_generated": as_int(metric_value(path, "phase300_results_generated", 0)),
            "above12_scenario_rows": as_int(metric_value(path, "phase300_above12_scenario_rows", 0)),
            "event_floor_scenario_rows": as_int(metric_value(path, "phase300_event_floor_scenario_rows", 0)),
            "breadth_met_scenario_rows": as_int(metric_value(path, "phase300_breadth_met_scenario_rows", 0)),
            "cost200_acceptance_survivor_rows": as_int(metric_value(path, "phase300_cost200_acceptance_survivor_rows", 0)),
            "best_scenario_id": metric_value(path, "phase300_best_scenario_id", ""),
            "best_seed_scope": metric_value(path, "phase300_best_seed_scope", ""),
            "best_fill_model_id": metric_value(path, "phase300_best_fill_model_id", ""),
            "best_execution_policy_id": metric_value(path, "phase300_best_execution_policy_id", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase300_best_scheduled_event_rows", 0)),
            "best_scheduled_symbols": as_int(metric_value(path, "phase300_best_scheduled_symbols", 0)),
            "best_positive_trade_dates": as_int(metric_value(path, "phase300_best_positive_trade_dates", 0)),
            "best_realized_net_pnl_inr": metric_value(path, "phase300_best_realized_net_pnl_inr", ""),
            "best_annualized_pct": metric_value(path, "phase300_best_annualized_pct", ""),
            "best_avg_entry_fill_probability": metric_value(path, "phase300_best_avg_entry_fill_probability", ""),
            "best_passive_entry_fill_rows": as_int(metric_value(path, "phase300_best_passive_entry_fill_rows", 0)),
            "best_forced_flatten_rows": as_int(metric_value(path, "phase300_best_forced_flatten_rows", 0)),
            "kill_switch_triggered": as_int(metric_value(path, "phase300_kill_switch_triggered", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase300_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase300_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase300_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase300_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase300_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase300_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase300_next_best_action", ""),
        }
    if phase == 301:
        complete = as_int(metric_value(path, "phase301_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "terminal_retail_top5_l2_alpha_thesis_report_open" if complete else "phase301_passive_aware_execution_interpretation_gated",
            "interpretation_complete": complete,
            "selected_outcome": metric_value(path, "phase301_selected_outcome", ""),
            "phase300_scenario_rows": as_int(metric_value(path, "phase301_phase300_scenario_rows", 0)),
            "phase300_above12_scenario_rows": as_int(metric_value(path, "phase301_phase300_above12_scenario_rows", 0)),
            "phase300_event_floor_scenario_rows": as_int(metric_value(path, "phase301_phase300_event_floor_scenario_rows", 0)),
            "phase300_breadth_met_scenario_rows": as_int(metric_value(path, "phase301_phase300_breadth_met_scenario_rows", 0)),
            "phase300_cost200_acceptance_survivor_rows": as_int(metric_value(path, "phase301_phase300_cost200_acceptance_survivor_rows", 0)),
            "phase300_kill_switch_triggered": as_int(metric_value(path, "phase301_phase300_kill_switch_triggered", 0)),
            "best_scenario_id": metric_value(path, "phase301_best_scenario_id", ""),
            "best_annualized_pct": metric_value(path, "phase301_best_annualized_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase301_best_scheduled_event_rows", 0)),
            "broadest_scenario_id": metric_value(path, "phase301_broadest_scenario_id", ""),
            "broadest_annualized_pct": metric_value(path, "phase301_broadest_annualized_pct", ""),
            "broadest_scheduled_event_rows": as_int(metric_value(path, "phase301_broadest_scheduled_event_rows", 0)),
            "terminal_report_required": as_int(metric_value(path, "phase301_terminal_report_required", 0)),
            "do_not_rescue_with_more_filters": as_int(metric_value(path, "phase301_do_not_rescue_with_more_filters", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase301_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase301_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase301_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase301_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase301_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase301_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase301_next_best_action", ""),
        }
    if phase == 302:
        complete = as_int(metric_value(path, "phase302_terminal_report_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "retail_top5_l2_alpha_thesis_closed_terminal_report_complete" if complete else "phase302_terminal_report_gated",
            "terminal_report_complete": complete,
            "selected_verdict": metric_value(path, "phase302_selected_verdict", ""),
            "closed_scope": metric_value(path, "phase302_closed_scope", ""),
            "phase300_scenario_rows": as_int(metric_value(path, "phase302_phase300_scenario_rows", 0)),
            "phase300_above12_scenario_rows": as_int(metric_value(path, "phase302_phase300_above12_scenario_rows", 0)),
            "phase300_event_floor_scenario_rows": as_int(metric_value(path, "phase302_phase300_event_floor_scenario_rows", 0)),
            "phase300_breadth_met_scenario_rows": as_int(metric_value(path, "phase302_phase300_breadth_met_scenario_rows", 0)),
            "phase300_cost200_acceptance_survivor_rows": as_int(metric_value(path, "phase302_phase300_cost200_acceptance_survivor_rows", 0)),
            "phase300_kill_switch_triggered": as_int(metric_value(path, "phase302_phase300_kill_switch_triggered", 0)),
            "best_sparse_scenario_id": metric_value(path, "phase302_best_sparse_scenario_id", ""),
            "best_sparse_annualized_pct": metric_value(path, "phase302_best_sparse_annualized_pct", ""),
            "best_sparse_scheduled_event_rows": as_int(metric_value(path, "phase302_best_sparse_scheduled_event_rows", 0)),
            "broadest_scenario_id": metric_value(path, "phase302_broadest_scenario_id", ""),
            "broadest_annualized_pct": metric_value(path, "phase302_broadest_annualized_pct", ""),
            "broadest_scheduled_event_rows": as_int(metric_value(path, "phase302_broadest_scheduled_event_rows", 0)),
            "byproduct_rows": as_int(metric_value(path, "phase302_byproduct_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase302_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase302_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase302_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase302_deployable_profitability_claim_allowed", 0)),
            "material_new_source_or_thesis_required": as_int(metric_value(path, "phase302_material_new_source_or_thesis_required", 0)),
            "do_not_continue_same_route": as_int(metric_value(path, "phase302_do_not_continue_same_route", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase302_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase302_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase302_next_best_action", ""),
        }
    if phase == 303:
        complete = as_int(metric_value(path, "phase303_material_new_selector_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "material_new_event_catalyst_source_acquisition_open" if complete else "phase303_material_new_selector_gated",
            "material_new_selector_complete": complete,
            "selected_route": metric_value(path, "phase303_selected_route", ""),
            "candidate_rows": as_int(metric_value(path, "phase303_candidate_rows", 0)),
            "rejected_same_route_rows": as_int(metric_value(path, "phase303_rejected_same_route_rows", 0)),
            "selected_requires_external_source": as_int(metric_value(path, "phase303_selected_requires_external_source", 0)),
            "selected_uses_top_five_depth_levels_1_to_5": as_int(metric_value(path, "phase303_selected_uses_top_five_depth_levels_1_to_5", 0)),
            "work_order_rows": as_int(metric_value(path, "phase303_work_order_rows", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase303_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase303_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase303_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase303_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase303_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase303_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase303_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase303_next_best_action", ""),
        }
    if phase == 304:
        complete = as_int(metric_value(path, "phase304_source_acquisition_package_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_dropzone_population_open" if complete else "phase304_source_acquisition_package_gated",
            "source_acquisition_package_complete": complete,
            "required_schema_rows": as_int(metric_value(path, "phase304_required_schema_rows", 0)),
            "optional_schema_rows": as_int(metric_value(path, "phase304_optional_schema_rows", 0)),
            "dropzone_file_rows": as_int(metric_value(path, "phase304_dropzone_file_rows", 0)),
            "non_template_source_file_rows": as_int(metric_value(path, "phase304_non_template_source_file_rows", 0)),
            "external_event_rows_imported": as_int(metric_value(path, "phase304_external_event_rows_imported", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase304_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase304_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase304_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase304_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase304_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase304_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase304_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase304_next_best_action", ""),
        }
    if phase == 305:
        complete = as_int(metric_value(path, "phase305_event_catalyst_import_audit_complete", 0))
        imported_rows = as_int(metric_value(path, "phase305_imported_event_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_source_imported_join_precommit_open" if complete and imported_rows > 0 else ("event_catalyst_source_import_blocked_dropzone_unpopulated" if complete else "phase305_event_catalyst_import_audit_gated"),
            "event_catalyst_import_audit_complete": complete,
            "candidate_source_file_rows": as_int(metric_value(path, "phase305_candidate_source_file_rows", 0)),
            "candidate_source_raw_rows": as_int(metric_value(path, "phase305_candidate_source_raw_rows", 0)),
            "imported_event_rows": imported_rows,
            "issue_rows": as_int(metric_value(path, "phase305_issue_rows", 0)),
            "template_rows_imported": as_int(metric_value(path, "phase305_template_rows_imported", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase305_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase305_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase305_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase305_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase305_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase305_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase305_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase305_next_best_action", ""),
        }
    if phase == 306:
        complete = as_int(metric_value(path, "phase306_join_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_top5_depth_join_materialization_open" if complete else "phase306_event_catalyst_join_precommit_gated",
            "join_precommit_complete": complete,
            "imported_event_rows": as_int(metric_value(path, "phase306_imported_event_rows", 0)),
            "event_universe_rows": as_int(metric_value(path, "phase306_event_universe_rows", 0)),
            "event_rows_with_depth_month": as_int(metric_value(path, "phase306_event_rows_with_depth_month", 0)),
            "symbol_rows": as_int(metric_value(path, "phase306_symbol_rows", 0)),
            "pre_event_seconds": as_int(metric_value(path, "phase306_pre_event_seconds", 0)),
            "post_event_seconds": as_int(metric_value(path, "phase306_post_event_seconds", 0)),
            "event_bucket_seconds": as_int(metric_value(path, "phase306_event_bucket_seconds", 0)),
            "full_depth_levels_1_to_5_required": as_int(metric_value(path, "phase306_full_depth_levels_1_to_5_required", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase306_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase306_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase306_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase306_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase306_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase306_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase306_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase306_next_best_action", ""),
        }
    if phase == 307:
        complete = as_int(metric_value(path, "phase307_join_materialization_complete", 0))
        joined_rows = as_int(metric_value(path, "phase307_materialized_join_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_top5_depth_join_quality_audit_open" if complete and joined_rows > 0 else ("event_catalyst_top5_depth_join_blocked_no_timestamp_overlap" if complete else "phase307_join_materialization_gated"),
            "join_materialization_complete": complete,
            "work_order_rows": as_int(metric_value(path, "phase307_work_order_rows", 0)),
            "timestamp_overlap_rows": as_int(metric_value(path, "phase307_timestamp_overlap_rows", 0)),
            "materialized_join_rows": joined_rows,
            "materialized_symbols": as_int(metric_value(path, "phase307_materialized_symbols", 0)),
            "full_depth_columns_present": as_int(metric_value(path, "phase307_full_depth_columns_present", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase307_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase307_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase307_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase307_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase307_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase307_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase307_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase307_next_best_action", ""),
        }
    if phase == 308:
        complete = as_int(metric_value(path, "phase308_join_quality_audit_complete", 0))
        hard_issues = as_int(metric_value(path, "phase308_hard_issue_rows", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_feature_precommit_open" if complete and hard_issues == 0 else ("event_catalyst_join_quality_repair_required" if complete else "phase308_join_quality_audit_gated"),
            "join_quality_audit_complete": complete,
            "joined_rows": as_int(metric_value(path, "phase308_joined_rows", 0)),
            "materialized_event_rows": as_int(metric_value(path, "phase308_materialized_event_rows", 0)),
            "materialized_symbols": as_int(metric_value(path, "phase308_materialized_symbols", 0)),
            "symbol_quality_rows": as_int(metric_value(path, "phase308_symbol_quality_rows", 0)),
            "required_columns_present": as_int(metric_value(path, "phase308_required_columns_present", 0)),
            "full_depth_columns_present": as_int(metric_value(path, "phase308_full_depth_columns_present", 0)),
            "required_null_cells": as_int(metric_value(path, "phase308_required_null_cells", 0)),
            "hard_issue_rows": hard_issues,
            "strategy_search_allowed_now": as_int(metric_value(path, "phase308_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase308_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase308_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase308_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase308_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase308_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase308_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase308_next_best_action", ""),
        }
    if phase == 309:
        complete = as_int(metric_value(path, "phase309_event_feature_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_feature_materialization_open" if complete else "phase309_event_feature_precommit_gated",
            "event_feature_precommit_complete": complete,
            "feature_catalog_rows": as_int(metric_value(path, "phase309_feature_catalog_rows", 0)),
            "depth_beyond_l1_feature_rows": as_int(metric_value(path, "phase309_depth_beyond_l1_feature_rows", 0)),
            "materialization_contract_rows": as_int(metric_value(path, "phase309_materialization_contract_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase309_full_depth_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase309_l1_only_candidate_allowed", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase309_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase309_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase309_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase309_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase309_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase309_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase309_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase309_next_best_action", ""),
        }
    if phase == 310:
        complete = as_int(metric_value(path, "phase310_event_feature_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_strategy_search_precommit_open" if complete else "phase310_event_feature_materialization_gated",
            "event_feature_materialization_complete": complete,
            "feature_matrix_rows": as_int(metric_value(path, "phase310_feature_matrix_rows", 0)),
            "materialized_event_rows": as_int(metric_value(path, "phase310_materialized_event_rows", 0)),
            "materialized_symbols": as_int(metric_value(path, "phase310_materialized_symbols", 0)),
            "quality_rows": as_int(metric_value(path, "phase310_quality_rows", 0)),
            "quality_pass_rows": as_int(metric_value(path, "phase310_quality_pass_rows", 0)),
            "full_depth_features_materialized": as_int(metric_value(path, "phase310_full_depth_features_materialized", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase310_strategy_search_allowed_now", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase310_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase310_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase310_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase310_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase310_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase310_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase310_next_best_action", ""),
        }
    if phase == 311:
        complete = as_int(metric_value(path, "phase311_strategy_search_precommit_complete", 0))
        execution_allowed = as_int(metric_value(path, "phase311_strategy_search_execution_allowed_next", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_training_strategy_search_open" if complete and execution_allowed == 1 else ("phase311_strategy_search_precommit_repair_required" if complete else "phase311_strategy_search_precommit_gated"),
            "strategy_search_precommit_complete": complete,
            "strategy_family_rows": as_int(metric_value(path, "phase311_strategy_family_rows", 0)),
            "search_grid_rows": as_int(metric_value(path, "phase311_search_grid_rows", 0)),
            "expanded_variant_upper_bound_rows": as_int(metric_value(path, "phase311_expanded_variant_upper_bound_rows", 0)),
            "capital_contract_rows": as_int(metric_value(path, "phase311_capital_contract_rows", 0)),
            "control_contract_rows": as_int(metric_value(path, "phase311_control_contract_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase311_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase311_depth_beyond_l1_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase311_l1_only_candidate_allowed", 0)),
            "strategy_search_execution_allowed_next": execution_allowed,
            "strategy_replay_allowed": as_int(metric_value(path, "phase311_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase311_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase311_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase311_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase311_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase311_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase311_next_best_action", ""),
        }
    if phase == 312:
        complete = as_int(metric_value(path, "phase312_strategy_search_training_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_training_strategy_search_interpretation_open" if complete else "phase312_training_strategy_search_gated",
            "strategy_search_training_complete": complete,
            "variant_rows": as_int(metric_value(path, "phase312_variant_rows", 0)),
            "positive_net_pnl_rows": as_int(metric_value(path, "phase312_positive_net_pnl_rows", 0)),
            "sparse_above12_annualized_rows": as_int(metric_value(path, "phase312_sparse_above12_annualized_rows", 0)),
            "best_scenario_id": metric_value(path, "phase312_best_scenario_id", ""),
            "best_annualized_return_pct_sparse": metric_value(path, "phase312_best_annualized_return_pct_sparse", ""),
            "best_net_pnl_inr": metric_value(path, "phase312_best_net_pnl_inr", ""),
            "best_scheduled_trade_rows": as_int(metric_value(path, "phase312_best_scheduled_trade_rows", 0)),
            "observed_trade_dates": as_int(metric_value(path, "phase312_observed_trade_dates", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase312_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase312_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase312_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase312_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase312_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase312_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase312_next_best_action", ""),
        }
    if phase == 313:
        complete = as_int(metric_value(path, "phase313_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_synthetic_breadth_precommit_open" if complete else "phase313_event_catalyst_interpretation_gated",
            "interpretation_complete": complete,
            "positive_sparse_leads_exist": as_int(metric_value(path, "phase313_positive_sparse_leads_exist", 0)),
            "cost_stress_sparse_leads_exist": as_int(metric_value(path, "phase313_cost_stress_sparse_leads_exist", 0)),
            "insufficient_event_breadth_for_acceptance": as_int(metric_value(path, "phase313_insufficient_event_breadth_for_acceptance", 0)),
            "insufficient_trade_breadth_for_acceptance": as_int(metric_value(path, "phase313_insufficient_trade_breadth_for_acceptance", 0)),
            "replay_allowed": as_int(metric_value(path, "phase313_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase313_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase313_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase313_deployable_profitability_claim_allowed", 0)),
            "selected_next_route": metric_value(path, "phase313_selected_next_route", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase313_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase313_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase313_next_best_action", ""),
        }
    if phase == 314:
        complete = as_int(metric_value(path, "phase314_multievent_breadth_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_synthetic_breadth_materialization_open" if complete else "phase314_multievent_breadth_precommit_gated",
            "multievent_breadth_precommit_complete": complete,
            "breadth_contract_rows": as_int(metric_value(path, "phase314_breadth_contract_rows", 0)),
            "generation_work_order_rows": as_int(metric_value(path, "phase314_generation_work_order_rows", 0)),
            "control_rows": as_int(metric_value(path, "phase314_control_rows", 0)),
            "min_synthetic_event_dates": as_int(metric_value(path, "phase314_min_synthetic_event_dates", 0)),
            "min_symbols_per_event": as_int(metric_value(path, "phase314_min_symbols_per_event", 0)),
            "full_depth_required": as_int(metric_value(path, "phase314_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase314_depth_beyond_l1_required", 0)),
            "replay_allowed": as_int(metric_value(path, "phase314_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase314_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase314_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase314_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase314_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase314_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase314_next_best_action", ""),
        }
    if phase == 315:
        complete = as_int(metric_value(path, "phase315_multievent_synthetic_breadth_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_top5_depth_join_precommit_open" if complete else "phase315_multievent_breadth_materialization_gated",
            "multievent_breadth_materialization_complete": complete,
            "generated_event_rows": as_int(metric_value(path, "phase315_generated_event_rows", 0)),
            "distinct_event_dates": as_int(metric_value(path, "phase315_distinct_event_dates", 0)),
            "min_symbols_per_event": as_int(metric_value(path, "phase315_min_symbols_per_event", 0)),
            "event_symbol_work_order_rows": as_int(metric_value(path, "phase315_event_symbol_work_order_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase315_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase315_depth_beyond_l1_required", 0)),
            "replay_allowed": as_int(metric_value(path, "phase315_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase315_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase315_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase315_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase315_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase315_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase315_next_best_action", ""),
        }
    if phase == 316:
        complete = as_int(metric_value(path, "phase316_multievent_top5_depth_join_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_top5_depth_join_materialization_open" if complete else "phase316_multievent_top5_depth_join_precommit_gated",
            "multievent_top5_depth_join_precommit_complete": complete,
            "generated_event_rows": as_int(metric_value(path, "phase316_generated_event_rows", 0)),
            "event_symbol_work_order_rows": as_int(metric_value(path, "phase316_event_symbol_work_order_rows", 0)),
            "min_symbols_per_event": as_int(metric_value(path, "phase316_min_symbols_per_event", 0)),
            "join_contract_rows": as_int(metric_value(path, "phase316_join_contract_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase316_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase316_depth_beyond_l1_required", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase316_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase316_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase316_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase316_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase316_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase316_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase316_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase316_next_best_action", ""),
        }
    if phase == 317:
        complete = as_int(metric_value(path, "phase317_multievent_top5_depth_join_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_join_quality_audit_open" if complete else "phase317_multievent_top5_depth_join_materialization_gated",
            "multievent_top5_depth_join_materialization_complete": complete,
            "work_order_rows": as_int(metric_value(path, "phase317_work_order_rows", 0)),
            "timestamp_overlap_rows": as_int(metric_value(path, "phase317_timestamp_overlap_rows", 0)),
            "materialized_join_rows": as_int(metric_value(path, "phase317_materialized_join_rows", 0)),
            "materialized_events": as_int(metric_value(path, "phase317_materialized_events", 0)),
            "materialized_symbols": as_int(metric_value(path, "phase317_materialized_symbols", 0)),
            "row_groups_read": as_int(metric_value(path, "phase317_row_groups_read", 0)),
            "full_depth_columns_present": as_int(metric_value(path, "phase317_full_depth_columns_present", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase317_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase317_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase317_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase317_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase317_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase317_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase317_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase317_next_best_action", ""),
        }
    if phase == 318:
        complete = as_int(metric_value(path, "phase318_multievent_join_quality_audit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_feature_materialization_precommit_open" if complete else "phase318_multievent_join_quality_audit_gated",
            "multievent_join_quality_audit_complete": complete,
            "joined_rows": as_int(metric_value(path, "phase318_joined_rows", 0)),
            "event_rows": as_int(metric_value(path, "phase318_event_rows", 0)),
            "symbol_rows": as_int(metric_value(path, "phase318_symbol_rows", 0)),
            "min_event_symbol_coverage": as_int(metric_value(path, "phase318_min_event_symbol_coverage", 0)),
            "min_symbol_event_coverage": as_int(metric_value(path, "phase318_min_symbol_event_coverage", 0)),
            "relative_second_min": as_int(metric_value(path, "phase318_relative_second_min", 0)),
            "relative_second_max": as_int(metric_value(path, "phase318_relative_second_max", 0)),
            "crossed_or_locked_l1_rows": as_int(metric_value(path, "phase318_crossed_or_locked_l1_rows", 0)),
            "bid_depth_sort_error_rows": as_int(metric_value(path, "phase318_bid_depth_sort_error_rows", 0)),
            "ask_depth_sort_error_rows": as_int(metric_value(path, "phase318_ask_depth_sort_error_rows", 0)),
            "depth_beyond_l1_material_rows": as_int(metric_value(path, "phase318_depth_beyond_l1_material_rows", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase318_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase318_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase318_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase318_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase318_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase318_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase318_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase318_next_best_action", ""),
        }
    if phase == 319:
        complete = as_int(metric_value(path, "phase319_multievent_feature_materialization_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_feature_materialization_open" if complete else "phase319_multievent_feature_materialization_precommit_gated",
            "multievent_feature_materialization_precommit_complete": complete,
            "feature_catalog_rows": as_int(metric_value(path, "phase319_feature_catalog_rows", 0)),
            "depth_beyond_l1_feature_rows": as_int(metric_value(path, "phase319_depth_beyond_l1_feature_rows", 0)),
            "lookahead_target_only_rows": as_int(metric_value(path, "phase319_lookahead_target_only_rows", 0)),
            "materialization_contract_rows": as_int(metric_value(path, "phase319_materialization_contract_rows", 0)),
            "processing_work_order_rows": as_int(metric_value(path, "phase319_processing_work_order_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase319_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase319_depth_beyond_l1_required", 0)),
            "l1_only_variant_rows_allowed": as_int(metric_value(path, "phase319_l1_only_variant_rows_allowed", 0)),
            "net_edge_live_mask_rows_allowed": as_int(metric_value(path, "phase319_net_edge_live_mask_rows_allowed", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase319_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase319_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase319_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase319_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase319_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase319_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase319_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase319_next_best_action", ""),
        }
    if phase == 320:
        complete = as_int(metric_value(path, "phase320_multievent_feature_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_strategy_search_precommit_open" if complete else "phase320_multievent_feature_materialization_gated",
            "multievent_feature_materialization_complete": complete,
            "feature_matrix_rows": as_int(metric_value(path, "phase320_feature_matrix_rows", 0)),
            "event_rows": as_int(metric_value(path, "phase320_event_rows", 0)),
            "symbol_rows": as_int(metric_value(path, "phase320_symbol_rows", 0)),
            "source_tick_rows": as_int(metric_value(path, "phase320_source_tick_rows", 0)),
            "min_source_tick_rows_per_event_symbol": as_int(metric_value(path, "phase320_min_source_tick_rows_per_event_symbol", 0)),
            "live_feature_columns": as_int(metric_value(path, "phase320_live_feature_columns", 0)),
            "depth_feature_columns": as_int(metric_value(path, "phase320_depth_feature_columns", 0)),
            "target_columns": as_int(metric_value(path, "phase320_target_columns", 0)),
            "live_feature_null_cells": as_int(metric_value(path, "phase320_live_feature_null_cells", 0)),
            "target_null_cells": as_int(metric_value(path, "phase320_target_null_cells", 0)),
            "target_columns_used_as_live_features": as_int(metric_value(path, "phase320_target_columns_used_as_live_features", 0)),
            "full_depth_required": as_int(metric_value(path, "phase320_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase320_depth_beyond_l1_required", 0)),
            "l1_only_variant_rows_allowed": as_int(metric_value(path, "phase320_l1_only_variant_rows_allowed", 0)),
            "net_edge_live_mask_rows_allowed": as_int(metric_value(path, "phase320_net_edge_live_mask_rows_allowed", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase320_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase320_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase320_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase320_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase320_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase320_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase320_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase320_next_best_action", ""),
        }
    if phase == 321:
        complete = as_int(metric_value(path, "phase321_multievent_strategy_search_precommit_complete", 0))
        execution_allowed = as_int(metric_value(path, "phase321_strategy_search_execution_allowed_next", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_training_strategy_search_open" if complete and execution_allowed == 1 else ("phase321_multievent_strategy_search_precommit_repair_required" if complete else "phase321_multievent_strategy_search_precommit_gated"),
            "multievent_strategy_search_precommit_complete": complete,
            "strategy_family_rows": as_int(metric_value(path, "phase321_strategy_family_rows", 0)),
            "depth_beyond_l1_family_rows": as_int(metric_value(path, "phase321_depth_beyond_l1_family_rows", 0)),
            "search_grid_rows": as_int(metric_value(path, "phase321_search_grid_rows", 0)),
            "expanded_variant_upper_bound_rows": as_int(metric_value(path, "phase321_expanded_variant_upper_bound_rows", 0)),
            "cost200_grid_rows": as_int(metric_value(path, "phase321_cost200_grid_rows", 0)),
            "passive_aware_grid_rows": as_int(metric_value(path, "phase321_passive_aware_grid_rows", 0)),
            "acceptance_contract_rows": as_int(metric_value(path, "phase321_acceptance_contract_rows", 0)),
            "work_order_rows": as_int(metric_value(path, "phase321_work_order_rows", 0)),
            "zerodha_cost_model_version": metric_value(path, "phase321_zerodha_cost_model_version", ""),
            "full_depth_required": as_int(metric_value(path, "phase321_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase321_depth_beyond_l1_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase321_l1_only_candidate_allowed", 0)),
            "net_edge_live_mask_rows_allowed": as_int(metric_value(path, "phase321_net_edge_live_mask_rows_allowed", 0)),
            "fixed_capital_required": as_int(metric_value(path, "phase321_fixed_capital_required", 0)),
            "cost200_required": as_int(metric_value(path, "phase321_cost200_required", 0)),
            "passive_realism_penalties_required": as_int(metric_value(path, "phase321_passive_realism_penalties_required", 0)),
            "strategy_search_execution_allowed_next": execution_allowed,
            "replay_allowed": as_int(metric_value(path, "phase321_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase321_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase321_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase321_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase321_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase321_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase321_next_best_action", ""),
        }
    if phase == 322:
        complete = as_int(metric_value(path, "phase322_multievent_strategy_search_training_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_multievent_strategy_search_interpretation_open" if complete else "phase322_multievent_strategy_search_training_gated",
            "multievent_strategy_search_training_complete": complete,
            "scenario_rows": as_int(metric_value(path, "phase322_scenario_rows", 0)),
            "family_rows": as_int(metric_value(path, "phase322_family_rows", 0)),
            "cost200_scenario_rows": as_int(metric_value(path, "phase322_cost200_scenario_rows", 0)),
            "passive_aware_scenario_rows": as_int(metric_value(path, "phase322_passive_aware_scenario_rows", 0)),
            "above12_annualized_scenario_rows": as_int(metric_value(path, "phase322_above12_annualized_scenario_rows", 0)),
            "cost200_above12_scenario_rows": as_int(metric_value(path, "phase322_cost200_above12_scenario_rows", 0)),
            "cost200_acceptance_grade_candidate_rows": as_int(metric_value(path, "phase322_cost200_acceptance_grade_candidate_rows", 0)),
            "best_scenario_id": metric_value(path, "phase322_best_scenario_id", ""),
            "best_family_id": metric_value(path, "phase322_best_family_id", ""),
            "best_execution_policy": metric_value(path, "phase322_best_execution_policy", ""),
            "best_cost_profile": metric_value(path, "phase322_best_cost_profile", ""),
            "best_annualized_return_pct": metric_value(path, "phase322_best_annualized_return_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase322_best_scheduled_event_rows", 0)),
            "best_cost200_annualized_return_pct": metric_value(path, "phase322_best_cost200_annualized_return_pct", ""),
            "best_cost200_scheduled_event_rows": as_int(metric_value(path, "phase322_best_cost200_scheduled_event_rows", 0)),
            "annualized_denominator": metric_value(path, "phase322_annualized_denominator", ""),
            "replay_allowed": as_int(metric_value(path, "phase322_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase322_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase322_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase322_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase322_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase322_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase322_next_best_action", ""),
        }
    if phase == 323:
        complete = as_int(metric_value(path, "phase323_multievent_strategy_search_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_breadth_expansion_precommit_open" if complete else "phase323_multievent_strategy_search_interpretation_gated",
            "multievent_strategy_search_interpretation_complete": complete,
            "fixed_capital_profitable_research_leads_exist": as_int(metric_value(path, "phase323_fixed_capital_profitable_research_leads_exist", 0)),
            "acceptance_grade_candidates_exist": as_int(metric_value(path, "phase323_acceptance_grade_candidates_exist", 0)),
            "best_2x_cost_lead_is_sparse": as_int(metric_value(path, "phase323_best_2x_cost_lead_is_sparse", 0)),
            "breadth_universe_limits_acceptance": as_int(metric_value(path, "phase323_breadth_universe_limits_acceptance", 0)),
            "best_family_preserved_for_breadth_expansion": metric_value(path, "phase323_best_family_preserved_for_breadth_expansion", ""),
            "passive_aware_rescue_status": metric_value(path, "phase323_passive_aware_rescue_status", ""),
            "replay_allowed": as_int(metric_value(path, "phase323_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase323_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase323_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase323_deployable_profitability_claim_allowed", 0)),
            "selected_next_route": metric_value(path, "phase323_selected_next_route", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase323_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase323_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase323_next_best_action", ""),
        }
    if phase == 324:
        complete = as_int(metric_value(path, "phase324_breadth_expansion_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_breadth_expansion_materialization_open" if complete else "phase324_breadth_expansion_precommit_gated",
            "breadth_expansion_precommit_complete": complete,
            "target_event_rows": as_int(metric_value(path, "phase324_target_event_rows", 0)),
            "minimum_event_rows": as_int(metric_value(path, "phase324_minimum_event_rows", 0)),
            "robust_event_floor": as_int(metric_value(path, "phase324_robust_event_floor", 0)),
            "min_symbols_per_event": as_int(metric_value(path, "phase324_min_symbols_per_event", 0)),
            "contract_rows": as_int(metric_value(path, "phase324_contract_rows", 0)),
            "work_order_rows": as_int(metric_value(path, "phase324_work_order_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase324_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase324_depth_beyond_l1_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase324_l1_only_candidate_allowed", 0)),
            "fixed_capital_required": as_int(metric_value(path, "phase324_fixed_capital_required", 0)),
            "cost200_required": as_int(metric_value(path, "phase324_cost200_required", 0)),
            "replay_allowed": as_int(metric_value(path, "phase324_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase324_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase324_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase324_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase324_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase324_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase324_next_best_action", ""),
        }
    if phase == 325:
        complete = as_int(metric_value(path, "phase325_breadth_expansion_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_top5_depth_join_precommit_open" if complete else "phase325_breadth_expansion_materialization_gated",
            "breadth_expansion_materialization_complete": complete,
            "generated_event_rows": as_int(metric_value(path, "phase325_generated_event_rows", 0)),
            "distinct_event_dates": as_int(metric_value(path, "phase325_distinct_event_dates", 0)),
            "min_symbols_per_event": as_int(metric_value(path, "phase325_min_symbols_per_event", 0)),
            "event_symbol_work_order_rows": as_int(metric_value(path, "phase325_event_symbol_work_order_rows", 0)),
            "target_event_rows": as_int(metric_value(path, "phase325_target_event_rows", 0)),
            "minimum_event_rows": as_int(metric_value(path, "phase325_minimum_event_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase325_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase325_depth_beyond_l1_required", 0)),
            "replay_allowed": as_int(metric_value(path, "phase325_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase325_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase325_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase325_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase325_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase325_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase325_next_best_action", ""),
        }
    if phase == 326:
        complete = as_int(metric_value(path, "phase326_expanded_top5_depth_join_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_top5_depth_join_materialization_open" if complete else "phase326_expanded_top5_depth_join_precommit_gated",
            "expanded_top5_depth_join_precommit_complete": complete,
            "generated_event_rows": as_int(metric_value(path, "phase326_generated_event_rows", 0)),
            "event_symbol_work_order_rows": as_int(metric_value(path, "phase326_event_symbol_work_order_rows", 0)),
            "min_symbols_per_event": as_int(metric_value(path, "phase326_min_symbols_per_event", 0)),
            "join_contract_rows": as_int(metric_value(path, "phase326_join_contract_rows", 0)),
            "target_event_rows": as_int(metric_value(path, "phase326_target_event_rows", 0)),
            "minimum_event_rows": as_int(metric_value(path, "phase326_minimum_event_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase326_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase326_depth_beyond_l1_required", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase326_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase326_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase326_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase326_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase326_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase326_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase326_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase326_next_best_action", ""),
        }
    if phase == 327:
        complete = as_int(metric_value(path, "phase327_expanded_top5_depth_join_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_join_quality_audit_open" if complete else "phase327_expanded_top5_depth_join_materialization_gated",
            "expanded_top5_depth_join_materialization_complete": complete,
            "work_order_rows": as_int(metric_value(path, "phase327_work_order_rows", 0)),
            "timestamp_overlap_rows": as_int(metric_value(path, "phase327_timestamp_overlap_rows", 0)),
            "materialized_join_rows": as_int(metric_value(path, "phase327_materialized_join_rows", 0)),
            "materialized_events": as_int(metric_value(path, "phase327_materialized_events", 0)),
            "materialized_symbols": as_int(metric_value(path, "phase327_materialized_symbols", 0)),
            "row_groups_read": as_int(metric_value(path, "phase327_row_groups_read", 0)),
            "full_depth_columns_present": as_int(metric_value(path, "phase327_full_depth_columns_present", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase327_depth_beyond_l1_required", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase327_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase327_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase327_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase327_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase327_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase327_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase327_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase327_next_best_action", ""),
        }
    if phase == 328:
        complete = as_int(metric_value(path, "phase328_expanded_join_quality_audit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_feature_materialization_precommit_open" if complete else "phase328_expanded_join_quality_audit_gated",
            "expanded_join_quality_audit_complete": complete,
            "joined_rows": as_int(metric_value(path, "phase328_joined_rows", 0)),
            "event_rows": as_int(metric_value(path, "phase328_event_rows", 0)),
            "symbol_rows": as_int(metric_value(path, "phase328_symbol_rows", 0)),
            "min_event_symbol_coverage": as_int(metric_value(path, "phase328_min_event_symbol_coverage", 0)),
            "min_symbol_event_coverage": as_int(metric_value(path, "phase328_min_symbol_event_coverage", 0)),
            "relative_second_min": as_int(metric_value(path, "phase328_relative_second_min", 0)),
            "relative_second_max": as_int(metric_value(path, "phase328_relative_second_max", 0)),
            "crossed_or_locked_l1_rows": as_int(metric_value(path, "phase328_crossed_or_locked_l1_rows", 0)),
            "bid_depth_sort_error_rows": as_int(metric_value(path, "phase328_bid_depth_sort_error_rows", 0)),
            "ask_depth_sort_error_rows": as_int(metric_value(path, "phase328_ask_depth_sort_error_rows", 0)),
            "depth_beyond_l1_material_rows": as_int(metric_value(path, "phase328_depth_beyond_l1_material_rows", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase328_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase328_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase328_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase328_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase328_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase328_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase328_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase328_next_best_action", ""),
        }
    if phase == 329:
        complete = as_int(metric_value(path, "phase329_expanded_feature_materialization_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_feature_materialization_open" if complete else "phase329_expanded_feature_materialization_precommit_gated",
            "expanded_feature_materialization_precommit_complete": complete,
            "feature_catalog_rows": as_int(metric_value(path, "phase329_feature_catalog_rows", 0)),
            "depth_beyond_l1_feature_rows": as_int(metric_value(path, "phase329_depth_beyond_l1_feature_rows", 0)),
            "lookahead_target_only_rows": as_int(metric_value(path, "phase329_lookahead_target_only_rows", 0)),
            "materialization_contract_rows": as_int(metric_value(path, "phase329_materialization_contract_rows", 0)),
            "processing_work_order_rows": as_int(metric_value(path, "phase329_processing_work_order_rows", 0)),
            "expected_feature_rows": as_int(metric_value(path, "phase329_expected_feature_rows", 0)),
            "full_depth_required": as_int(metric_value(path, "phase329_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase329_depth_beyond_l1_required", 0)),
            "l1_only_variant_rows_allowed": as_int(metric_value(path, "phase329_l1_only_variant_rows_allowed", 0)),
            "net_edge_live_mask_rows_allowed": as_int(metric_value(path, "phase329_net_edge_live_mask_rows_allowed", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase329_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase329_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase329_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase329_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase329_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase329_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase329_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase329_next_best_action", ""),
        }
    if phase == 330:
        complete = as_int(metric_value(path, "phase330_expanded_feature_materialization_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_strategy_search_precommit_open" if complete else "phase330_expanded_feature_materialization_gated",
            "expanded_feature_materialization_complete": complete,
            "feature_matrix_rows": as_int(metric_value(path, "phase330_feature_matrix_rows", 0)),
            "event_rows": as_int(metric_value(path, "phase330_event_rows", 0)),
            "symbol_rows": as_int(metric_value(path, "phase330_symbol_rows", 0)),
            "source_tick_rows": as_int(metric_value(path, "phase330_source_tick_rows", 0)),
            "min_source_tick_rows_per_event_symbol": as_int(metric_value(path, "phase330_min_source_tick_rows_per_event_symbol", 0)),
            "live_feature_columns": as_int(metric_value(path, "phase330_live_feature_columns", 0)),
            "depth_feature_columns": as_int(metric_value(path, "phase330_depth_feature_columns", 0)),
            "target_columns": as_int(metric_value(path, "phase330_target_columns", 0)),
            "live_feature_null_cells": as_int(metric_value(path, "phase330_live_feature_null_cells", 0)),
            "target_null_cells": as_int(metric_value(path, "phase330_target_null_cells", 0)),
            "target_columns_used_as_live_features": as_int(metric_value(path, "phase330_target_columns_used_as_live_features", 0)),
            "matrix_parquet_written": as_int(metric_value(path, "phase330_matrix_parquet_written", 0)),
            "matrix_parquet_bytes": as_int(metric_value(path, "phase330_matrix_parquet_bytes", 0)),
            "full_depth_required": as_int(metric_value(path, "phase330_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase330_depth_beyond_l1_required", 0)),
            "l1_only_variant_rows_allowed": as_int(metric_value(path, "phase330_l1_only_variant_rows_allowed", 0)),
            "net_edge_live_mask_rows_allowed": as_int(metric_value(path, "phase330_net_edge_live_mask_rows_allowed", 0)),
            "strategy_search_allowed_now": as_int(metric_value(path, "phase330_strategy_search_allowed_now", 0)),
            "replay_allowed": as_int(metric_value(path, "phase330_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase330_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase330_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase330_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase330_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase330_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase330_next_best_action", ""),
        }
    if phase == 331:
        complete = as_int(metric_value(path, "phase331_expanded_strategy_search_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_training_strategy_search_open" if complete else "phase331_expanded_strategy_search_precommit_gated",
            "expanded_strategy_search_precommit_complete": complete,
            "strategy_family_rows": as_int(metric_value(path, "phase331_strategy_family_rows", 0)),
            "depth_beyond_l1_family_rows": as_int(metric_value(path, "phase331_depth_beyond_l1_family_rows", 0)),
            "search_grid_rows": as_int(metric_value(path, "phase331_search_grid_rows", 0)),
            "expanded_variant_upper_bound_rows": as_int(metric_value(path, "phase331_expanded_variant_upper_bound_rows", 0)),
            "cost200_grid_rows": as_int(metric_value(path, "phase331_cost200_grid_rows", 0)),
            "passive_aware_grid_rows": as_int(metric_value(path, "phase331_passive_aware_grid_rows", 0)),
            "event_bucket_policy_rows": as_int(metric_value(path, "phase331_event_bucket_policy_rows", 0)),
            "acceptance_contract_rows": as_int(metric_value(path, "phase331_acceptance_contract_rows", 0)),
            "work_order_rows": as_int(metric_value(path, "phase331_work_order_rows", 0)),
            "zerodha_cost_model_version": metric_value(path, "phase331_zerodha_cost_model_version", ""),
            "full_depth_required": as_int(metric_value(path, "phase331_full_depth_required", 0)),
            "depth_beyond_l1_required": as_int(metric_value(path, "phase331_depth_beyond_l1_required", 0)),
            "l1_only_candidate_allowed": as_int(metric_value(path, "phase331_l1_only_candidate_allowed", 1)),
            "net_edge_live_mask_rows_allowed": as_int(metric_value(path, "phase331_net_edge_live_mask_rows_allowed", 1)),
            "fixed_capital_required": as_int(metric_value(path, "phase331_fixed_capital_required", 0)),
            "cost200_required": as_int(metric_value(path, "phase331_cost200_required", 0)),
            "passive_realism_penalties_required": as_int(metric_value(path, "phase331_passive_realism_penalties_required", 0)),
            "strategy_search_execution_allowed_next": as_int(metric_value(path, "phase331_strategy_search_execution_allowed_next", 0)),
            "replay_allowed": as_int(metric_value(path, "phase331_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase331_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase331_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase331_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase331_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase331_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase331_next_best_action", ""),
        }
    if phase == 332:
        complete = as_int(metric_value(path, "phase332_expanded_strategy_search_training_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "event_catalyst_expanded_strategy_search_interpretation_open" if complete else "phase332_expanded_strategy_search_training_gated",
            "expanded_strategy_search_training_complete": complete,
            "scenario_rows": as_int(metric_value(path, "phase332_scenario_rows", 0)),
            "family_rows": as_int(metric_value(path, "phase332_family_rows", 0)),
            "cost200_scenario_rows": as_int(metric_value(path, "phase332_cost200_scenario_rows", 0)),
            "passive_aware_scenario_rows": as_int(metric_value(path, "phase332_passive_aware_scenario_rows", 0)),
            "event_bucket_policy_rows": as_int(metric_value(path, "phase332_event_bucket_policy_rows", 0)),
            "above12_annualized_scenario_rows": as_int(metric_value(path, "phase332_above12_annualized_scenario_rows", 0)),
            "cost200_above12_scenario_rows": as_int(metric_value(path, "phase332_cost200_above12_scenario_rows", 0)),
            "cost200_acceptance_grade_candidate_rows": as_int(metric_value(path, "phase332_cost200_acceptance_grade_candidate_rows", 0)),
            "best_scenario_id": metric_value(path, "phase332_best_scenario_id", ""),
            "best_family_id": metric_value(path, "phase332_best_family_id", ""),
            "best_execution_policy": metric_value(path, "phase332_best_execution_policy", ""),
            "best_cost_profile": metric_value(path, "phase332_best_cost_profile", ""),
            "best_event_bucket_policy": metric_value(path, "phase332_best_event_bucket_policy", ""),
            "best_annualized_return_pct": metric_value(path, "phase332_best_annualized_return_pct", ""),
            "best_scheduled_event_rows": as_int(metric_value(path, "phase332_best_scheduled_event_rows", 0)),
            "best_cost200_scenario_id": metric_value(path, "phase332_best_cost200_scenario_id", ""),
            "best_cost200_annualized_return_pct": metric_value(path, "phase332_best_cost200_annualized_return_pct", ""),
            "best_cost200_scheduled_event_rows": as_int(metric_value(path, "phase332_best_cost200_scheduled_event_rows", 0)),
            "scenario_parquet_written": as_int(metric_value(path, "phase332_scenario_parquet_written", 0)),
            "scenario_parquet_bytes": as_int(metric_value(path, "phase332_scenario_parquet_bytes", 0)),
            "annualized_denominator": metric_value(path, "phase332_annualized_denominator", ""),
            "replay_allowed": as_int(metric_value(path, "phase332_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase332_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase332_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase332_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase332_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase332_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase332_next_best_action", ""),
        }
    if phase == 333:
        complete = as_int(metric_value(path, "phase333_event_catalyst_expanded_strategy_search_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_stress_margin_redesign_precommit_open" if complete else "phase333_event_catalyst_expanded_strategy_search_interpretation_gated",
            "event_catalyst_expanded_strategy_search_interpretation_complete": complete,
            "base_or_slippage_profitable_research_pockets_exist": as_int(metric_value(path, "phase333_base_or_slippage_profitable_research_pockets_exist", 0)),
            "cost200_profitability_bar_passed": as_int(metric_value(path, "phase333_cost200_profitability_bar_passed", 0)),
            "cost200_acceptance_grade_candidates_exist": as_int(metric_value(path, "phase333_cost200_acceptance_grade_candidates_exist", 0)),
            "best_cost200_near_miss_preserved": as_int(metric_value(path, "phase333_best_cost200_near_miss_preserved", 0)),
            "preserved_family_for_redesign": metric_value(path, "phase333_preserved_family_for_redesign", ""),
            "passive_aware_rescue_status": metric_value(path, "phase333_passive_aware_rescue_status", ""),
            "next_design_focus": metric_value(path, "phase333_next_design_focus", ""),
            "replay_allowed": as_int(metric_value(path, "phase333_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase333_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase333_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase333_deployable_profitability_claim_allowed", 0)),
            "selected_next_route": metric_value(path, "phase333_selected_next_route", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase333_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase333_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase333_next_best_action", ""),
        }
    if phase == 334:
        complete = as_int(metric_value(path, "phase334_cost_stress_margin_redesign_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_stress_margin_redesign_training_search_open" if complete else "phase334_cost_stress_margin_redesign_precommit_gated",
            "cost_stress_margin_redesign_precommit_complete": complete,
            "preserved_family": metric_value(path, "phase334_preserved_family", ""),
            "design_lane_rows": as_int(metric_value(path, "phase334_design_lane_rows", 0)),
            "search_contract_rows": as_int(metric_value(path, "phase334_search_contract_rows", 0)),
            "phase335_work_order_rows": as_int(metric_value(path, "phase334_phase335_work_order_rows", 0)),
            "best_cost200_prior_annualized_return_pct": metric_value(path, "phase334_best_cost200_prior_annualized_return_pct", ""),
            "required_annualized_threshold_pct": metric_value(path, "phase334_required_annualized_threshold_pct", ""),
            "required_cost_profile": metric_value(path, "phase334_required_cost_profile", ""),
            "full_depth_required": as_int(metric_value(path, "phase334_full_depth_required", 0)),
            "levels_2_to_5_required": as_int(metric_value(path, "phase334_levels_2_to_5_required", 0)),
            "l1_only_allowed": as_int(metric_value(path, "phase334_l1_only_allowed", 1)),
            "net_edge_live_mask_allowed": as_int(metric_value(path, "phase334_net_edge_live_mask_allowed", 1)),
            "strategy_search_execution_allowed_next": as_int(metric_value(path, "phase334_strategy_search_execution_allowed_next", 0)),
            "replay_allowed": as_int(metric_value(path, "phase334_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase334_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase334_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase334_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase334_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase334_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase334_next_best_action", ""),
        }
    if phase == 335:
        complete = as_int(metric_value(path, "phase335_cost_stress_margin_redesign_training_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_stress_margin_redesign_interpretation_open" if complete else "phase335_cost_stress_margin_redesign_training_gated",
            "cost_stress_margin_redesign_training_complete": complete,
            "scenario_rows": as_int(metric_value(path, "phase335_scenario_rows", 0)),
            "design_lane_rows": as_int(metric_value(path, "phase335_design_lane_rows", 0)),
            "cost200_scenario_rows": as_int(metric_value(path, "phase335_cost200_scenario_rows", 0)),
            "passive_aware_scenario_rows": as_int(metric_value(path, "phase335_passive_aware_scenario_rows", 0)),
            "above12_annualized_scenario_rows": as_int(metric_value(path, "phase335_above12_annualized_scenario_rows", 0)),
            "cost200_above12_scenario_rows": as_int(metric_value(path, "phase335_cost200_above12_scenario_rows", 0)),
            "cost200_acceptance_grade_candidate_rows": as_int(metric_value(path, "phase335_cost200_acceptance_grade_candidate_rows", 0)),
            "best_scenario_id": metric_value(path, "phase335_best_scenario_id", ""),
            "best_lane_id": metric_value(path, "phase335_best_lane_id", ""),
            "best_annualized_return_pct": metric_value(path, "phase335_best_annualized_return_pct", ""),
            "best_cost_profile": metric_value(path, "phase335_best_cost_profile", ""),
            "best_cost200_scenario_id": metric_value(path, "phase335_best_cost200_scenario_id", ""),
            "best_cost200_lane_id": metric_value(path, "phase335_best_cost200_lane_id", ""),
            "best_cost200_annualized_return_pct": metric_value(path, "phase335_best_cost200_annualized_return_pct", ""),
            "best_cost200_scheduled_event_rows": as_int(metric_value(path, "phase335_best_cost200_scheduled_event_rows", 0)),
            "best_cost200_control_pass": as_int(metric_value(path, "phase335_best_cost200_control_pass", 0)),
            "best_acceptance_grade_cost200_scenario_id": metric_value(path, "phase335_best_acceptance_grade_cost200_scenario_id", ""),
            "best_acceptance_grade_cost200_lane_id": metric_value(path, "phase335_best_acceptance_grade_cost200_lane_id", ""),
            "best_acceptance_grade_cost200_annualized_return_pct": metric_value(path, "phase335_best_acceptance_grade_cost200_annualized_return_pct", ""),
            "best_acceptance_grade_cost200_scheduled_event_rows": as_int(metric_value(path, "phase335_best_acceptance_grade_cost200_scheduled_event_rows", 0)),
            "scenario_parquet_written": as_int(metric_value(path, "phase335_scenario_parquet_written", 0)),
            "scenario_parquet_bytes": as_int(metric_value(path, "phase335_scenario_parquet_bytes", 0)),
            "annualized_denominator": metric_value(path, "phase335_annualized_denominator", ""),
            "cost_model_version": metric_value(path, "phase335_cost_model_version", ""),
            "replay_allowed": as_int(metric_value(path, "phase335_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase335_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase335_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase335_deployable_profitability_claim_allowed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase335_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase335_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase335_next_best_action", ""),
        }
    if phase == 336:
        complete = as_int(metric_value(path, "phase336_cost_stress_margin_redesign_interpretation_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_stress_holdout_validation_precommit_open" if complete else "phase336_cost_stress_margin_redesign_interpretation_gated",
            "cost_stress_margin_redesign_interpretation_complete": complete,
            "cost200_profitable_training_pockets_exist": as_int(metric_value(path, "phase336_cost200_profitable_training_pockets_exist", 0)),
            "cost200_acceptance_grade_training_candidates_exist": as_int(metric_value(path, "phase336_cost200_acceptance_grade_training_candidates_exist", 0)),
            "candidate_rows_preserved": as_int(metric_value(path, "phase336_candidate_rows_preserved", 0)),
            "best_acceptance_grade_candidate": metric_value(path, "phase336_best_acceptance_grade_candidate", ""),
            "best_acceptance_grade_annualized_return_pct": metric_value(path, "phase336_best_acceptance_grade_annualized_return_pct", ""),
            "best_acceptance_grade_scheduled_events": as_int(metric_value(path, "phase336_best_acceptance_grade_scheduled_events", 0)),
            "candidate_lanes_preserved": metric_value(path, "phase336_candidate_lanes_preserved", ""),
            "passive_aware_status": metric_value(path, "phase336_passive_aware_status", ""),
            "replay_allowed": as_int(metric_value(path, "phase336_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase336_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase336_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase336_deployable_profitability_claim_allowed", 0)),
            "selected_next_route": metric_value(path, "phase336_selected_next_route", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase336_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase336_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase336_next_best_action", ""),
        }
    if phase == 337:
        complete = as_int(metric_value(path, "phase337_cost_stress_holdout_validation_precommit_complete", 0))
        return {
            "branch": "synthetic_strategy_discovery",
            "state": "cost_stress_holdout_validation_execution_open" if complete else "phase337_cost_stress_holdout_validation_precommit_gated",
            "cost_stress_holdout_validation_precommit_complete": complete,
            "candidate_rows_frozen": as_int(metric_value(path, "phase337_candidate_rows_frozen", 0)),
            "best_frozen_candidate": metric_value(path, "phase337_best_frozen_candidate", ""),
            "best_frozen_annualized_return_pct": metric_value(path, "phase337_best_frozen_annualized_return_pct", ""),
            "best_frozen_scheduled_events": as_int(metric_value(path, "phase337_best_frozen_scheduled_events", 0)),
            "candidate_lanes_frozen": metric_value(path, "phase337_candidate_lanes_frozen", ""),
            "attached_passive_aware_charter_reconciled": as_int(metric_value(path, "phase337_attached_passive_aware_charter_reconciled", 0)),
            "passive_fill_model_required": as_int(metric_value(path, "phase337_passive_fill_model_required", 0)),
            "adverse_selection_penalty_required": as_int(metric_value(path, "phase337_adverse_selection_penalty_required", 0)),
            "forced_flatten_cost_required": as_int(metric_value(path, "phase337_forced_flatten_cost_required", 0)),
            "maker_rebate_allowed": as_int(metric_value(path, "phase337_maker_rebate_allowed", 1)),
            "cost_profile_required": metric_value(path, "phase337_cost_profile_required", ""),
            "cost_model_version": metric_value(path, "phase337_cost_model_version", ""),
            "annualized_threshold_pct": metric_value(path, "phase337_annualized_threshold_pct", ""),
            "robust_event_floor": as_int(metric_value(path, "phase337_robust_event_floor", 0)),
            "full_depth_required": as_int(metric_value(path, "phase337_full_depth_required", 0)),
            "levels_2_to_5_required": as_int(metric_value(path, "phase337_levels_2_to_5_required", 0)),
            "l1_only_allowed": as_int(metric_value(path, "phase337_l1_only_allowed", 1)),
            "net_edge_live_mask_allowed": as_int(metric_value(path, "phase337_net_edge_live_mask_allowed", 1)),
            "replay_allowed": as_int(metric_value(path, "phase337_strategy_replay_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase337_strategy_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase337_paper_or_live_acceptance_allowed", 0)),
            "profitability_claim_allowed": as_int(metric_value(path, "phase337_deployable_profitability_claim_allowed", 0)),
            "phase338_execution_allowed_next": as_int(metric_value(path, "phase337_phase338_execution_allowed_next", 0)),
            "contract_rows": as_int(metric_value(path, "phase337_contract_rows", 0)),
            "phase338_work_order_rows": as_int(metric_value(path, "phase337_phase338_work_order_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase337_hard_gate_pass_rows", 0)),
            "hard_gate_rows": as_int(metric_value(path, "phase337_hard_gate_rows", 0)),
            "next_action": metric_value(path, "phase337_next_best_action", ""),
        }
    return {}


def build_phase_ledger(scripts: pd.DataFrame, outputs: pd.DataFrame) -> pd.DataFrame:
    phases = sorted(set(scripts["phase"].astype(int).tolist() if not scripts.empty else []).union(outputs["phase"].astype(int).tolist() if not outputs.empty else []))
    rows: list[dict[str, Any]] = []
    for phase in phases:
        script_rows = scripts[scripts["phase"].astype(int).eq(phase)] if not scripts.empty else pd.DataFrame()
        output_rows = outputs[outputs["phase"].astype(int).eq(phase)] if not outputs.empty else pd.DataFrame()
        metric_status = phase_status_from_metrics(phase)
        has_runner = not script_rows.empty
        has_outputs = not output_rows.empty
        has_acceptance = bool(not output_rows.empty and output_rows["acceptance_files"].astype(str).ne("").any())
        smoke_or_partial = bool(not output_rows.empty and output_rows["is_smoke_or_partial"].astype(bool).any())
        status = "script_only"
        if has_outputs and has_acceptance and not smoke_or_partial:
            status = "evidence_present"
        elif has_outputs and smoke_or_partial:
            status = "smoke_or_partial"
        if metric_status.get("state"):
            status = str(metric_status["state"])
        rows.append(
            {
                "phase": phase,
                "runner_count": int(len(script_rows)),
                "output_rows": int(len(output_rows)),
                "has_runner": has_runner,
                "has_outputs": has_outputs,
                "has_acceptance_summary": has_acceptance,
                "status": status,
                "branch": metric_status.get("branch", ""),
                "strategy_replay_allowed": metric_status.get("strategy_replay_allowed", ""),
                "pnl_allowed": metric_status.get("pnl_allowed", ""),
                "test_rows_used": metric_status.get("test_rows_used", ""),
                "test_replay_execution": metric_status.get("test_replay_execution", ""),
                "test_result_allowed": metric_status.get("test_result_allowed", ""),
                "test_replay_allowed_next": metric_status.get("test_replay_allowed_next", ""),
                "untouched_test_replay_precommit_allowed": metric_status.get("untouched_test_replay_precommit_allowed", ""),
                "reuse_without_redesign_allowed": metric_status.get("reuse_without_redesign_allowed", ""),
                "additional_validation_breadth_available_now": metric_status.get("additional_validation_breadth_available_now", ""),
                "may_relabel_test_as_validation": metric_status.get("may_relabel_test_as_validation", ""),
                "breadth_warning": metric_status.get("breadth_warning", ""),
                "date_count_warning": metric_status.get("date_count_warning", ""),
                "promotion_allowed": metric_status.get("promotion_allowed", ""),
                "paper_or_live_acceptance_allowed": metric_status.get("paper_or_live_acceptance_allowed", ""),
                "next_action": metric_status.get("next_action", ""),
                "runner": "|".join(script_rows["runner"].astype(str).tolist()) if has_runner else "",
                "output_dir": "|".join(output_rows["output_dir"].astype(str).tolist()) if has_outputs else "",
            }
        )
    return pd.DataFrame(rows)


def build_branch_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    phase174 = phase_status_from_metrics(174)
    phase175 = phase_status_from_metrics(175)
    phase176 = phase_status_from_metrics(176)
    phase177 = phase_status_from_metrics(177)
    phase178 = phase_status_from_metrics(178)
    phase179 = phase_status_from_metrics(179)
    phase180 = phase_status_from_metrics(180)
    phase181 = phase_status_from_metrics(181)
    phase182 = phase_status_from_metrics(182)
    phase183 = phase_status_from_metrics(183)
    phase184 = phase_status_from_metrics(184)
    phase185 = phase_status_from_metrics(185)
    phase186 = phase_status_from_metrics(186)
    phase187 = phase_status_from_metrics(187)
    phase188 = phase_status_from_metrics(188)
    phase189 = phase_status_from_metrics(189)
    phase190 = phase_status_from_metrics(190)
    phase191 = phase_status_from_metrics(191)
    phase192 = phase_status_from_metrics(192)
    phase193 = phase_status_from_metrics(193)
    phase194 = phase_status_from_metrics(194)
    phase195 = phase_status_from_metrics(195)
    phase196 = phase_status_from_metrics(196)
    phase197 = phase_status_from_metrics(197)
    phase198 = phase_status_from_metrics(198)
    phase199 = phase_status_from_metrics(199)
    phase200 = phase_status_from_metrics(200)
    phase201 = phase_status_from_metrics(201)
    phase202 = phase_status_from_metrics(202)
    phase203 = phase_status_from_metrics(203)
    phase204 = phase_status_from_metrics(204)
    phase205 = phase_status_from_metrics(205)
    phase206 = phase_status_from_metrics(206)
    phase207 = phase_status_from_metrics(207)
    phase208 = phase_status_from_metrics(208)
    phase209 = phase_status_from_metrics(209)
    phase210 = phase_status_from_metrics(210)
    phase211 = phase_status_from_metrics(211)
    phase212 = phase_status_from_metrics(212)
    phase213 = phase_status_from_metrics(213)
    phase214 = phase_status_from_metrics(214)
    phase215 = phase_status_from_metrics(215)
    phase216 = phase_status_from_metrics(216)
    phase217 = phase_status_from_metrics(217)
    phase218 = phase_status_from_metrics(218)
    phase219 = phase_status_from_metrics(219)
    phase220 = phase_status_from_metrics(220)
    phase221 = phase_status_from_metrics(221)
    phase222 = phase_status_from_metrics(222)
    phase223 = phase_status_from_metrics(223)
    phase224 = phase_status_from_metrics(224)
    phase225 = phase_status_from_metrics(225)
    phase226 = phase_status_from_metrics(226)
    phase227 = phase_status_from_metrics(227)
    phase228 = phase_status_from_metrics(228)
    phase229 = phase_status_from_metrics(229)
    phase230 = phase_status_from_metrics(230)
    phase231 = phase_status_from_metrics(231)
    phase232 = phase_status_from_metrics(232)
    phase233 = phase_status_from_metrics(233)
    phase234 = phase_status_from_metrics(234)
    phase235 = phase_status_from_metrics(235)
    phase236 = phase_status_from_metrics(236)
    phase237 = phase_status_from_metrics(237)
    phase238 = phase_status_from_metrics(238)
    phase239 = phase_status_from_metrics(239)
    phase240 = phase_status_from_metrics(240)
    phase241 = phase_status_from_metrics(241)
    phase242 = phase_status_from_metrics(242)
    phase243 = phase_status_from_metrics(243)
    phase244 = phase_status_from_metrics(244)
    phase245 = phase_status_from_metrics(245)
    phase246 = phase_status_from_metrics(246)
    phase247 = phase_status_from_metrics(247)
    phase248 = phase_status_from_metrics(248)
    phase249 = phase_status_from_metrics(249)
    phase250 = phase_status_from_metrics(250)
    phase251 = phase_status_from_metrics(251)
    phase252 = phase_status_from_metrics(252)
    phase253 = phase_status_from_metrics(253)
    phase254 = phase_status_from_metrics(254)
    phase255 = phase_status_from_metrics(255)
    phase256 = phase_status_from_metrics(256)
    phase257 = phase_status_from_metrics(257)
    phase258 = phase_status_from_metrics(258)
    phase259 = phase_status_from_metrics(259)
    phase260 = phase_status_from_metrics(260)
    phase261 = phase_status_from_metrics(261)
    phase262 = phase_status_from_metrics(262)
    phase263 = phase_status_from_metrics(263)
    phase264 = phase_status_from_metrics(264)
    phase265 = phase_status_from_metrics(265)
    phase266 = phase_status_from_metrics(266)
    phase267 = phase_status_from_metrics(267)
    phase268 = phase_status_from_metrics(268)
    phase269 = phase_status_from_metrics(269)
    phase270 = phase_status_from_metrics(270)
    phase271 = phase_status_from_metrics(271)
    phase272 = phase_status_from_metrics(272)
    phase273 = phase_status_from_metrics(273)
    phase274 = phase_status_from_metrics(274)
    phase275 = phase_status_from_metrics(275)
    phase276 = phase_status_from_metrics(276)
    phase277 = phase_status_from_metrics(277)
    phase278 = phase_status_from_metrics(278)
    phase279 = phase_status_from_metrics(279)
    phase280 = phase_status_from_metrics(280)
    phase281 = phase_status_from_metrics(281)
    phase282 = phase_status_from_metrics(282)
    phase283 = phase_status_from_metrics(283)
    phase284 = phase_status_from_metrics(284)
    phase285 = phase_status_from_metrics(285)
    phase286 = phase_status_from_metrics(286)
    phase287 = phase_status_from_metrics(287)
    phase288 = phase_status_from_metrics(288)
    phase289 = phase_status_from_metrics(289)
    phase290 = phase_status_from_metrics(290)
    phase291 = phase_status_from_metrics(291)
    phase292 = phase_status_from_metrics(292)
    phase293 = phase_status_from_metrics(293)
    phase294 = phase_status_from_metrics(294)
    phase295 = phase_status_from_metrics(295)
    phase296 = phase_status_from_metrics(296)
    phase297 = phase_status_from_metrics(297)
    phase298 = phase_status_from_metrics(298)
    phase299 = phase_status_from_metrics(299)
    phase300 = phase_status_from_metrics(300)
    phase301 = phase_status_from_metrics(301)
    phase302 = phase_status_from_metrics(302)
    phase303 = phase_status_from_metrics(303)
    phase304 = phase_status_from_metrics(304)
    phase305 = phase_status_from_metrics(305)
    phase306 = phase_status_from_metrics(306)
    phase307 = phase_status_from_metrics(307)
    phase308 = phase_status_from_metrics(308)
    phase309 = phase_status_from_metrics(309)
    phase310 = phase_status_from_metrics(310)
    phase311 = phase_status_from_metrics(311)
    phase312 = phase_status_from_metrics(312)
    phase313 = phase_status_from_metrics(313)
    phase314 = phase_status_from_metrics(314)
    phase315 = phase_status_from_metrics(315)
    phase316 = phase_status_from_metrics(316)
    phase317 = phase_status_from_metrics(317)
    phase318 = phase_status_from_metrics(318)
    phase319 = phase_status_from_metrics(319)
    phase320 = phase_status_from_metrics(320)
    phase321 = phase_status_from_metrics(321)
    phase322 = phase_status_from_metrics(322)
    phase323 = phase_status_from_metrics(323)
    phase324 = phase_status_from_metrics(324)
    phase325 = phase_status_from_metrics(325)
    phase326 = phase_status_from_metrics(326)
    phase327 = phase_status_from_metrics(327)
    phase328 = phase_status_from_metrics(328)
    phase329 = phase_status_from_metrics(329)
    phase330 = phase_status_from_metrics(330)
    phase331 = phase_status_from_metrics(331)
    phase332 = phase_status_from_metrics(332)
    phase333 = phase_status_from_metrics(333)
    phase334 = phase_status_from_metrics(334)
    phase335 = phase_status_from_metrics(335)
    phase336 = phase_status_from_metrics(336)
    phase337 = phase_status_from_metrics(337)
    phase172 = phase_status_from_metrics(172)
    real_receive_next = phase337.get("next_action") or phase336.get("next_action") or phase335.get("next_action") or phase334.get("next_action") or phase333.get("next_action") or phase332.get("next_action") or phase331.get("next_action") or phase330.get("next_action") or phase329.get("next_action") or phase328.get("next_action") or phase327.get("next_action") or phase326.get("next_action") or phase325.get("next_action") or phase324.get("next_action") or phase323.get("next_action") or phase322.get("next_action") or phase321.get("next_action") or phase320.get("next_action") or phase319.get("next_action") or phase318.get("next_action") or phase317.get("next_action") or phase316.get("next_action") or phase315.get("next_action") or phase314.get("next_action") or phase313.get("next_action") or phase312.get("next_action") or phase311.get("next_action") or phase310.get("next_action") or phase309.get("next_action") or phase308.get("next_action") or phase307.get("next_action") or phase306.get("next_action") or phase305.get("next_action") or phase304.get("next_action") or phase303.get("next_action") or phase302.get("next_action") or phase301.get("next_action") or phase300.get("next_action") or phase299.get("next_action") or phase298.get("next_action") or phase297.get("next_action") or phase296.get("next_action") or phase295.get("next_action") or phase294.get("next_action") or phase293.get("next_action") or phase292.get("next_action") or phase291.get("next_action") or phase290.get("next_action") or phase289.get("next_action") or phase288.get("next_action") or phase287.get("next_action") or phase286.get("next_action") or phase285.get("next_action") or phase284.get("next_action") or phase283.get("next_action") or phase282.get("next_action") or phase281.get("next_action") or phase280.get("next_action") or phase279.get("next_action") or phase278.get("next_action") or phase277.get("next_action") or phase276.get("next_action") or phase275.get("next_action") or phase274.get("next_action") or phase273.get("next_action") or phase272.get("next_action") or phase271.get("next_action") or phase270.get("next_action") or phase269.get("next_action") or phase268.get("next_action") or phase267.get("next_action") or phase266.get("next_action") or phase265.get("next_action") or phase264.get("next_action") or phase263.get("next_action") or phase262.get("next_action") or phase261.get("next_action") or phase260.get("next_action") or phase259.get("next_action") or phase258.get("next_action") or phase257.get("next_action") or phase256.get("next_action") or phase255.get("next_action") or phase254.get("next_action") or phase253.get("next_action") or phase252.get("next_action") or phase251.get("next_action") or phase250.get("next_action") or phase249.get("next_action") or phase248.get("next_action") or phase247.get("next_action") or phase246.get("next_action") or phase245.get("next_action") or phase244.get("next_action") or phase243.get("next_action") or phase242.get("next_action") or phase241.get("next_action") or phase240.get("next_action") or phase239.get("next_action") or phase238.get("next_action") or phase237.get("next_action") or phase236.get("next_action") or phase235.get("next_action") or phase234.get("next_action") or phase233.get("next_action") or phase232.get("next_action") or phase231.get("next_action") or phase230.get("next_action") or phase229.get("next_action") or phase228.get("next_action") or phase227.get("next_action") or phase226.get("next_action") or phase225.get("next_action") or phase224.get("next_action") or phase223.get("next_action") or phase222.get("next_action") or phase221.get("next_action") or phase220.get("next_action") or phase219.get("next_action") or phase218.get("next_action") or phase217.get("next_action") or phase216.get("next_action") or phase215.get("next_action") or phase214.get("next_action") or phase213.get("next_action") or phase212.get("next_action") or phase211.get("next_action") or phase210.get("next_action") or phase209.get("next_action") or phase208.get("next_action") or phase207.get("next_action") or phase206.get("next_action") or phase205.get("next_action") or phase204.get("next_action") or phase203.get("next_action") or phase202.get("next_action") or phase201.get("next_action") or phase200.get("next_action") or phase199.get("next_action") or phase198.get("next_action") or phase197.get("next_action") or phase196.get("next_action") or phase195.get("next_action") or phase194.get("next_action") or phase193.get("next_action") or phase192.get("next_action") or phase191.get("next_action") or phase190.get("next_action") or phase189.get("next_action") or phase188.get("next_action") or phase187.get("next_action") or phase186.get("next_action") or phase185.get("next_action") or phase184.get("next_action") or phase183.get("next_action") or phase182.get("next_action") or phase181.get("next_action") or phase180.get("next_action") or phase179.get("next_action") or phase178.get("next_action") or phase177.get("next_action") or phase176.get("next_action") or phase175.get("next_action") or phase174.get("next_action") or phase172.get("next_action") or "run_phase174_or_phase172_according_to_latest_gate"
    ready_dates = as_int(phase172.get("ready_receive_flow_dates", 0))
    additional_dates_needed = as_int(phase172.get("additional_dates_needed", 0))
    features_materialized = as_int(phase176.get("features_materialized", 0))
    quality_audit_ran = as_int(phase177.get("feature_quality_audit_ran", 0))
    handoff_ready = as_int(phase178.get("handoff_ready", 0))
    precommit_ready = as_int(phase179.get("precommit_ready", 0))
    cost_label_ready = as_int(phase180.get("precommit_ready", 0))
    labels_materialized = as_int(phase181.get("labels_materialized", 0))
    label_audit_pass = as_int(phase182.get("label_quality_leakage_audit_pass", 0))
    replay_readiness = as_int(phase183.get("replay_readiness_precommitted", 0))
    dry_run_complete = as_int(phase184.get("train_validation_dry_run_complete", 0))
    interpretation_complete = as_int(phase185.get("validation_interpretation_complete", 0))
    family_set_closed = as_int(phase186.get("current_family_set_closed", 0))
    sparse_candidate_complete = as_int(phase187.get("cost_aware_sparse_candidate_complete", 0))
    sparse_interpretation_complete = as_int(phase188.get("sparse_candidate_interpretation_complete", 0))
    test_precommit_decision_complete = as_int(phase189.get("test_precommit_decision_complete", 0))
    phase190_complete = as_int(phase190.get("phase190_decision_complete", 0))
    phase191_complete = as_int(phase191.get("diagnostic_test_precommit_complete", 0))
    phase192_complete = as_int(phase192.get("real_validation_download_complete", 0))
    phase193_complete = as_int(phase193.get("validation_breadth_extension_complete", 0))
    phase194_complete = as_int(phase194.get("fragility_decision_complete", 0))
    phase195_complete = as_int(phase195.get("redesign_search_complete", 0))
    phase196_complete = as_int(phase196.get("expanded_model_search_complete", 0))
    phase197_complete = as_int(phase197.get("non_receive_flow_feature_precommit_complete", 0))
    phase198_complete = as_int(phase198.get("context_model_search_complete", 0))
    phase199_complete = as_int(phase199.get("branch_decision_complete", 0))
    phase200_complete = as_int(phase200.get("material_new_hypothesis_precommit_complete", 0))
    phase201_complete = as_int(phase201.get("label_only_stage01_complete", 0))
    phase202_complete = as_int(phase202.get("passive_feature_redesign_precommit_complete", 0))
    phase203_complete = as_int(phase203.get("label_materialization_complete", 0))
    phase204_complete = as_int(phase204.get("closure_decision_complete", 0))
    phase205_complete = as_int(phase205.get("material_new_source_precommit_complete", 0))
    phase206_complete = as_int(phase206.get("nonoverlap_feature_contract_complete", 0))
    phase207_complete = as_int(phase207.get("feature_matrix_precommit_complete", 0))
    phase208_complete = as_int(phase208.get("feature_matrix_quality_gate_complete", 0))
    phase209_complete = as_int(phase209.get("model_fit_precommit_spec_complete", 0))
    phase210_complete = as_int(phase210.get("train_validation_model_fit_dry_run_complete", 0))
    phase211_complete = as_int(phase211.get("model_fit_validation_interpretation_complete", 0))
    phase212_complete = as_int(phase212.get("model_family_closure_or_redesign_precommit_complete", 0))
    phase213_complete = as_int(phase213.get("material_new_model_source_precommit_complete", 0))
    phase214_complete = as_int(phase214.get("event_surprise_label_materialization_complete", 0))
    phase215_complete = as_int(phase215.get("event_surprise_label_quality_interpretation_complete", 0))
    phase216_complete = as_int(phase216.get("event_surprise_event_only_target_precommit_complete", 0))
    phase217_complete = as_int(phase217.get("event_only_design_matrix_precommit_complete", 0))
    phase218_complete = as_int(phase218.get("event_only_model_fit_precommit_or_stop_complete", 0))
    phase219_complete = as_int(phase219.get("event_only_train_validation_model_fit_dry_run_complete", 0))
    phase220_complete = as_int(phase220.get("event_only_model_fit_validation_interpretation_complete", 0))
    phase221_complete = as_int(phase221.get("event_only_signal_replay_precommit_or_stop_complete", 0))
    phase222_complete = as_int(phase222.get("event_only_train_validation_signal_replay_dry_run_complete", 0))
    phase223_complete = as_int(phase223.get("event_only_signal_replay_validation_interpretation_complete", 0))
    phase224_complete = as_int(phase224.get("event_only_signal_replay_closure_or_redesign_precommit_complete", 0))
    phase225_complete = as_int(phase225.get("cost_aware_event_source_redesign_precommit_complete", 0))
    phase226_complete = as_int(phase226.get("cost_aware_event_label_materialization_dry_run_complete", 0))
    phase227_complete = as_int(phase227.get("cost_aware_event_label_quality_interpretation_complete", 0))
    phase228_complete = as_int(phase228.get("cost_aware_label_redesign_closure_or_relaxation_precommit_complete", 0))
    phase250_complete = as_int(phase250.get("pair_basket_precommit_complete", 0))
    phase251_complete = as_int(phase251.get("pair_basket_search_complete", 0))
    phase252_complete = as_int(phase252.get("close_or_broaden_complete", 0))
    phase253_complete = as_int(phase253.get("richer_raw_depth_precommit_complete", 0))
    phase254_complete = as_int(phase254.get("richer_raw_depth_materialization_complete", 0))
    phase255_complete = as_int(phase255.get("feature_quality_interpretation_complete", 0))
    phase256_complete = as_int(phase256.get("strategy_search_complete", 0))
    phase257_complete = as_int(phase257.get("interpretation_complete", 0))
    phase258_complete = as_int(phase258.get("passive_queue_precommit_complete", 0))
    phase259_complete = as_int(phase259.get("passive_training_search_complete", 0))
    phase260_complete = as_int(phase260.get("interpretation_complete", 0))
    phase261_complete = as_int(phase261.get("passive_repair_precommit_complete", 0))
    phase262_complete = as_int(phase262.get("passive_training_search_complete", 0))
    phase263_complete = as_int(phase263.get("interpretation_complete", 0))
    phase264_complete = as_int(phase264.get("liquidity_shock_precommit_complete", 0))
    phase265_complete = as_int(phase265.get("liquidity_shock_training_search_complete", 0))
    phase266_complete = as_int(phase266.get("interpretation_complete", 0))
    phase267_complete = as_int(phase267.get("breadth_shuffle_repair_precommit_complete", 0))
    phase268_complete = as_int(phase268.get("two_lane_training_search_complete", 0))
    phase269_complete = as_int(phase269.get("interpretation_complete", 0))
    phase270_complete = as_int(phase270.get("fixed_capital_precommit_complete", 0))
    phase271_complete = as_int(phase271.get("fixed_capital_analysis_complete", 0))
    phase272_complete = as_int(phase272.get("interpretation_complete", 0))
    phase273_complete = as_int(phase273.get("followthrough_search_complete", 0))
    phase274_complete = as_int(phase274.get("interpretation_complete", 0))
    phase275_complete = as_int(phase275.get("multiday_synthetic_followthrough_search_complete", 0))
    phase276_complete = as_int(phase276.get("interpretation_complete", 0))
    phase277_complete = as_int(phase277.get("cost_robust_redesign_search_complete", 0))
    phase278_complete = as_int(phase278.get("interpretation_complete", 0))
    phase279_complete = as_int(phase279.get("target_construction_precommit_complete", 0))
    phase280_complete = as_int(phase280.get("material_new_target_construction_search_complete", 0))
    phase281_complete = as_int(phase281.get("interpretation_complete", 0))
    phase282_complete = as_int(phase282.get("regime_conditioned_ensemble_precommit_complete", 0))
    phase283_complete = as_int(phase283.get("regime_conditioned_ensemble_search_complete", 0))
    phase284_complete = as_int(phase284.get("interpretation_complete", 0))
    phase285_complete = as_int(phase285.get("lifecycle_redesign_precommit_complete", 0))
    phase286_complete = as_int(phase286.get("lifecycle_redesign_search_complete", 0))
    phase287_complete = as_int(phase287.get("interpretation_complete", 0))
    phase288_complete = as_int(phase288.get("liquidity_pressure_search_complete", 0))
    phase289_complete = as_int(phase289.get("interpretation_complete", 0))
    phase290_complete = as_int(phase290.get("adaptive_liquidity_pressure_search_complete", 0))
    phase291_complete = as_int(phase291.get("interpretation_complete", 0))
    phase292_complete = as_int(phase292.get("breadth_repair_search_complete", 0))
    phase293_complete = as_int(phase293.get("interpretation_complete", 0))
    phase294_complete = as_int(phase294.get("continuation_search_complete", 0))
    phase295_complete = as_int(phase295.get("interpretation_complete", 0))
    phase296_complete = as_int(phase296.get("full_year_sweep_complete", 0))
    phase297_complete = as_int(phase297.get("interpretation_complete", 0))
    phase298_complete = as_int(phase298.get("raw_dense_sweep_complete", 0))
    phase299_complete = as_int(phase299.get("interpretation_complete", 0))
    phase300_complete = as_int(phase300.get("precommit_complete", 0))
    phase300_execution_complete = as_int(phase300.get("execution_complete", 0))
    phase301_complete = as_int(phase301.get("interpretation_complete", 0))
    phase302_complete = as_int(phase302.get("terminal_report_complete", 0))
    phase303_complete = as_int(phase303.get("material_new_selector_complete", 0))
    phase304_complete = as_int(phase304.get("source_acquisition_package_complete", 0))
    phase305_complete = as_int(phase305.get("event_catalyst_import_audit_complete", 0))
    phase306_complete = as_int(phase306.get("join_precommit_complete", 0))
    phase307_complete = as_int(phase307.get("join_materialization_complete", 0))
    phase308_complete = as_int(phase308.get("join_quality_audit_complete", 0))
    phase309_complete = as_int(phase309.get("event_feature_precommit_complete", 0))
    phase310_complete = as_int(phase310.get("event_feature_materialization_complete", 0))
    phase311_complete = as_int(phase311.get("strategy_search_precommit_complete", 0))
    phase312_complete = as_int(phase312.get("strategy_search_training_complete", 0))
    phase313_complete = as_int(phase313.get("interpretation_complete", 0))
    phase314_complete = as_int(phase314.get("multievent_breadth_precommit_complete", 0))
    phase315_complete = as_int(phase315.get("multievent_breadth_materialization_complete", 0))
    phase316_complete = as_int(phase316.get("multievent_top5_depth_join_precommit_complete", 0))
    phase317_complete = as_int(phase317.get("multievent_top5_depth_join_materialization_complete", 0))
    phase318_complete = as_int(phase318.get("multievent_join_quality_audit_complete", 0))
    phase319_complete = as_int(phase319.get("multievent_feature_materialization_precommit_complete", 0))
    phase320_complete = as_int(phase320.get("multievent_feature_materialization_complete", 0))
    phase321_complete = as_int(phase321.get("multievent_strategy_search_precommit_complete", 0))
    phase322_complete = as_int(phase322.get("multievent_strategy_search_training_complete", 0))
    phase323_complete = as_int(phase323.get("multievent_strategy_search_interpretation_complete", 0))
    phase324_complete = as_int(phase324.get("breadth_expansion_precommit_complete", 0))
    phase325_complete = as_int(phase325.get("breadth_expansion_materialization_complete", 0))
    phase326_complete = as_int(phase326.get("expanded_top5_depth_join_precommit_complete", 0))
    phase327_complete = as_int(phase327.get("expanded_top5_depth_join_materialization_complete", 0))
    phase328_complete = as_int(phase328.get("expanded_join_quality_audit_complete", 0))
    phase329_complete = as_int(phase329.get("expanded_feature_materialization_precommit_complete", 0))
    phase330_complete = as_int(phase330.get("expanded_feature_materialization_complete", 0))
    phase331_complete = as_int(phase331.get("expanded_strategy_search_precommit_complete", 0))
    phase332_complete = as_int(phase332.get("expanded_strategy_search_training_complete", 0))
    phase333_complete = as_int(phase333.get("event_catalyst_expanded_strategy_search_interpretation_complete", 0))
    phase334_complete = as_int(phase334.get("cost_stress_margin_redesign_precommit_complete", 0))
    phase335_complete = as_int(phase335.get("cost_stress_margin_redesign_training_complete", 0))
    phase336_complete = as_int(phase336.get("cost_stress_margin_redesign_interpretation_complete", 0))
    phase337_complete = as_int(phase337.get("cost_stress_holdout_validation_precommit_complete", 0))
    if ready_dates >= 5 and additional_dates_needed == 0:
        real_receive_status = "source_gate_open_feature_materialization_pending" if features_materialized == 0 else "feature_quality_pending"
        if quality_audit_ran == 1:
            real_receive_status = "quality_audited_handoff_pending"
        if handoff_ready == 1:
            real_receive_status = "handoff_precommitted_strategy_family_pending"
        if precommit_ready == 1:
            real_receive_status = "strategy_family_precommitted_cost_latency_label_pending"
        if cost_label_ready == 1:
            real_receive_status = "cost_latency_label_precommitted_label_materialization_pending"
        if labels_materialized == 1:
            real_receive_status = "labels_materialized_quality_leakage_pending"
        if label_audit_pass == 1:
            real_receive_status = "label_quality_leakage_audited_replay_readiness_pending"
        if replay_readiness == 1:
            real_receive_status = "replay_readiness_precommitted_train_validation_dry_run_pending"
        if dry_run_complete == 1:
            real_receive_status = "train_validation_replay_dry_run_complete_interpretation_pending"
        if interpretation_complete == 1:
            real_receive_status = "validation_interpretation_cost_dominated_redesign_or_close_pending"
        if family_set_closed == 1:
            real_receive_status = "current_family_set_closed_cost_aware_redesign_pending"
        if sparse_candidate_complete == 1:
            real_receive_status = "cost_aware_sparse_candidate_validation_interpretation_pending"
        if sparse_interpretation_complete == 1:
            real_receive_status = "sparse_candidate_interpreted_phase189_decision_pending"
        if test_precommit_decision_complete == 1:
            real_receive_status = "test_replay_deferred_validation_breadth_pending"
        if phase190_complete == 1:
            real_receive_status = "diagnostic_test_spec_written_validation_breadth_pending"
        if phase191_complete == 1:
            real_receive_status = "diagnostic_test_replay_precommitted_no_execution"
        if phase192_complete == 1:
            real_receive_status = "real_validation_date_downloaded_feature_label_refresh_pending"
        if phase193_complete == 1:
            real_receive_status = "validation_breadth_extended_mixed_negative_by_date_no_test"
        if phase194_complete == 1:
            real_receive_status = "frozen_sparse_candidate_closed_for_test_replay_redesign_required"
        if phase195_complete == 1:
            real_receive_status = str(phase195.get("state", "redesign_search_complete_no_test"))
        if phase196_complete == 1:
            real_receive_status = str(phase196.get("state", "expanded_feature_model_search_complete_no_test"))
        if phase197_complete == 1:
            real_receive_status = str(phase197.get("state", "non_receive_flow_feature_expansion_precommitted_no_test"))
        if phase198_complete == 1:
            real_receive_status = str(phase198.get("state", "non_receive_flow_context_model_search_complete_no_test"))
        if phase199_complete == 1:
            real_receive_status = str(phase199.get("state", "branch_decision_complete_no_test"))
        if phase200_complete == 1:
            real_receive_status = str(phase200.get("state", "material_new_hypothesis_precommit_complete_no_test"))
        if phase201_complete == 1:
            real_receive_status = str(phase201.get("state", "passive_queue_stage01_complete_no_test"))
        if phase202_complete == 1:
            real_receive_status = str(phase202.get("state", "passive_feature_redesign_precommitted_no_test"))
        if phase203_complete == 1:
            real_receive_status = str(phase203.get("state", "redesigned_passive_labels_materialized_no_test"))
        if phase204_complete == 1:
            real_receive_status = str(phase204.get("state", "passive_redesign_closure_decision_complete_no_test"))
        if phase205_complete == 1:
            real_receive_status = str(phase205.get("state", "material_new_source_precommit_complete_no_test"))
        if phase206_complete == 1:
            real_receive_status = str(phase206.get("state", "selected_source_nonoverlap_feature_contract_complete_no_test"))
        if phase207_complete == 1:
            real_receive_status = str(phase207.get("state", "allowed_feature_matrix_precommit_complete_no_test"))
        if phase208_complete == 1:
            real_receive_status = str(phase208.get("state", "feature_matrix_quality_gate_complete_no_test"))
        if phase209_complete == 1:
            real_receive_status = str(phase209.get("state", "model_fit_precommit_spec_complete_no_test"))
        if phase210_complete == 1:
            real_receive_status = str(phase210.get("state", "train_validation_model_fit_dry_run_complete_no_test"))
        if phase211_complete == 1:
            real_receive_status = str(phase211.get("state", "model_fit_validation_interpretation_complete_no_test"))
        if phase212_complete == 1:
            real_receive_status = str(phase212.get("state", "model_family_closure_or_redesign_precommit_complete_no_test"))
        if phase213_complete == 1:
            real_receive_status = str(phase213.get("state", "material_new_model_source_precommit_complete_no_test"))
        if phase214_complete == 1:
            real_receive_status = str(phase214.get("state", "event_surprise_label_materialization_complete_no_test"))
        if phase215_complete == 1:
            real_receive_status = str(phase215.get("state", "event_surprise_label_quality_interpretation_complete_no_test"))
        if phase216_complete == 1:
            real_receive_status = str(phase216.get("state", "event_surprise_event_only_target_precommit_complete_no_test"))
        if phase217_complete == 1:
            real_receive_status = str(phase217.get("state", "event_only_design_matrix_precommit_complete_no_test"))
        if phase218_complete == 1:
            real_receive_status = str(phase218.get("state", "event_only_model_fit_precommit_complete_no_test"))
        if phase219_complete == 1:
            real_receive_status = str(phase219.get("state", "event_only_train_validation_model_fit_dry_run_complete_no_test"))
        if phase220_complete == 1:
            real_receive_status = str(phase220.get("state", "event_only_model_fit_validation_interpretation_complete_no_test"))
        if phase221_complete == 1:
            real_receive_status = str(phase221.get("state", "event_only_signal_replay_precommit_complete_no_test"))
        if phase222_complete == 1:
            real_receive_status = str(phase222.get("state", "event_only_train_validation_signal_replay_dry_run_complete_no_test"))
        if phase223_complete == 1:
            real_receive_status = str(phase223.get("state", "event_only_signal_replay_validation_interpretation_complete_no_test"))
        if phase224_complete == 1:
            real_receive_status = str(phase224.get("state", "event_only_signal_replay_candidate_set_closed_no_test"))
        if phase225_complete == 1:
            real_receive_status = str(phase225.get("state", "cost_aware_event_source_redesign_precommit_complete_no_test"))
        if phase226_complete == 1:
            real_receive_status = str(phase226.get("state", "cost_aware_event_label_materialization_complete_no_test"))
        if phase227_complete == 1:
            real_receive_status = str(phase227.get("state", "cost_aware_event_label_quality_interpretation_complete_no_test"))
        if phase228_complete == 1:
            real_receive_status = str(phase228.get("state", "cost_aware_label_set_closed_no_test"))
        if phase250_complete == 1:
            real_receive_status = str(phase250.get("state", "pair_basket_relative_value_training_search_precommitted"))
        if phase251_complete == 1:
            real_receive_status = str(phase251.get("state", "pair_basket_relative_value_no_survivor_broaden_or_close"))
        if phase252_complete == 1:
            real_receive_status = str(phase252.get("state", "aggregate_pair_basket_closed_richer_raw_depth_precommit_open"))
        if phase253_complete == 1:
            real_receive_status = str(phase253.get("state", "richer_raw_top5_depth_materialization_precommitted"))
        if phase254_complete == 1:
            real_receive_status = str(phase254.get("state", "richer_raw_top5_depth_materialized_quality_interpretation_open"))
        if phase255_complete == 1:
            real_receive_status = str(phase255.get("state", "richer_raw_top5_depth_quality_passed_strategy_search_open"))
        if phase256_complete == 1:
            real_receive_status = str(phase256.get("state", "richer_raw_top5_depth_taker_search_no_survivor_interpretation_open"))
        if phase257_complete == 1:
            real_receive_status = str(phase257.get("state", "passive_queue_aware_spread_capture_precommit_open"))
        if phase258_complete == 1:
            real_receive_status = str(phase258.get("state", "passive_queue_aware_spread_capture_training_search_open"))
        if phase259_complete == 1:
            real_receive_status = str(phase259.get("state", "passive_queue_aware_training_search_no_survivor_interpretation_open"))
        if phase260_complete == 1:
            real_receive_status = str(phase260.get("state", "passive_opportunity_breadth_fill_model_repair_precommit_open"))
        if phase261_complete == 1:
            real_receive_status = str(phase261.get("state", "passive_opportunity_breadth_fill_model_training_search_open"))
        if phase262_complete == 1:
            real_receive_status = str(phase262.get("state", "passive_opportunity_breadth_fill_model_training_no_survivor_interpretation_open"))
        if phase263_complete == 1:
            real_receive_status = str(phase263.get("state", "full_depth_liquidity_shock_absorption_event_precommit_open"))
        if phase264_complete == 1:
            real_receive_status = str(phase264.get("state", "full_depth_liquidity_shock_absorption_event_training_search_open"))
        if phase265_complete == 1:
            real_receive_status = str(phase265.get("state", "full_depth_liquidity_shock_training_no_survivor_interpretation_open"))
        if phase266_complete == 1:
            real_receive_status = str(phase266.get("state", "full_depth_liquidity_shock_breadth_shuffle_repair_precommit_open"))
        if phase267_complete == 1:
            real_receive_status = str(phase267.get("state", "full_depth_liquidity_shock_two_lane_training_search_open"))
        if phase268_complete == 1:
            real_receive_status = str(phase268.get("state", "full_depth_liquidity_shock_two_lane_training_no_acceptance_interpretation_open"))
        if phase269_complete == 1:
            real_receive_status = str(phase269.get("state", "fixed_capital_concurrency_capacity_return_precommit_open"))
        if phase270_complete == 1:
            real_receive_status = str(phase270.get("state", "fixed_capital_concurrency_capacity_return_analysis_open"))
        if phase271_complete == 1:
            real_receive_status = str(phase271.get("state", "fixed_capital_capacity_return_interpretation_open"))
        if phase272_complete == 1:
            real_receive_status = str(phase272.get("state", "focused_capital_aware_candidate_followthrough_search_open"))
        if phase273_complete == 1:
            real_receive_status = str(phase273.get("state", "focused_capital_followthrough_interpretation_open"))
        if phase274_complete == 1:
            real_receive_status = str(phase274.get("state", "focused_capital_multiday_synthetic_followthrough_search_open"))
        if phase275_complete == 1:
            real_receive_status = str(phase275.get("state", "multiday_synthetic_followthrough_interpretation_open"))
        if phase276_complete == 1:
            real_receive_status = str(phase276.get("state", "cost_robust_full_depth_redesign_search_open"))
        if phase277_complete == 1:
            real_receive_status = str(phase277.get("state", "cost_robust_redesign_interpretation_open"))
        if phase278_complete == 1:
            real_receive_status = str(phase278.get("state", "material_new_target_construction_precommit_open"))
        if phase279_complete == 1:
            real_receive_status = str(phase279.get("state", "material_new_target_construction_search_open"))
        if phase280_complete == 1:
            real_receive_status = str(phase280.get("state", "material_new_target_construction_interpretation_open"))
        if phase281_complete == 1:
            real_receive_status = str(phase281.get("state", "regime_conditioned_full_depth_ensemble_precommit_open"))
        if phase282_complete == 1:
            real_receive_status = str(phase282.get("state", "regime_conditioned_full_depth_ensemble_search_open"))
        if phase283_complete == 1:
            real_receive_status = str(phase283.get("state", "regime_conditioned_full_depth_ensemble_interpretation_open"))
        if phase284_complete == 1:
            real_receive_status = str(phase284.get("state", "event_lifecycle_exit_side_redesign_precommit_open"))
        if phase285_complete == 1:
            real_receive_status = str(phase285.get("state", "event_lifecycle_exit_side_redesign_search_open"))
        if phase286_complete == 1:
            real_receive_status = str(phase286.get("state", "event_lifecycle_exit_side_redesign_interpretation_open"))
        if phase287_complete == 1:
            real_receive_status = str(phase287.get("state", "full_depth_liquidity_pressure_strategy_search_open"))
        if phase288_complete == 1:
            real_receive_status = str(phase288.get("state", "full_depth_liquidity_pressure_interpretation_open"))
        if phase289_complete == 1:
            real_receive_status = str(phase289.get("state", "adaptive_full_depth_liquidity_pressure_expansion_search_open"))
        if phase290_complete == 1:
            real_receive_status = str(phase290.get("state", "adaptive_full_depth_liquidity_pressure_interpretation_open"))
        if phase291_complete == 1:
            real_receive_status = str(phase291.get("state", "adaptive_pressure_breadth_repair_search_open"))
        if phase292_complete == 1:
            real_receive_status = str(phase292.get("state", "adaptive_pressure_breadth_repair_interpretation_open"))
        if phase293_complete == 1:
            real_receive_status = str(phase293.get("state", "full_depth_pressure_absorption_continuation_search_open"))
        if phase294_complete == 1:
            real_receive_status = str(phase294.get("state", "full_depth_pressure_absorption_continuation_interpretation_open"))
        if phase295_complete == 1:
            real_receive_status = str(phase295.get("state", "full_year_top5_depth_strategy_family_sweep_open"))
        if phase296_complete == 1:
            real_receive_status = str(phase296.get("state", "full_year_top5_depth_strategy_family_sweep_interpretation_open"))
        if phase297_complete == 1:
            real_receive_status = str(phase297.get("state", "raw_dense_top5_book_state_strategy_sweep_open"))
        if phase298_complete == 1:
            real_receive_status = str(phase298.get("state", "raw_dense_top5_book_state_strategy_sweep_interpretation_open"))
        if phase299_complete == 1:
            real_receive_status = str(phase299.get("state", "passive_aware_execution_hybrid_precommit_open"))
        if phase300_complete == 1:
            real_receive_status = str(phase300.get("state", "passive_aware_execution_hybrid_execution_open"))
        if phase300_execution_complete == 1:
            real_receive_status = str(phase300.get("state", "passive_aware_execution_hybrid_interpretation_open"))
        if phase301_complete == 1:
            real_receive_status = str(phase301.get("state", "terminal_retail_top5_l2_alpha_thesis_report_open"))
        if phase302_complete == 1:
            real_receive_status = str(phase302.get("state", "retail_top5_l2_alpha_thesis_closed_terminal_report_complete"))
        if phase303_complete == 1:
            real_receive_status = str(phase303.get("state", "material_new_event_catalyst_source_acquisition_open"))
        if phase304_complete == 1:
            real_receive_status = str(phase304.get("state", "event_catalyst_dropzone_population_open"))
        if phase305_complete == 1:
            real_receive_status = str(phase305.get("state", "event_catalyst_source_import_blocked_dropzone_unpopulated"))
        if phase306_complete == 1:
            real_receive_status = str(phase306.get("state", "event_catalyst_top5_depth_join_materialization_open"))
        if phase307_complete == 1:
            real_receive_status = str(phase307.get("state", "event_catalyst_top5_depth_join_blocked_no_timestamp_overlap"))
        if phase308_complete == 1:
            real_receive_status = str(phase308.get("state", "event_catalyst_feature_precommit_open"))
        if phase309_complete == 1:
            real_receive_status = str(phase309.get("state", "event_catalyst_feature_materialization_open"))
        if phase310_complete == 1:
            real_receive_status = str(phase310.get("state", "event_catalyst_strategy_search_precommit_open"))
        if phase311_complete == 1:
            real_receive_status = str(phase311.get("state", "event_catalyst_training_strategy_search_open"))
        if phase312_complete == 1:
            real_receive_status = str(phase312.get("state", "event_catalyst_training_strategy_search_interpretation_open"))
        if phase313_complete == 1:
            real_receive_status = str(phase313.get("state", "event_catalyst_multievent_synthetic_breadth_precommit_open"))
        if phase314_complete == 1:
            real_receive_status = str(phase314.get("state", "event_catalyst_multievent_synthetic_breadth_materialization_open"))
        if phase315_complete == 1:
            real_receive_status = str(phase315.get("state", "event_catalyst_multievent_top5_depth_join_precommit_open"))
        if phase316_complete == 1:
            real_receive_status = str(phase316.get("state", "event_catalyst_multievent_top5_depth_join_materialization_open"))
        if phase317_complete == 1:
            real_receive_status = str(phase317.get("state", "event_catalyst_multievent_join_quality_audit_open"))
        if phase318_complete == 1:
            real_receive_status = str(phase318.get("state", "event_catalyst_multievent_feature_materialization_precommit_open"))
        if phase319_complete == 1:
            real_receive_status = str(phase319.get("state", "event_catalyst_multievent_feature_materialization_open"))
        if phase320_complete == 1:
            real_receive_status = str(phase320.get("state", "event_catalyst_multievent_strategy_search_precommit_open"))
        if phase321_complete == 1:
            real_receive_status = str(phase321.get("state", "event_catalyst_multievent_training_strategy_search_open"))
        if phase322_complete == 1:
            real_receive_status = str(phase322.get("state", "event_catalyst_multievent_strategy_search_interpretation_open"))
        if phase323_complete == 1:
            real_receive_status = str(phase323.get("state", "event_catalyst_breadth_expansion_precommit_open"))
        if phase324_complete == 1:
            real_receive_status = str(phase324.get("state", "event_catalyst_breadth_expansion_materialization_open"))
        if phase325_complete == 1:
            real_receive_status = str(phase325.get("state", "event_catalyst_expanded_top5_depth_join_precommit_open"))
        if phase326_complete == 1:
            real_receive_status = str(phase326.get("state", "event_catalyst_expanded_top5_depth_join_materialization_open"))
        if phase327_complete == 1:
            real_receive_status = str(phase327.get("state", "event_catalyst_expanded_join_quality_audit_open"))
        if phase328_complete == 1:
            real_receive_status = str(phase328.get("state", "event_catalyst_expanded_feature_materialization_precommit_open"))
        if phase329_complete == 1:
            real_receive_status = str(phase329.get("state", "event_catalyst_expanded_feature_materialization_open"))
        if phase330_complete == 1:
            real_receive_status = str(phase330.get("state", "event_catalyst_expanded_strategy_search_precommit_open"))
        if phase331_complete == 1:
            real_receive_status = str(phase331.get("state", "event_catalyst_expanded_training_strategy_search_open"))
        if phase332_complete == 1:
            real_receive_status = str(phase332.get("state", "event_catalyst_expanded_strategy_search_interpretation_open"))
        if phase333_complete == 1:
            real_receive_status = str(phase333.get("state", "cost_stress_margin_redesign_precommit_open"))
        if phase334_complete == 1:
            real_receive_status = str(phase334.get("state", "cost_stress_margin_redesign_training_search_open"))
        if phase335_complete == 1:
            real_receive_status = str(phase335.get("state", "cost_stress_margin_redesign_interpretation_open"))
        if phase336_complete == 1:
            real_receive_status = str(phase336.get("state", "cost_stress_holdout_validation_precommit_open"))
        if phase337_complete == 1:
            real_receive_status = str(phase337.get("state", "cost_stress_holdout_validation_execution_open"))
    else:
        real_receive_status = "gated_waiting_for_two_more_real_l2_dates"
    real_receive_evidence = (
        f"Phase172 ready_dates={phase172.get('ready_receive_flow_dates', '')}, additional_dates_needed={phase172.get('additional_dates_needed', '')}; "
        f"Phase174 download_ran={phase174.get('download_ran', '')}; "
        f"Phase175 activation_ready={phase175.get('activation_ready', '')}; "
        f"Phase176 features_materialized={phase176.get('features_materialized', '')}; "
        f"Phase177 quality_audit_ran={phase177.get('feature_quality_audit_ran', '')}; "
        f"Phase178 handoff_ready={phase178.get('handoff_ready', '')}; "
        f"Phase179 precommit_ready={phase179.get('precommit_ready', '')}; "
        f"Phase180 precommit_ready={phase180.get('precommit_ready', '')}; "
        f"Phase181 labels_materialized={phase181.get('labels_materialized', '')}; "
        f"Phase182 label_audit_pass={phase182.get('label_quality_leakage_audit_pass', '')}; "
        f"Phase183 replay_readiness={phase183.get('replay_readiness_precommitted', '')}; "
        f"Phase184 dry_run_complete={phase184.get('train_validation_dry_run_complete', '')}, test_rows_used={phase184.get('test_rows_used', '')}, promotion_allowed={phase184.get('promotion_allowed', '')}; "
        f"Phase185 interpretation_complete={phase185.get('validation_interpretation_complete', '')}, cost_dominates={phase185.get('cost_dominates_validation_edge', '')}, test_replay_allowed_next={phase185.get('test_replay_allowed_next', '')}; "
        f"Phase186 family_set_closed={phase186.get('current_family_set_closed', '')}, reuse_without_redesign_allowed={phase186.get('reuse_without_redesign_allowed', '')}, test_replay_allowed_next={phase186.get('test_replay_allowed_next', '')}; "
        f"Phase187 candidate_complete={phase187.get('cost_aware_sparse_candidate_complete', '')}, validation_positive_all_profiles={phase187.get('validation_positive_all_profiles', '')}, test_replay_allowed_next={phase187.get('test_replay_allowed_next', '')}; "
        f"Phase188 interpretation_complete={phase188.get('sparse_candidate_interpretation_complete', '')}, breadth_warning={phase188.get('breadth_warning', '')}, date_count_warning={phase188.get('date_count_warning', '')}, test_replay_allowed_next={phase188.get('test_replay_allowed_next', '')}; "
        f"Phase189 decision_complete={phase189.get('test_precommit_decision_complete', '')}, test_precommit_allowed={phase189.get('untouched_test_replay_precommit_allowed', '')}, test_replay_allowed_next={phase189.get('test_replay_allowed_next', '')}; "
        f"Phase190 decision_complete={phase190.get('phase190_decision_complete', '')}, additional_validation_breadth_available_now={phase190.get('additional_validation_breadth_available_now', '')}, test_replay_execution={phase190.get('test_replay_execution', '')}; "
        f"Phase191 precommit_complete={phase191.get('diagnostic_test_precommit_complete', '')}, test_replay_execution={phase191.get('test_replay_execution', '')}, test_result_allowed={phase191.get('test_result_allowed', '')}; "
        f"Phase192 download_complete={phase192.get('real_validation_download_complete', '')}, test_replay_execution={phase192.get('test_replay_execution', '')}; "
        f"Phase193 extension_complete={phase193.get('validation_breadth_extension_complete', '')}, extension_dates={phase193.get('extension_validation_dates', '')}, min_profile_net={phase193.get('min_profile_net_bps_proxy_mean', '')}, breadth_warning={phase193.get('breadth_warning', '')}, test_replay_execution={phase193.get('test_replay_execution', '')}; "
        f"Phase194 fragility_decision_complete={phase194.get('fragility_decision_complete', '')}, all_extension_profile_dates_negative={phase194.get('all_extension_profile_dates_negative', '')}, test_replay_allowed_next={phase194.get('test_replay_allowed_next', '')}; "
        f"Phase195 redesign_search_complete={phase195.get('redesign_search_complete', '')}, passing_extension_gate_candidates={phase195.get('passing_extension_gate_candidates', '')}, best_candidate={phase195.get('best_candidate_id', '')}, best_min_extension_net={phase195.get('best_min_extension_net_bps', '')}, test_replay_allowed_next={phase195.get('test_replay_allowed_next', '')}; "
        f"Phase196 expanded_model_search_complete={phase196.get('expanded_model_search_complete', '')}, train_selected_model_rows={phase196.get('train_selected_model_rows', '')}, passing_extension_gate_models={phase196.get('passing_extension_gate_models', '')}, best_model={phase196.get('best_model_id', '')}, test_replay_allowed_next={phase196.get('test_replay_allowed_next', '')}; "
        f"Phase197 feature_precommit_complete={phase197.get('non_receive_flow_feature_precommit_complete', '')}, ready_feature_families={phase197.get('ready_feature_families', '')}, strategy_replay_allowed={phase197.get('strategy_replay_allowed', '')}, test_replay_allowed_next={phase197.get('test_replay_allowed_next', '')}; "
        f"Phase198 context_model_search_complete={phase198.get('context_model_search_complete', '')}, train_selected_model_rows={phase198.get('train_selected_model_rows', '')}, passing_extension_gate_models={phase198.get('passing_extension_gate_models', '')}, best_model={phase198.get('best_model_id', '')}, best_family={phase198.get('best_feature_family', '')}, test_replay_allowed_next={phase198.get('test_replay_allowed_next', '')}; "
        f"Phase199 branch_decision_complete={phase199.get('branch_decision_complete', '')}, current_branch_paused={phase199.get('current_branch_paused', '')}, material_redesign_required={phase199.get('material_redesign_required', '')}, test_replay_allowed_next={phase199.get('test_replay_allowed_next', '')}; "
        f"Phase200 precommit_complete={phase200.get('material_new_hypothesis_precommit_complete', '')}, selected_hypothesis={phase200.get('selected_hypothesis_id', '')}, label_contract_rows={phase200.get('label_contract_rows', '')}, stage_action_rows={phase200.get('stage_action_rows', '')}, test_replay_allowed_next={phase200.get('test_replay_allowed_next', '')}; "
        f"Phase201 stage01_complete={phase201.get('label_only_stage01_complete', '')}, joined_rows={phase201.get('joined_label_candidate_rows', '')}, pre_replay_candidates={phase201.get('pre_replay_candidate_rows', '')}, max_symbols={phase201.get('max_candidate_symbols', '')}, max_dates={phase201.get('max_candidate_trade_dates', '')}, test_replay_allowed_next={phase201.get('test_replay_allowed_next', '')}; "
        f"Phase202 redesign_precommit_complete={phase202.get('passive_feature_redesign_precommit_complete', '')}, redesigned_feature_rows={phase202.get('redesigned_feature_rows', '')}, acceptance_contract_rows={phase202.get('acceptance_contract_rows', '')}, phase203_action_rows={phase202.get('phase203_action_rows', '')}, test_replay_allowed_next={phase202.get('test_replay_allowed_next', '')}; "
        f"Phase203 label_materialization_complete={phase203.get('label_materialization_complete', '')}, materialized_label_rows={phase203.get('materialized_label_rows', '')}, redesigned_candidate_pass_rows={phase203.get('redesigned_candidate_pass_rows', '')}, max_symbols={phase203.get('max_candidate_symbols', '')}, max_dates={phase203.get('max_candidate_trade_dates', '')}, adverse_selection_ceiling_met={phase203.get('adverse_selection_ceiling_met', '')}, candidate_gate_open={phase203.get('candidate_gate_open', '')}, test_replay_allowed_next={phase203.get('test_replay_allowed_next', '')}; "
        f"Phase204 closure_decision_complete={phase204.get('closure_decision_complete', '')}, passive_redesign_closed_for_replay={phase204.get('current_passive_redesign_closed_for_replay', '')}, material_new_source_required={phase204.get('material_new_source_required', '')}, threshold_widening_allowed={phase204.get('threshold_widening_allowed', '')}, test_replay_allowed_next={phase204.get('test_replay_allowed_next', '')}; "
        f"Phase205 material_new_source_precommit_complete={phase205.get('material_new_source_precommit_complete', '')}, selected_route={phase205.get('selected_route_id', '')}, phase206_work_order_rows={phase205.get('phase206_work_order_rows', '')}, test_replay_allowed_next={phase205.get('test_replay_allowed_next', '')}; "
        f"Phase206 nonoverlap_feature_contract_complete={phase206.get('nonoverlap_feature_contract_complete', '')}, feature_catalog_rows={phase206.get('feature_catalog_rows', '')}, blocked_reference_rows={phase206.get('blocked_reference_rows', '')}, nonoverlap_pass_rows={phase206.get('nonoverlap_pass_rows', '')}, model_fit_allowed={phase206.get('model_fit_allowed', '')}, test_replay_allowed_next={phase206.get('test_replay_allowed_next', '')}; "
        f"Phase207 feature_matrix_precommit_complete={phase207.get('feature_matrix_precommit_complete', '')}, matrix_rows={phase207.get('feature_matrix_rows', '')}, available_rows={phase207.get('feature_available_rows', '')}, trade_dates={phase207.get('trade_dates_max', '')}, symbols={phase207.get('symbols_max', '')}, model_fit_allowed={phase207.get('model_fit_allowed', '')}, test_replay_allowed_next={phase207.get('test_replay_allowed_next', '')}; "
        f"Phase208 quality_gate_complete={phase208.get('feature_matrix_quality_gate_complete', '')}, quality_rows={phase208.get('quality_summary_rows', '')}, quality_pass_rows={phase208.get('quality_pass_rows', '')}, blocking_gaps={phase208.get('blocking_gap_rows', '')}, model_fit_allowed={phase208.get('model_fit_allowed', '')}, test_replay_allowed_next={phase208.get('test_replay_allowed_next', '')}; "
        f"Phase209 model_fit_precommit_spec_complete={phase209.get('model_fit_precommit_spec_complete', '')}, model_spec_rows={phase209.get('model_spec_rows', '')}, feature_set_rows={phase209.get('feature_set_rows', '')}, label_target_rows={phase209.get('label_target_rows', '')}, split_control_rows={phase209.get('split_control_rows', '')}, model_fit_execution_allowed={phase209.get('model_fit_execution_allowed', '')}, test_replay_allowed_next={phase209.get('test_replay_allowed_next', '')}; "
        f"Phase210 train_validation_model_fit_dry_run_complete={phase210.get('train_validation_model_fit_dry_run_complete', '')}, joined_rows={phase210.get('design_matrix_joined_rows', '')}, model_fit_rows={phase210.get('model_fit_rows', '')}, validation_metric_rows={phase210.get('validation_metric_rows', '')}, negative_control_rows={phase210.get('negative_control_rows', '')}, test_rows_used={phase210.get('test_rows_used', '')}, strategy_replay_allowed={phase210.get('strategy_replay_allowed', '')}, profitability_claim_allowed={phase210.get('profitability_claim_allowed', '')}; "
        f"Phase211 interpretation_complete={phase211.get('model_fit_validation_interpretation_complete', '')}, interpretation_rows={phase211.get('interpretation_rows', '')}, passing_rows={phase211.get('passing_interpretation_rows', '')}, candidate_opened_for_replay={phase211.get('candidate_opened_for_replay', '')}, strategy_replay_allowed={phase211.get('strategy_replay_allowed', '')}, profitability_claim_allowed={phase211.get('profitability_claim_allowed', '')}; "
        f"Phase212 closure_complete={phase212.get('model_family_closure_or_redesign_precommit_complete', '')}, families_closed={phase212.get('families_closed_for_replay', '')}, redesign_rows={phase212.get('redesign_precommit_rows', '')}, model_fit_allowed_next={phase212.get('model_fit_allowed_next', '')}, strategy_replay_allowed={phase212.get('strategy_replay_allowed', '')}, profitability_claim_allowed={phase212.get('profitability_claim_allowed', '')}; "
        f"Phase213 source_precommit_complete={phase213.get('material_new_model_source_precommit_complete', '')}, selected_source={phase213.get('selected_source_id', '')}, label_contract_rows={phase213.get('label_contract_rows', '')}, phase214_work_order_rows={phase213.get('phase214_work_order_rows', '')}, model_fit_allowed_next={phase213.get('model_fit_allowed_next', '')}, strategy_replay_allowed={phase213.get('strategy_replay_allowed', '')}; "
        f"Phase214 label_materialization_complete={phase214.get('event_surprise_label_materialization_complete', '')}, label_rows={phase214.get('label_rows', '')}, event_surprise_rows={phase214.get('event_surprise_rows', '')}, quality_pass_rows={phase214.get('quality_pass_rows', '')}, sealed_test_rows_used={phase214.get('sealed_test_rows_used', '')}, strategy_replay_allowed={phase214.get('strategy_replay_allowed', '')}; "
        f"Phase215 quality_interpretation_complete={phase215.get('event_surprise_label_quality_interpretation_complete', '')}, passing_rows={phase215.get('passing_interpretation_rows', '')}, families_with_interpretable_rows={phase215.get('label_families_with_interpretable_rows', '')}, phase216_work_order_rows={phase215.get('phase216_work_order_rows', '')}, model_fit_allowed_next={phase215.get('model_fit_allowed_next', '')}, strategy_replay_allowed={phase215.get('strategy_replay_allowed', '')}; "
        f"Phase216 event_only_precommit_complete={phase216.get('event_surprise_event_only_target_precommit_complete', '')}, target_rows={phase216.get('event_only_target_rows', '')}, full_train_validation_targets={phase216.get('full_train_validation_target_rows', '')}, excluded_targets={phase216.get('excluded_target_rows', '')}, model_fit_allowed_next={phase216.get('model_fit_allowed_next', '')}, strategy_replay_allowed={phase216.get('strategy_replay_allowed', '')}; "
        f"Phase217 design_matrix_precommit_complete={phase217.get('event_only_design_matrix_precommit_complete', '')}, target_scope_rows={phase217.get('target_scope_rows', '')}, feature_binding_rows={phase217.get('feature_binding_rows', '')}, target_row_observation_scope={phase217.get('target_row_observation_scope', '')}, row_level_export_allowed={phase217.get('row_level_design_matrix_export_allowed', '')}, model_fit_allowed_next={phase217.get('model_fit_allowed_next', '')}, strategy_replay_allowed={phase217.get('strategy_replay_allowed', '')}; "
        f"Phase218 model_fit_precommit_complete={phase218.get('event_only_model_fit_precommit_or_stop_complete', '')}, dry_run_precommitted_for_phase219={phase218.get('model_fit_dry_run_precommitted_for_phase219', '')}, model_specs={phase218.get('model_spec_rows', '')}, target_contracts={phase218.get('target_contract_rows', '')}, feature_contracts={phase218.get('feature_contract_rows', '')}, phase218_model_fit_execution_allowed={phase218.get('model_fit_execution_allowed', '')}, strategy_replay_allowed={phase218.get('strategy_replay_allowed', '')}; "
        f"Phase219 model_fit_dry_run_complete={phase219.get('event_only_train_validation_model_fit_dry_run_complete', '')}, event_only_joined_rows={phase219.get('event_only_joined_rows', '')}, model_fit_rows={phase219.get('model_fit_rows', '')}, validation_metric_rows={phase219.get('validation_metric_rows', '')}, control_rows={phase219.get('control_rows', '')}, model_fit_execution={phase219.get('model_fit_execution', '')}, strategy_replay_allowed={phase219.get('strategy_replay_allowed', '')}, test_rows_used={phase219.get('test_rows_used', '')}; "
        f"Phase220 validation_interpretation_complete={phase220.get('event_only_model_fit_validation_interpretation_complete', '')}, passing_candidates={phase220.get('passing_candidate_rows', '')}, candidate_families={phase220.get('candidate_family_rows', '')}, best_mse_improvement_vs_base={phase220.get('best_mse_improvement_vs_base', '')}, best_correlation={phase220.get('best_validation_correlation', '')}, candidate_opened_for_phase221={phase220.get('candidate_opened_for_phase221_precommit', '')}, strategy_replay_allowed={phase220.get('strategy_replay_allowed', '')}; "
        f"Phase221 signal_replay_precommit_complete={phase221.get('event_only_signal_replay_precommit_or_stop_complete', '')}, frozen_candidates={phase221.get('candidate_rows', '')}, signal_rules={phase221.get('signal_rule_rows', '')}, phase222_replay_precommitted={phase221.get('phase222_replay_dry_run_precommitted', '')}, phase221_replay_execution_allowed={phase221.get('strategy_replay_execution_allowed', '')}, test_replay_allowed_next={phase221.get('test_replay_allowed_next', '')}, profitability_claim_allowed={phase221.get('profitability_claim_allowed', '')}; "
        f"Phase222 signal_replay_dry_run_complete={phase222.get('event_only_train_validation_signal_replay_dry_run_complete', '')}, event_only_joined_rows={phase222.get('event_only_joined_rows', '')}, replay_summary_rows={phase222.get('replay_summary_rows', '')}, validation_decision_events={phase222.get('validation_decision_events', '')}, best_validation_net_after_cost_bps_proxy={phase222.get('best_validation_net_after_cost_bps_proxy', '')}, strategy_replay_execution={phase222.get('strategy_replay_execution', '')}, test_rows_used={phase222.get('test_rows_used', '')}, profitability_claim_allowed={phase222.get('profitability_claim_allowed', '')}; "
        f"Phase223 validation_interpretation_complete={phase223.get('event_only_signal_replay_validation_interpretation_complete', '')}, interpretation_rows={phase223.get('interpretation_rows', '')}, positive_net_validation_rows={phase223.get('positive_net_validation_rows', '')}, passing_interpretation_rows={phase223.get('passing_interpretation_rows', '')}, best_validation_net_after_cost_bps_proxy={phase223.get('best_validation_net_after_cost_bps_proxy', '')}, best_actual_vs_shuffle_net_edge_bps={phase223.get('best_actual_vs_shuffle_net_edge_bps', '')}, phase224_work_order_rows={phase223.get('phase224_work_order_rows', '')}, broader_replay_allowed_next={phase223.get('broader_replay_allowed_next', '')}, test_rows_used={phase223.get('test_rows_used', '')}, profitability_claim_allowed={phase223.get('profitability_claim_allowed', '')}; "
        f"Phase224 closure_or_redesign_complete={phase224.get('event_only_signal_replay_closure_or_redesign_precommit_complete', '')}, candidate_set_closed_for_broader={phase224.get('current_candidate_set_closed_for_broader_replay', '')}, candidate_set_closed_for_test={phase224.get('current_candidate_set_closed_for_test', '')}, failure_modes={phase224.get('failure_mode_rows', '')}, redesign_routes={phase224.get('redesign_route_rows', '')}, selected_redesign_route={phase224.get('selected_redesign_route', '')}, phase225_work_order_rows={phase224.get('phase225_work_order_rows', '')}, model_fit_allowed_next={phase224.get('model_fit_allowed_next', '')}, broader_replay_allowed_next={phase224.get('broader_replay_allowed_next', '')}, profitability_claim_allowed={phase224.get('profitability_claim_allowed', '')}; "
        f"Phase225 cost_aware_redesign_precommit_complete={phase225.get('cost_aware_event_source_redesign_precommit_complete', '')}, cost_hurdles={phase225.get('cost_hurdle_rows', '')}, label_contracts={phase225.get('label_contract_rows', '')}, negative_controls={phase225.get('negative_control_rows', '')}, selected_route={phase225.get('selected_route_id', '')}, label_materialization_allowed_next={phase225.get('label_materialization_allowed_next', '')}, model_fit_allowed_next={phase225.get('model_fit_allowed_next', '')}, strategy_replay_allowed={phase225.get('strategy_replay_allowed', '')}, test_rows_used={phase225.get('test_rows_used', '')}, profitability_claim_allowed={phase225.get('profitability_claim_allowed', '')}; "
        f"Phase226 cost_aware_label_materialization_complete={phase226.get('cost_aware_event_label_materialization_dry_run_complete', '')}, availability_rows={phase226.get('horizon_availability_rows', '')}, available_horizons={phase226.get('available_horizon_rows', '')}, blocked_horizons={phase226.get('blocked_horizon_rows', '')}, label_partitions={phase226.get('label_partition_rows', '')}, total_label_rows={phase226.get('total_label_rows', '')}, actionable_rows={phase226.get('cost_aware_actionable_rows', '')}, quality_pass_rows={phase226.get('quality_pass_rows', '')}, sealed_test_rows_available={phase226.get('sealed_test_rows_available', '')}, test_rows_used={phase226.get('test_rows_used', '')}, model_fit_allowed_next={phase226.get('model_fit_allowed_next', '')}, profitability_claim_allowed={phase226.get('profitability_claim_allowed', '')}; "
        f"Phase227 quality_interpretation_complete={phase227.get('cost_aware_event_label_quality_interpretation_complete', '')}, quality_rows={phase227.get('quality_interpretation_rows', '')}, horizon_rows={phase227.get('horizon_interpretation_rows', '')}, failure_modes={phase227.get('failure_mode_rows', '')}, actionable_rows={phase227.get('actionable_rows', '')}, quality_pass_rows={phase227.get('quality_pass_rows', '')}, fit_precommit_candidates={phase227.get('fit_precommit_candidate_rows', '')}, phase228_work_order_rows={phase227.get('phase228_work_order_rows', '')}, model_fit_allowed_next={phase227.get('model_fit_allowed_next', '')}, test_rows_used={phase227.get('test_rows_used', '')}, profitability_claim_allowed={phase227.get('profitability_claim_allowed', '')}; "
        f"Phase228 closure_or_relaxation_complete={phase228.get('cost_aware_label_redesign_closure_or_relaxation_precommit_complete', '')}, closed_for_fit={phase228.get('current_label_set_closed_for_fit', '')}, closed_for_replay={phase228.get('current_label_set_closed_for_replay', '')}, redesign_routes={phase228.get('redesign_route_rows', '')}, guardrails={phase228.get('guardrail_rows', '')}, selected_route={phase228.get('selected_route_id', '')}, phase229_work_order_rows={phase228.get('phase229_work_order_rows', '')}, label_materialization_allowed_next={phase228.get('label_materialization_allowed_next', '')}, threshold_widening_allowed={phase228.get('threshold_widening_allowed', '')}, model_fit_allowed_next={phase228.get('model_fit_allowed_next', '')}, profitability_claim_allowed={phase228.get('profitability_claim_allowed', '')}; "
        f"Phase229 multi_strategy_search_complete={phase229.get('multi_strategy_profitability_search_complete', '')}, distinct_strategy_ids={phase229.get('distinct_strategy_ids', '')}, realistic_profile_rows={phase229.get('realistic_profile_rows', '')}, positive_realistic_candidates={phase229.get('positive_realistic_candidate_rows', '')}, positive_any_profile_rows={phase229.get('positive_any_profile_rows', '')}, best_strategy={phase229.get('best_strategy_id', '')}, best_annual_net_pnl={phase229.get('best_annual_net_pnl_inr', '')}; "
        f"Phase230 low_turnover_high_edge_complete={phase230.get('low_turnover_high_edge_search_complete', '')}, variant_group_rows={phase230.get('variant_group_rows', '')}, positive_expanded_groups={phase230.get('positive_expanded_group_rows', '')}, positive_oracle_signed_groups={phase230.get('positive_oracle_signed_group_rows', '')}, best_scope={phase230.get('best_scope', '')}, best_variant={phase230.get('best_expanded_variant', '')}, best_net_pnl={phase230.get('best_expanded_net_pnl_inr', '')}, profitability_claim_allowed={phase230.get('profitability_claim_allowed', '')}; "
        f"Phase231 material_new_forms_complete={phase231.get('material_new_strategy_forms_complete', '')}, candidate_rows={phase231.get('candidate_rows', '')}, train_pass={phase231.get('train_pass_candidates', '')}, test_pass={phase231.get('test_pass_candidates', '')}, synthetic_candidates={phase231.get('synthetic_candidate_rows', '')}, best_candidate={phase231.get('best_candidate_id', '')}, best_test_net_pnl={phase231.get('best_test_net_pnl_inr', '')}, profitability_claim_allowed={phase231.get('profitability_claim_allowed', '')}; "
        f"Phase232 validation_complete={phase232.get('validate_phase231_candidates_complete', '')}, validated_candidates={phase232.get('validated_synthetic_candidate_rows', '')}, negative_control_pass={phase232.get('negative_control_pass_rows', '')}, cost_stress_pass={phase232.get('cost_stress_pass_rows', '')}, holdout_stability_pass={phase232.get('holdout_stability_pass_rows', '')}, best_candidate={phase232.get('best_candidate_id', '')}, best_test_net_pnl={phase232.get('best_test_net_pnl_inr', '')}, profitability_claim_allowed={phase232.get('profitability_claim_allowed', '')}; "
        f"Phase233 fragility_realism_complete={phase233.get('fragility_realism_validation_complete', '')}, pass={phase233.get('fragility_realism_pass', '')}, neighbor_pass={phase233.get('neighbor_pass_rows', '')}, parent_test_2x_cost_net={phase233.get('parent_test_2x_cost_net_pnl_inr', '')}, profitability_claim_allowed={phase233.get('profitability_claim_allowed', '')}; "
        f"Phase234 holdout_preparation_complete={phase234.get('holdout_preparation_complete', '')}, selected_route={phase234.get('selected_route_id', '')}, real_anchor_route_ready={phase234.get('real_anchor_route_ready', '')}, required_schema_present={phase234.get('required_schema_present_rows', '')}/{phase234.get('required_schema_rows', '')}, phase235_work_order_rows={phase234.get('phase235_work_order_rows', '')}, profitability_claim_allowed={phase234.get('profitability_claim_allowed', '')}; "
        f"Phase235 real_anchor_replay_complete={phase235.get('real_anchor_microprice_replay_complete', '')}, pass={phase235.get('real_anchor_replay_pass', '')}, trades={phase235.get('real_anchor_trade_rows', '')}, net_pnl={phase235.get('real_anchor_net_pnl_inr', '')}, dates={phase235.get('real_anchor_dates', '')}, symbols={phase235.get('real_anchor_symbols', '')}, profitability_claim_allowed={phase235.get('profitability_claim_allowed', '')}; "
        f"Phase236 neighbor_search_complete={phase236.get('real_anchor_neighbor_search_complete', '')}, positive_variants={phase236.get('positive_real_anchor_variant_rows', '')}, breadth_passing_variants={phase236.get('breadth_passing_variant_rows', '')}, best_candidate={phase236.get('best_candidate_id', '')}, best_net_pnl={phase236.get('best_real_anchor_net_pnl_inr', '')}, best_trades={phase236.get('best_real_anchor_trade_rows', '')}, profitability_claim_allowed={phase236.get('profitability_claim_allowed', '')}; "
        f"Phase237 threshold_transfer_complete={phase237.get('threshold_transfer_search_complete', '')}, breadth_positive_candidates={phase237.get('breadth_positive_candidate_rows', '')}, best_candidate={phase237.get('best_candidate_id', '')}, best_family={phase237.get('best_family_id', '')}, best_net_pnl={phase237.get('best_real_anchor_net_pnl_inr', '')}, best_trades={phase237.get('best_real_anchor_trade_rows', '')}, phase238_opened={phase237.get('candidate_opened_for_phase238', '')}, profitability_claim_allowed={phase237.get('profitability_claim_allowed', '')}; "
        f"Phase238 validation_precommit_complete={phase238.get('validation_precommit_complete', '')}, candidate={phase238.get('candidate_id', '')}, local_unseen_dates_available={phase238.get('local_unseen_validation_dates_available', '')}, min_unseen_dates_required={phase238.get('min_unseen_validation_dates_required', '')}, phase239_work_order_rows={phase238.get('phase239_work_order_rows', '')}, profitability_claim_allowed={phase238.get('profitability_claim_allowed', '')}; "
        f"Phase239 unseen_date_audit_complete={phase239.get('unseen_date_acquisition_audit_complete', '')}, local_unseen_dates={phase239.get('local_unseen_candidate_dates', '')}, target_unseen_dates={phase239.get('target_unseen_date_rows', '')}, azure_ready={phase239.get('azure_storage_listing_ready', '')}, download_plan_rows={phase239.get('download_plan_rows', '')}, profitability_claim_allowed={phase239.get('profitability_claim_allowed', '')}; "
        f"Phase240 raw_l2_download_complete={phase240.get('unseen_raw_l2_download_complete', '')}, partial_attempt={phase240.get('partial_attempt', '')}, target_dates={phase240.get('target_trade_dates', '')}, completed_files={phase240.get('completed_files', '')}, failed_files={phase240.get('failed_files', '')}, completed_dates={phase240.get('completed_dates', '')}, profitability_claim_allowed={phase240.get('profitability_claim_allowed', '')}; "
        f"Phase241 one_date_complete={phase241.get('one_date_unseen_diagnostic_complete', '')}, candidate={phase241.get('candidate_id', '')}, trade_date={phase241.get('trade_date', '')}, trades={phase241.get('trade_rows', '')}, net_pnl={phase241.get('net_pnl_inr', '')}, controls={phase241.get('control_pass_rows', '')}/{phase241.get('control_rows', '')}, survived={phase241.get('one_date_diagnostic_candidate_survived', '')}, profitability_claim_allowed={phase241.get('profitability_claim_allowed', '')}; "
        f"Phase242 closed_candidate={phase242.get('closed_candidate_id', '')}, redesign_queue_rows={phase242.get('redesign_queue_rows', '')}, download_more_dates_allowed={phase242.get('download_more_dates_for_closed_candidate_allowed', '')}, holdout_tuning_allowed={phase242.get('holdout_parameter_tuning_allowed', '')}, profitability_claim_allowed={phase242.get('profitability_claim_allowed', '')}; "
        f"Phase243 redesign_complete={phase243.get('cost_stress_first_redesign_complete', '')}, survivors={phase243.get('survivor_candidate_rows', '')}, best_candidate={phase243.get('best_candidate_id', '')}, best_2x_cost_net={phase243.get('best_cost200_net_pnl_inr', '')}, random_beat={phase243.get('best_random_beat_fraction', '')}, future_holdout_precommit_allowed={phase243.get('future_holdout_precommit_allowed', '')}, profitability_claim_allowed={phase243.get('profitability_claim_allowed', '')}; "
        f"Phase244 precommit_complete={phase244.get('future_holdout_precommit_complete', '')}, frozen_candidate={phase244.get('candidate_id', '')}, min_holdout_dates={phase244.get('min_holdout_dates_required', '')}, storage_decision_required={phase244.get('storage_decision_required', '')}, download_now_allowed={phase244.get('download_more_dates_now_allowed', '')}, holdout_execution_now={phase244.get('future_holdout_execution_allowed_now', '')}, profitability_claim_allowed={phase244.get('profitability_claim_allowed', '')}; "
        f"Phase245 storage_audit_complete={phase245.get('storage_decision_audit_complete', '')}, free_gb={phase245.get('free_gb_now', '')}, projected_required_gb={phase245.get('projected_required_gb', '')}, local_feasible_space_only={phase245.get('local_download_feasible_by_space_only', '')}, cleanup_candidates={phase245.get('cleanup_candidate_rows', '')}, download_now_allowed={phase245.get('download_more_dates_now_allowed', '')}; "
        f"Phase246 one_date_complete={phase246.get('fresh_one_date_holdout_diagnostic_complete', '')}, candidate={phase246.get('candidate_id', '')}, trade_date={phase246.get('trade_date', '')}, trades={phase246.get('trade_rows', '')}, net_pnl={phase246.get('net_pnl_inr', '')}, symbols={phase246.get('symbols', '')}, controls={phase246.get('control_pass_rows', '')}/{phase246.get('control_rows', '')}, survived={phase246.get('one_date_diagnostic_candidate_survived', '')}, profitability_claim_allowed={phase246.get('profitability_claim_allowed', '')}; "
        f"Phase247 redesign_precommit_complete={phase247.get('l2_imbalance_regime_filter_redesign_precommit_complete', '')}, parent={phase247.get('parent_candidate_id', '')}, redesign_candidates={phase247.get('redesign_candidate_rows', '')}, l2_filter_required={phase247.get('l2_imbalance_filter_required', '')}, forbidden_tuning_dates={phase247.get('forbidden_tuning_dates', '')}, training_search_allowed_next={phase247.get('training_search_allowed_next', '')}, profitability_claim_allowed={phase247.get('profitability_claim_allowed', '')}; "
        f"Phase248 search_complete={phase248.get('l2_imbalance_regime_filtered_search_complete', '')}, variants={phase248.get('variant_rows', '')}, cost200_positive={phase248.get('cost200_positive_variant_rows', '')}, controlled={phase248.get('controlled_candidate_rows', '')}, survivors={phase248.get('survivor_candidate_rows', '')}, best={phase248.get('best_candidate_id', '')}, best_cost200={phase248.get('best_cost200_net_pnl_inr', '')}, future_holdout_precommit_allowed={phase248.get('future_holdout_precommit_allowed', '')}, profitability_claim_allowed={phase248.get('profitability_claim_allowed', '')}; "
        f"Phase249 close_or_broaden_complete={phase249.get('close_or_broaden_complete', '')}, closed_scope={phase249.get('closed_scope', '')}, selected_next_route={phase249.get('selected_next_route', '')}, broaden_queue_rows={phase249.get('broaden_queue_rows', '')}, threshold_relaxation_only_allowed={phase249.get('threshold_relaxation_only_allowed', '')}, download_now_allowed={phase249.get('download_more_dates_now_allowed', '')}, profitability_claim_allowed={phase249.get('profitability_claim_allowed', '')}; "
        f"Phase250 pair_basket_precommit_complete={phase250.get('pair_basket_precommit_complete', '')}, selected_route={phase250.get('selected_route', '')}, grouped_symbols={phase250.get('grouped_symbols', '')}, candidate_families={phase250.get('candidate_family_rows', '')}, phase251_allowed={phase250.get('phase251_training_search_allowed_next', '')}, download_now_allowed={phase250.get('download_more_dates_now_allowed', '')}, replay_now_allowed={phase250.get('replay_execution_allowed_now', '')}, profitability_claim_allowed={phase250.get('profitability_claim_allowed', '')}; "
        f"Phase251 pair_basket_search_complete={phase251.get('pair_basket_search_complete', '')}, variants={phase251.get('variant_rows', '')}, full_top_five_depth_variants={phase251.get('full_top_five_depth_variant_rows', '')}, depth_beyond_l1_variants={phase251.get('depth_beyond_l1_variant_rows', '')}, base_positive={phase251.get('net_positive_variant_rows', '')}, cost200_positive={phase251.get('cost200_positive_variant_rows', '')}, survivors={phase251.get('survivor_candidate_rows', '')}, best={phase251.get('best_candidate_id', '')}, best_net={phase251.get('best_training_net_pnl_inr', '')}, profitability_claim_allowed={phase251.get('profitability_claim_allowed', '')}; "
        f"Phase252 close_or_broaden_complete={phase252.get('close_or_broaden_complete', '')}, closed_scope={phase252.get('closed_scope', '')}, selected_next_route={phase252.get('selected_next_route', '')}, raw_depth_schema={phase252.get('raw_depth_schema_present_rows', '')}/{phase252.get('raw_depth_schema_rows', '')}, download_now_allowed={phase252.get('download_more_dates_now_allowed', '')}, profitability_claim_allowed={phase252.get('profitability_claim_allowed', '')}; "
        f"Phase253 richer_raw_depth_precommit_complete={phase253.get('richer_raw_depth_precommit_complete', '')}, usable_raw_roots={phase253.get('usable_raw_root_rows', '')}, schema={phase253.get('schema_present_rows', '')}/{phase253.get('schema_rows', '')}, raw_depth_level_columns={phase253.get('raw_depth_level_columns', '')}, feature_catalog_rows={phase253.get('feature_catalog_rows', '')}, phase254_allowed={phase253.get('phase254_materialization_allowed_next', '')}, profitability_claim_allowed={phase253.get('profitability_claim_allowed', '')}; "
        f"Phase254 richer_raw_depth_materialization_complete={phase254.get('richer_raw_depth_materialization_complete', '')}, event_bars={phase254.get('event_bar_rows', '')}, dates={phase254.get('trade_dates', '')}, symbols={phase254.get('symbols', '')}, source_ticks={phase254.get('source_tick_rows', '')}, excluded_invalid_ticks={phase254.get('excluded_invalid_source_tick_rows', '')}, hard_gates={phase254.get('hard_gate_pass_rows', '')}/{phase254.get('hard_gate_rows', '')}, profitability_claim_allowed={phase254.get('profitability_claim_allowed', '')}; "
        f"Phase255 feature_quality_interpretation_complete={phase255.get('feature_quality_interpretation_complete', '')}, healthy_features={phase255.get('healthy_feature_rows', '')}/{phase255.get('feature_rows', '')}, healthy_full_depth_features={phase255.get('healthy_full_depth_feature_rows', '')}/{phase255.get('full_depth_feature_rows', '')}, max_abs_full_depth_ic={phase255.get('max_abs_full_depth_spearman_ic', '')}, top_full_depth_feature={phase255.get('top_full_depth_feature', '')}, strategy_search_allowed_next={phase255.get('strategy_search_allowed_next', '')}, profitability_claim_allowed={phase255.get('profitability_claim_allowed', '')}; "
        f"Phase256 strategy_search_complete={phase256.get('strategy_search_complete', '')}, variants={phase256.get('variant_rows', '')}, full_depth_variants={phase256.get('full_top_five_depth_variant_rows', '')}, cost100_positive={phase256.get('cost100_positive_variant_rows', '')}, cost200_positive={phase256.get('cost200_positive_variant_rows', '')}, survivors={phase256.get('survivor_candidate_rows', '')}, best={phase256.get('best_candidate_id', '')}, best_cost100={phase256.get('best_cost100_net_pnl_inr', '')}, best_cost200={phase256.get('best_cost200_net_pnl_inr', '')}, profitability_claim_allowed={phase256.get('profitability_claim_allowed', '')}; "
        f"Phase257 interpretation_complete={phase257.get('interpretation_complete', '')}, closed_taker_threshold={phase257.get('closed_taker_threshold_route', '')}, full_depth_preserved={phase257.get('full_top_five_depth_preserved', '')}, selected_next_route={phase257.get('selected_next_route', '')}, threshold_relaxation_only_allowed={phase257.get('threshold_relaxation_only_allowed', '')}, profitability_claim_allowed={phase257.get('profitability_claim_allowed', '')}; "
        f"Phase258 passive_queue_precommit_complete={phase258.get('passive_queue_precommit_complete', '')}, route={phase258.get('selected_route', '')}, families={phase258.get('candidate_family_rows', '')}, controls={phase258.get('control_contract_rows', '')}, full_depth_required={phase258.get('full_top_five_depth_required', '')}, l1_only_allowed={phase258.get('l1_only_candidate_allowed', '')}, profitability_claim_allowed={phase258.get('profitability_claim_allowed', '')}; "
        f"Phase259 passive_training_search_complete={phase259.get('passive_training_search_complete', '')}, variants={phase259.get('variant_rows', '')}, full_depth_variants={phase259.get('full_top_five_depth_variant_rows', '')}, cost100_positive={phase259.get('cost100_positive_variant_rows', '')}, cost200_positive={phase259.get('cost200_positive_variant_rows', '')}, survivors={phase259.get('survivor_candidate_rows', '')}, best={phase259.get('best_candidate_id', '')}, best_cost100={phase259.get('best_cost100_expected_net_pnl_inr', '')}, best_cost200={phase259.get('best_cost200_expected_net_pnl_inr', '')}, profitability_claim_allowed={phase259.get('profitability_claim_allowed', '')}; "
        f"Phase260 interpretation_complete={phase260.get('interpretation_complete', '')}, close_phase259_for_promotion={phase260.get('close_phase259_for_promotion', '')}, full_passive_route_closed={phase260.get('full_passive_route_closed', '')}, selected_next_route={phase260.get('selected_next_route', '')}, full_depth_preserved={phase260.get('full_top_five_depth_preserved', '')}, profitability_claim_allowed={phase260.get('profitability_claim_allowed', '')}; "
        f"Phase261 passive_repair_precommit_complete={phase261.get('passive_repair_precommit_complete', '')}, route={phase261.get('selected_route', '')}, fill_grid={phase261.get('fill_probability_grid_rows', '')}, families={phase261.get('candidate_family_rows', '')}, full_depth_required={phase261.get('full_top_five_depth_required', '')}, levels_2_to_5_required={phase261.get('levels_2_to_5_materiality_required', '')}, l1_only_allowed={phase261.get('l1_only_candidate_allowed', '')}, profitability_claim_allowed={phase261.get('profitability_claim_allowed', '')}; "
        f"Phase262 passive_training_search_complete={phase262.get('passive_training_search_complete', '')}, variants={phase262.get('variant_rows', '')}, full_depth_variants={phase262.get('full_top_five_depth_variant_rows', '')}, levels_2_to_5_variants={phase262.get('depth_beyond_l1_variant_rows', '')}, l1_only_variants={phase262.get('l1_only_variant_rows', '')}, fill_models={phase262.get('fill_model_rows_used', '')}, cost100_positive={phase262.get('cost100_positive_variant_rows', '')}, cost200_positive={phase262.get('cost200_positive_variant_rows', '')}, survivors={phase262.get('survivor_candidate_rows', '')}, best={phase262.get('best_candidate_id', '')}, best_cost100={phase262.get('best_cost100_expected_net_pnl_inr', '')}, best_cost200={phase262.get('best_cost200_expected_net_pnl_inr', '')}, profitability_claim_allowed={phase262.get('profitability_claim_allowed', '')}; "
        f"Phase263 interpretation_complete={phase263.get('interpretation_complete', '')}, close_passive_route={phase263.get('close_passive_spread_capture_fill_model_route', '')}, full_depth_preserved={phase263.get('full_top_five_depth_preserved', '')}, threshold_relaxation_only_allowed={phase263.get('threshold_relaxation_only_allowed', '')}, selected_next_route={phase263.get('selected_next_route', '')}, profitability_claim_allowed={phase263.get('profitability_claim_allowed', '')}; "
        f"Phase264 liquidity_shock_precommit_complete={phase264.get('liquidity_shock_precommit_complete', '')}, route={phase264.get('selected_route', '')}, features={phase264.get('feature_catalog_rows', '')}, families={phase264.get('event_family_rows', '')}, controls={phase264.get('control_contract_rows', '')}, full_depth_required={phase264.get('full_top_five_depth_required', '')}, levels_2_to_5_required={phase264.get('levels_2_to_5_materiality_required', '')}, l1_only_allowed={phase264.get('l1_only_candidate_allowed', '')}, profitability_claim_allowed={phase264.get('profitability_claim_allowed', '')}."
        f" Phase265 liquidity_shock_training_search_complete={phase265.get('liquidity_shock_training_search_complete', '')}, variants={phase265.get('variant_rows', '')}, full_depth_variants={phase265.get('full_top_five_depth_variant_rows', '')}, levels_2_to_5_variants={phase265.get('depth_beyond_l1_variant_rows', '')}, l1_only_variants={phase265.get('l1_only_variant_rows', '')}, cost100_positive={phase265.get('cost100_positive_variant_rows', '')}, cost200_positive={phase265.get('cost200_positive_variant_rows', '')}, survivors={phase265.get('survivor_candidate_rows', '')}, best={phase265.get('best_candidate_id', '')}, best_cost100={phase265.get('best_cost100_net_pnl_inr', '')}, best_cost200={phase265.get('best_cost200_net_pnl_inr', '')}, profitability_claim_allowed={phase265.get('profitability_claim_allowed', '')}."
        f" Phase266 interpretation_complete={phase266.get('interpretation_complete', '')}, close_phase265_for_replay={phase266.get('close_phase265_for_replay', '')}, full_depth_preserved={phase266.get('full_top_five_depth_preserved', '')}, selected_next_route={phase266.get('selected_next_route', '')}, best_cost200_avg={phase266.get('best_cost200_avg_net_per_event_inr', '')}, best_shuffle_margin={phase266.get('best_shuffle_label_margin_inr', '')}, profitability_claim_allowed={phase266.get('profitability_claim_allowed', '')}."
        f" Phase267 repair_precommit_complete={phase267.get('breadth_shuffle_repair_precommit_complete', '')}, exploratory_lane_enabled={phase267.get('exploratory_lane_enabled', '')}, exploratory_controls_are_filters={phase267.get('exploratory_controls_are_filters', '')}, acceptance_events={phase267.get('acceptance_min_event_rows', '')}, acceptance_symbols={phase267.get('acceptance_min_symbols', '')}, full_depth_required={phase267.get('full_top_five_depth_required', '')}, levels_2_to_5_required={phase267.get('levels_2_to_5_materiality_required', '')}, l1_only_allowed={phase267.get('l1_only_candidate_allowed', '')}, profitability_claim_allowed={phase267.get('profitability_claim_allowed', '')}."
        f" Phase268 two_lane_training_search_complete={phase268.get('two_lane_training_search_complete', '')}, variants={phase268.get('variant_rows', '')}, full_depth_variants={phase268.get('full_top_five_depth_variant_rows', '')}, levels_2_to_5_variants={phase268.get('depth_beyond_l1_variant_rows', '')}, l1_only_variants={phase268.get('l1_only_variant_rows', '')}, exploratory_candidates={phase268.get('exploratory_candidate_rows', '')}, annualized_research_leads={phase268.get('annualized_profitable_research_lead_rows', '')}, cost200_annualized_research_leads={phase268.get('cost200_annualized_profitable_research_lead_rows', '')}, acceptance_grade_candidates={phase268.get('acceptance_grade_candidate_rows', '')}, best={phase268.get('best_candidate_id', '')}, best_cost100_annualized={phase268.get('best_cost100_annualized_return_pct', '')}, best_cost200_annualized={phase268.get('best_cost200_annualized_return_pct', '')}, best_cost200={phase268.get('best_cost200_net_pnl_inr', '')}, profitability_claim_allowed={phase268.get('profitability_claim_allowed', '')}."
        f" Phase269 interpretation_complete={phase269.get('interpretation_complete', '')}, preserve_research_leads={phase269.get('preserve_research_leads', '')}, do_not_claim_portfolio_annual_return={phase269.get('do_not_claim_portfolio_annual_return', '')}, do_not_promote_or_replay={phase269.get('do_not_promote_or_replay_phase268', '')}, selected_next_route={phase269.get('selected_next_route', '')}, profitability_claim_allowed={phase269.get('profitability_claim_allowed', '')}."
        f" Phase270 fixed_capital_precommit_complete={phase270.get('fixed_capital_precommit_complete', '')}, capital_contract_rows={phase270.get('capital_model_contract_rows', '')}, concurrency_capacity_rows={phase270.get('concurrency_capacity_contract_rows', '')}, unlimited_capital_allowed={phase270.get('unlimited_capital_assumption_allowed', '')}, portfolio_claim_without_scheduler_allowed={phase270.get('portfolio_return_claim_without_scheduler_allowed', '')}, fixed_proxy_as_portfolio_allowed={phase270.get('fixed_notional_proxy_as_portfolio_return_allowed', '')}, profitability_claim_allowed={phase270.get('profitability_claim_allowed', '')}."
        f" Phase271 fixed_capital_analysis_complete={phase271.get('fixed_capital_analysis_complete', '')}, scopes={phase271.get('scope_rows', '')}, scenarios={phase271.get('scenario_rows', '')}, cost100_above12={phase271.get('cost100_annualized_above_12pct_scenario_rows', '')}, cost200_above12={phase271.get('cost200_annualized_above_12pct_scenario_rows', '')}, best={phase271.get('best_scenario_id', '')}, best_mechanical_annualized={phase271.get('best_mechanical_one_date_annualized_portfolio_return_pct', '')}, portfolio_claim_allowed={phase271.get('portfolio_claim_allowed', '')}, profitability_claim_allowed={phase271.get('profitability_claim_allowed', '')}."
        f" Phase272 interpretation_complete={phase272.get('interpretation_complete', '')}, priority_candidates={phase272.get('followthrough_priority_candidate_rows', '')}, pooled_above12={phase272.get('pooled_above12_scenario_rows', '')}, best_candidate={phase272.get('best_candidate_id', '')}, best={phase272.get('best_scenario_id', '')}, selected_next_route={phase272.get('selected_next_route', '')}, portfolio_claim_allowed={phase272.get('portfolio_claim_allowed', '')}, profitability_claim_allowed={phase272.get('profitability_claim_allowed', '')}."
        f" Phase273 followthrough_search_complete={phase273.get('followthrough_search_complete', '')}, scopes={phase273.get('scope_rows', '')}, order_policies={phase273.get('order_policy_rows', '')}, scenarios={phase273.get('scenario_rows', '')}, cost100_above12={phase273.get('cost100_above12_scenario_rows', '')}, cost200_above12={phase273.get('cost200_above12_scenario_rows', '')}, best={phase273.get('best_scenario_id', '')}, best_mechanical_annualized={phase273.get('best_mechanical_one_date_annualized_portfolio_return_pct', '')}, portfolio_claim_allowed={phase273.get('portfolio_claim_allowed', '')}, profitability_claim_allowed={phase273.get('profitability_claim_allowed', '')}."
        f" Phase274 interpretation_complete={phase274.get('interpretation_complete', '')}, cost200_survivor_profiles={phase274.get('cost200_survivor_scope_profile_rows', '')}, median_positive_profiles={phase274.get('median_positive_scope_profile_rows', '')}, worst_case_positive_profiles={phase274.get('worst_case_positive_scope_profile_rows', '')}, best_scope_profile={phase274.get('best_scope_profile', '')}, selected_next_route={phase274.get('selected_next_route', '')}, portfolio_claim_allowed={phase274.get('portfolio_claim_allowed', '')}, profitability_claim_allowed={phase274.get('profitability_claim_allowed', '')}."
        f" Phase275 multiday_synthetic_complete={phase275.get('multiday_synthetic_followthrough_search_complete', '')}, scenarios={phase275.get('scenario_rows', '')}, synthetic_dates={phase275.get('synthetic_date_rows', '')}, cost100_above12={phase275.get('cost100_above12_scenario_rows', '')}, cost200_above12={phase275.get('cost200_above12_scenario_rows', '')}, best={phase275.get('best_scenario_id', '')}, best_synthetic_annualized={phase275.get('best_synthetic_multiday_annualized_portfolio_return_pct', '')}, portfolio_claim_allowed={phase275.get('portfolio_claim_allowed', '')}, profitability_claim_allowed={phase275.get('profitability_claim_allowed', '')}."
        f" Phase276 interpretation_complete={phase276.get('interpretation_complete', '')}, selected_next_route={phase276.get('selected_next_route', '')}, normal_cost_sparse_positive_profiles={phase276.get('normal_cost_sparse_positive_profile_rows', '')}, cost200_failed_profiles={phase276.get('cost200_failed_profile_rows', '')}, as_is_promotion_allowed={phase276.get('as_is_promotion_allowed', '')}, portfolio_claim_allowed={phase276.get('portfolio_claim_allowed', '')}, profitability_claim_allowed={phase276.get('profitability_claim_allowed', '')}."
        f" Phase277 cost_robust_redesign_complete={phase277.get('cost_robust_redesign_search_complete', '')}, variants={phase277.get('variant_rows', '')}, scenarios={phase277.get('scenario_rows', '')}, cost200_above12={phase277.get('cost200_above12_scenario_rows', '')}, best_variant={phase277.get('best_variant_id', '')}, best_cost200_annualized={phase277.get('best_cost200_annualized_pct', '')}, profitability_claim_allowed={phase277.get('profitability_claim_allowed', '')}."
        f" Phase278 interpretation_complete={phase278.get('interpretation_complete', '')}, selected_next_route={phase278.get('selected_next_route', '')}, close_filter_redesign={phase278.get('close_filter_redesign_for_acceptance', '')}, best_preserved_clue={phase278.get('best_preserved_clue_variant', '')}, do_not_relax_cost_threshold={phase278.get('do_not_relax_cost_threshold', '')}, profitability_claim_allowed={phase278.get('profitability_claim_allowed', '')}."
        f" Phase279 target_construction_precommit_complete={phase279.get('target_construction_precommit_complete', '')}, target_families={phase279.get('target_family_rows', '')}, allowed_target_families={phase279.get('phase280_allowed_target_family_rows', '')}, preserved_clues={phase279.get('preserved_clue_rows', '')}, cost200_required={phase279.get('cost200_required', '')}, full_depth_required={phase279.get('full_depth_required', '')}, l1_only_allowed={phase279.get('l1_only_allowed', '')}, profitability_claim_allowed={phase279.get('profitability_claim_allowed', '')}."
        f" Phase280 material_target_search_complete={phase280.get('material_new_target_construction_search_complete', '')}, target_families={phase280.get('target_family_rows', '')}, variants={phase280.get('variant_rows', '')}, scenarios={phase280.get('scenario_rows', '')}, cost200_above12={phase280.get('cost200_above12_scenario_rows', '')}, best_variant={phase280.get('best_variant_id', '')}, best_family={phase280.get('best_target_family', '')}, best_cost200_annualized={phase280.get('best_cost200_annualized_pct', '')}, l1_only_variants={phase280.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase280.get('net_edge_live_mask_rows', '')}, profitability_claim_allowed={phase280.get('profitability_claim_allowed', '')}."
        f" Phase281 interpretation_complete={phase281.get('interpretation_complete', '')}, selected_next_route={phase281.get('selected_next_route', '')}, close_phase280={phase281.get('close_phase280_for_acceptance', '')}, material_clues={phase281.get('material_clue_variant_rows', '')}, near_misses={phase281.get('near_miss_variant_rows', '')}, best_preserved_clue={phase281.get('best_preserved_clue_variant', '')}, do_not_claim_portfolio_return={phase281.get('do_not_claim_portfolio_return', '')}, profitability_claim_allowed={phase281.get('profitability_claim_allowed', '')}."
        f" Phase282 ensemble_precommit_complete={phase282.get('regime_conditioned_ensemble_precommit_complete', '')}, search_seeds={phase282.get('phase283_search_seed_rows', '')}, ensembles={phase282.get('ensemble_family_rows', '')}, allowed_ensembles={phase282.get('phase283_allowed_ensemble_rows', '')}, regime_buckets={phase282.get('regime_bucket_rows', '')}, event_floor={phase282.get('min_event_floor_diagnostic', '')}, robust_portfolio_floor={phase282.get('min_events_for_robust_portfolio_claim', '')}, cost200_required={phase282.get('cost200_required', '')}, fixed_capital_required={phase282.get('fixed_capital_required', '')}, full_depth_required={phase282.get('full_depth_required', '')}, l1_only_allowed={phase282.get('l1_only_allowed', '')}, net_edge_live_mask_allowed={phase282.get('net_edge_live_mask_allowed', '')}, profitability_claim_allowed={phase282.get('profitability_claim_allowed', '')}."
        f" Phase283 ensemble_search_complete={phase283.get('regime_conditioned_ensemble_search_complete', '')}, seeds={phase283.get('seed_rows', '')}, variants={phase283.get('variant_rows', '')}, scenarios={phase283.get('scenario_rows', '')}, sparse_above12={phase283.get('sparse_above12_scenario_rows', '')}, robust_floor_rows={phase283.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase283.get('best_variant_id', '')}, best_family={phase283.get('best_ensemble_family', '')}, best_bucket={phase283.get('best_bucket_id', '')}, best_cost200_annualized={phase283.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase283.get('best_scheduled_event_rows', '')}, l1_only_variants={phase283.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase283.get('net_edge_live_mask_rows', '')}, profitability_claim_allowed={phase283.get('profitability_claim_allowed', '')}."
        f" Phase284 interpretation_complete={phase284.get('interpretation_complete', '')}, selected_next_route={phase284.get('selected_next_route', '')}, close_phase283={phase284.get('close_phase283_for_acceptance', '')}, positive_full_depth_clues={phase284.get('positive_full_depth_clue_variant_rows', '')}, near_misses={phase284.get('near_miss_variant_rows', '')}, best_preserved_clue={phase284.get('best_preserved_clue_variant', '')}, best_cost200_annualized={phase284.get('phase283_best_cost200_annualized_pct', '')}, best_scheduled_events={phase284.get('phase283_best_scheduled_event_rows', '')}, do_not_claim_portfolio_return={phase284.get('do_not_claim_portfolio_return', '')}, profitability_claim_allowed={phase284.get('profitability_claim_allowed', '')}."
        f" Phase285 lifecycle_precommit_complete={phase285.get('lifecycle_redesign_precommit_complete', '')}, seeds={phase285.get('phase286_lifecycle_seed_rows', '')}, event_universe_rows={phase285.get('event_universe_rows', '')}, lifecycle_families={phase285.get('lifecycle_family_rows', '')}, entry_exit_grid={phase285.get('entry_exit_grid_rows', '')}, same_symbol_rejections={phase285.get('phase283_rejected_same_symbol_overlap_rows', '')}, max_concurrent_rejections={phase285.get('phase283_rejected_max_concurrent_rows', '')}, cost200_required={phase285.get('cost200_required', '')}, full_depth_required={phase285.get('full_depth_required', '')}, profitability_claim_allowed={phase285.get('profitability_claim_allowed', '')}."
        f" Phase286 lifecycle_search_complete={phase286.get('lifecycle_redesign_search_complete', '')}, variants={phase286.get('variant_rows', '')}, scenarios={phase286.get('scenario_rows', '')}, sparse_above12={phase286.get('sparse_above12_scenario_rows', '')}, robust_floor={phase286.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase286.get('best_variant_id', '')}, best_family={phase286.get('best_lifecycle_family', '')}, best_grid={phase286.get('best_grid_id', '')}, best_cost200_annualized={phase286.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase286.get('best_scheduled_event_rows', '')}, profitability_claim_allowed={phase286.get('profitability_claim_allowed', '')}."
        f" Phase287 interpretation_complete={phase287.get('interpretation_complete', '')}, selected_next_route={phase287.get('selected_next_route', '')}, close_phase286={phase287.get('close_phase286_for_acceptance', '')}, positive_full_depth_clues={phase287.get('positive_full_depth_clue_variant_rows', '')}, best_phase286_variant={phase287.get('best_phase286_variant_id', '')}, best_family={phase287.get('best_lifecycle_family', '')}, best_cost200_annualized={phase287.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase287.get('best_scheduled_event_rows', '')}, fixed_capital_denominator_required={phase287.get('do_not_relax_annualized_denominator', '')}, profitability_claim_allowed={phase287.get('profitability_claim_allowed', '')}."
        f" Phase288 liquidity_pressure_search_complete={phase288.get('liquidity_pressure_search_complete', '')}, variants={phase288.get('variant_rows', '')}, scenarios={phase288.get('scenario_rows', '')}, sparse_above12={phase288.get('sparse_above12_scenario_rows', '')}, robust_floor={phase288.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase288.get('best_variant_id', '')}, best_family={phase288.get('best_liquidity_family', '')}, best_pressure={phase288.get('best_pressure_column', '')}, best_side={phase288.get('best_side_mode', '')}, best_cost200_annualized={phase288.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase288.get('best_scheduled_event_rows', '')}, profitability_claim_allowed={phase288.get('profitability_claim_allowed', '')}."
        f" Phase289 interpretation_complete={phase289.get('interpretation_complete', '')}, selected_next_route={phase289.get('selected_next_route', '')}, close_phase288={phase289.get('close_phase288_for_acceptance', '')}, positive_full_depth_clues={phase289.get('positive_full_depth_clue_variant_rows', '')}, best_phase288_variant={phase289.get('best_phase288_variant_id', '')}, best_family={phase289.get('best_liquidity_family', '')}, best_pressure={phase289.get('best_pressure_column', '')}, best_cost200_annualized={phase289.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase289.get('best_scheduled_event_rows', '')}, fixed_capital_denominator_required={phase289.get('do_not_relax_annualized_denominator', '')}, profitability_claim_allowed={phase289.get('profitability_claim_allowed', '')}."
        f" Phase290 adaptive_pressure_search_complete={phase290.get('adaptive_liquidity_pressure_search_complete', '')}, variants={phase290.get('variant_rows', '')}, scenarios={phase290.get('scenario_rows', '')}, sparse_above12={phase290.get('sparse_above12_scenario_rows', '')}, robust_floor={phase290.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase290.get('best_variant_id', '')}, best_family={phase290.get('best_adaptive_family', '')}, best_primary={phase290.get('best_primary_pressure_column', '')}, best_interaction={phase290.get('best_interaction_column', '')}, best_side={phase290.get('best_side_mode', '')}, best_bucket={phase290.get('best_market_bucket', '')}, best_cost200_annualized={phase290.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase290.get('best_scheduled_event_rows', '')}, profitability_claim_allowed={phase290.get('profitability_claim_allowed', '')}."
        f" Phase291 interpretation_complete={phase291.get('interpretation_complete', '')}, selected_next_route={phase291.get('selected_next_route', '')}, close_phase290={phase291.get('close_phase290_for_acceptance', '')}, above12_too_sparse={phase291.get('above12_but_too_sparse_variant_rows', '')}, best_phase290_variant={phase291.get('best_phase290_variant_id', '')}, best_family={phase291.get('best_adaptive_family', '')}, best_primary={phase291.get('best_primary_pressure_column', '')}, best_interaction={phase291.get('best_interaction_column', '')}, best_cost200_annualized={phase291.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase291.get('best_scheduled_event_rows', '')}, profitability_claim_allowed={phase291.get('profitability_claim_allowed', '')}."
        f" Phase292 breadth_repair_search_complete={phase292.get('breadth_repair_search_complete', '')}, variants={phase292.get('variant_rows', '')}, scenarios={phase292.get('scenario_rows', '')}, sparse_above12={phase292.get('sparse_above12_scenario_rows', '')}, robust_floor={phase292.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase292.get('best_variant_id', '')}, best_family={phase292.get('best_repair_family', '')}, best_side={phase292.get('best_side_mode', '')}, best_bucket={phase292.get('best_market_bucket', '')}, best_cost200_annualized={phase292.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase292.get('best_scheduled_event_rows', '')}, l1_only_variants={phase292.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase292.get('net_edge_live_mask_rows', '')}, profitability_claim_allowed={phase292.get('profitability_claim_allowed', '')}."
        f" Phase293 interpretation_complete={phase293.get('interpretation_complete', '')}, selected_next_route={phase293.get('selected_next_route', '')}, close_phase292={phase293.get('close_phase292_for_acceptance', '')}, close_same_contrarian_repair={phase293.get('close_same_contrarian_repair_family', '')}, positive_below12={phase293.get('positive_but_below12_variant_rows', '')}, best_phase292_variant={phase293.get('best_phase292_variant_id', '')}, best_family={phase293.get('best_repair_family', '')}, best_side={phase293.get('best_side_mode', '')}, best_bucket={phase293.get('best_market_bucket', '')}, best_cost200_annualized={phase293.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase293.get('best_scheduled_event_rows', '')}, do_not_lower_cost_or_event_floor={phase293.get('do_not_lower_cost_or_event_floor', '')}, profitability_claim_allowed={phase293.get('profitability_claim_allowed', '')}."
        f" Phase294 continuation_search_complete={phase294.get('continuation_search_complete', '')}, families={phase294.get('family_rows', '')}, variants={phase294.get('variant_rows', '')}, scenarios={phase294.get('scenario_rows', '')}, sparse_above12={phase294.get('sparse_above12_scenario_rows', '')}, robust_floor={phase294.get('robust_portfolio_floor_scenario_rows', '')}, robust_above12={phase294.get('robust_portfolio_above12_scenario_rows', '')}, discovery_survivors={phase294.get('discovery_survivor_variant_rows', '')}, robust_survivors={phase294.get('robust_survivor_variant_rows', '')}, best_variant={phase294.get('best_variant_id', '')}, best_family={phase294.get('best_continuation_family', '')}, best_side={phase294.get('best_side_mode', '')}, best_bucket={phase294.get('best_market_bucket', '')}, best_cost200_annualized={phase294.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase294.get('best_scheduled_event_rows', '')}, l1_only_variants={phase294.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase294.get('net_edge_live_mask_rows', '')}, profitability_claim_allowed={phase294.get('profitability_claim_allowed', '')}."
        f" Phase295 interpretation_complete={phase295.get('interpretation_complete', '')}, selected_next_route={phase295.get('selected_next_route', '')}, close_phase294={phase295.get('close_phase294_for_acceptance', '')}, close_phase277_minor_repairs={phase295.get('close_phase277_event_universe_for_minor_repairs', '')}, positive_below12={phase295.get('positive_but_below12_variant_rows', '')}, best_phase294_variant={phase295.get('best_phase294_variant_id', '')}, best_family={phase295.get('best_continuation_family', '')}, best_cost200_annualized={phase295.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase295.get('best_scheduled_event_rows', '')}, do_not_lower_cost_or_event_floor={phase295.get('do_not_lower_cost_or_event_floor', '')}, profitability_claim_allowed={phase295.get('profitability_claim_allowed', '')}."
        f" Phase296 full_year_sweep_complete={phase296.get('full_year_sweep_complete', '')}, input_rows={phase296.get('input_rows', '')}, dates={phase296.get('input_trade_dates', '')}, symbols={phase296.get('input_symbols', '')}, feed_profiles={phase296.get('input_feed_profiles', '')}, variants={phase296.get('variant_rows', '')}, scenarios={phase296.get('scenario_rows', '')}, sparse_above12={phase296.get('sparse_above12_scenario_rows', '')}, robust_floor={phase296.get('robust_portfolio_floor_scenario_rows', '')}, robust_above12={phase296.get('robust_portfolio_above12_scenario_rows', '')}, best_variant={phase296.get('best_variant_id', '')}, best_family={phase296.get('best_strategy_family', '')}, best_feed={phase296.get('best_feed_profile', '')}, best_cost200_annualized={phase296.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase296.get('best_scheduled_event_rows', '')}, annualized_denominator={phase296.get('annualized_denominator', '')}, profitability_claim_allowed={phase296.get('profitability_claim_allowed', '')}."
        f" Phase297 interpretation_complete={phase297.get('interpretation_complete', '')}, selected_next_route={phase297.get('selected_next_route', '')}, close_phase296={phase297.get('close_phase296_for_acceptance', '')}, close_phase42_proxy={phase297.get('close_phase42_proxy_sweep_for_direct_acceptance', '')}, raw_book_state_clues={phase297.get('raw_book_state_clue_variant_rows', '')}, best_phase296_variant={phase297.get('best_phase296_variant_id', '')}, best_family={phase297.get('best_strategy_family', '')}, best_feed={phase297.get('best_feed_profile', '')}, best_cost200_annualized={phase297.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase297.get('best_scheduled_event_rows', '')}, do_not_claim_portfolio_return={phase297.get('do_not_claim_portfolio_return', '')}, profitability_claim_allowed={phase297.get('profitability_claim_allowed', '')}."
        f" Phase298 raw_dense_sweep_complete={phase298.get('raw_dense_sweep_complete', '')}, symbols={phase298.get('symbol_rows', '')}, months={phase298.get('trade_month_rows', '')}, files={phase298.get('source_file_rows', '')}, stride={phase298.get('sample_stride', '')}, sampled_rows={phase298.get('sampled_dense_rows', '')}, shard_date_rows={phase298.get('shard_trade_date_rows', '')}, raw_events={phase298.get('raw_event_rows', '')}, variants={phase298.get('variant_rows', '')}, scenarios={phase298.get('scenario_rows', '')}, sparse_above12={phase298.get('sparse_above12_scenario_rows', '')}, robust_above12={phase298.get('robust_portfolio_above12_scenario_rows', '')}, best_variant={phase298.get('best_variant_id', '')}, best_family={phase298.get('best_strategy_family', '')}, best_cost200_annualized={phase298.get('best_cost200_annualized_pct', '')}, best_events={phase298.get('best_scheduled_event_rows', '')}, best_dates={phase298.get('best_observed_trade_dates', '')}, annualized_denominator={phase298.get('annualized_denominator', '')}, profitability_claim_allowed={phase298.get('profitability_claim_allowed', '')}."
        f" Phase299 interpretation_complete={phase299.get('interpretation_complete', '')}, selected_next_route={phase299.get('selected_next_route', '')}, close_phase298={phase299.get('close_phase298_for_direct_acceptance', '')}, above12_below_30={phase299.get('above12_below_30_event_variant_rows', '')}, directional_signal_seeds={phase299.get('directional_signal_seed_rows', '')}, best_phase298_variant={phase299.get('best_phase298_variant_id', '')}, best_family={phase299.get('best_strategy_family', '')}, best_cost200_annualized={phase299.get('best_cost200_annualized_pct', '')}, best_events={phase299.get('best_scheduled_event_rows', '')}, passive_fill_model_required={phase299.get('require_passive_fill_model', '')}, adverse_selection_required={phase299.get('require_adverse_selection_penalty', '')}, forced_flatten_required={phase299.get('require_forced_flatten_cost', '')}, profitability_claim_allowed={phase299.get('profitability_claim_allowed', '')}."
        f" Phase300 precommit_complete={phase300.get('precommit_complete', '')}, execution_complete={phase300.get('execution_complete', '')}, selected_route={phase300.get('selected_route', '')}, charter_rows={phase300.get('charter_rows', '')}, inputs={phase300.get('input_registry_rows', '')}, work_order={phase300.get('execution_work_order_rows', '')}, directional_signal_seeds={phase300.get('directional_signal_seed_rows', '')}, seed_variants={phase300.get('seed_variant_rows', '')}, seed_events={phase300.get('seed_event_rows', '')}, scenarios={phase300.get('scenario_rows', '')}, fill_models={phase300.get('fill_model_rows', '')}, execution_policies={phase300.get('execution_policy_rows', '')}, raw_depth_schema_columns={phase300.get('raw_depth_schema_columns_present', '')}, l1_only={phase300.get('l1_only_variant_rows', '')}, live_masks={phase300.get('net_edge_live_mask_rows', '')}, fill_model_required={phase300.get('fill_model_required', '')}, adverse_selection_required={phase300.get('adverse_selection_required', '')}, forced_flatten_required={phase300.get('forced_flatten_cost_required', '')}, cost200_required={phase300.get('cost200_required', '')}, fixed_capital_required={phase300.get('fixed_capital_required', '')}, above12={phase300.get('above12_scenario_rows', '')}, event_floor={phase300.get('event_floor_scenario_rows', '')}, breadth={phase300.get('breadth_met_scenario_rows', '')}, survivors={phase300.get('cost200_acceptance_survivor_rows', '')}, best_scenario={phase300.get('best_scenario_id', '')}, best_annualized={phase300.get('best_annualized_pct', '')}, best_events={phase300.get('best_scheduled_event_rows', '')}, kill_switch={phase300.get('kill_switch_triggered', '')}, profitability_claim_allowed={phase300.get('profitability_claim_allowed', '')}."
        f" Phase301 interpretation_complete={phase301.get('interpretation_complete', '')}, selected_outcome={phase301.get('selected_outcome', '')}, phase300_scenarios={phase301.get('phase300_scenario_rows', '')}, above12={phase301.get('phase300_above12_scenario_rows', '')}, event_floor={phase301.get('phase300_event_floor_scenario_rows', '')}, breadth={phase301.get('phase300_breadth_met_scenario_rows', '')}, survivors={phase301.get('phase300_cost200_acceptance_survivor_rows', '')}, kill_switch={phase301.get('phase300_kill_switch_triggered', '')}, best_annualized={phase301.get('best_annualized_pct', '')}, best_events={phase301.get('best_scheduled_event_rows', '')}, broadest_annualized={phase301.get('broadest_annualized_pct', '')}, broadest_events={phase301.get('broadest_scheduled_event_rows', '')}, terminal_report_required={phase301.get('terminal_report_required', '')}, do_not_rescue={phase301.get('do_not_rescue_with_more_filters', '')}, profitability_claim_allowed={phase301.get('profitability_claim_allowed', '')}."
        f" Phase302 terminal_report_complete={phase302.get('terminal_report_complete', '')}, selected_verdict={phase302.get('selected_verdict', '')}, closed_scope={phase302.get('closed_scope', '')}, phase300_scenarios={phase302.get('phase300_scenario_rows', '')}, above12={phase302.get('phase300_above12_scenario_rows', '')}, event_floor={phase302.get('phase300_event_floor_scenario_rows', '')}, breadth={phase302.get('phase300_breadth_met_scenario_rows', '')}, survivors={phase302.get('phase300_cost200_acceptance_survivor_rows', '')}, best_sparse_annualized={phase302.get('best_sparse_annualized_pct', '')}, best_sparse_events={phase302.get('best_sparse_scheduled_event_rows', '')}, broadest_annualized={phase302.get('broadest_annualized_pct', '')}, broadest_events={phase302.get('broadest_scheduled_event_rows', '')}, byproducts={phase302.get('byproduct_rows', '')}, material_new_required={phase302.get('material_new_source_or_thesis_required', '')}, do_not_continue_same_route={phase302.get('do_not_continue_same_route', '')}, profitability_claim_allowed={phase302.get('profitability_claim_allowed', '')}."
    )
    branches = [
        {
            "branch": "real_l2_anchor_gate",
            "status": "gated",
            "evidence": "Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven.",
            "current_next_action": "use_phase174_secure_download_orchestrator_for_required_real_l2_dates",
        },
        {
            "branch": "real_receive_flow_source",
            "status": real_receive_status,
            "evidence": real_receive_evidence,
            "current_next_action": real_receive_next,
        },
        {
            "branch": "top_five_depth_passive",
            "status": "closed_clean_falsification",
            "evidence": "Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification.",
            "current_next_action": "do_not_open_phase134_or_phase135_for_this_branch",
        },
        {
            "branch": "synthetic_strategy_discovery",
            "status": phase337.get("state") or phase336.get("state") or phase335.get("state") or phase334.get("state") or phase333.get("state") or phase332.get("state") or phase331.get("state") or phase330.get("state") or phase329.get("state") or phase328.get("state") or phase327.get("state") or phase326.get("state") or phase325.get("state") or phase324.get("state") or phase323.get("state") or phase322.get("state") or phase321.get("state") or phase320.get("state") or phase319.get("state") or phase318.get("state") or phase317.get("state") or phase316.get("state") or phase315.get("state") or phase314.get("state") or phase313.get("state") or phase312.get("state") or phase311.get("state") or phase310.get("state") or phase309.get("state") or phase308.get("state") or phase307.get("state") or phase306.get("state") or phase305.get("state") or phase304.get("state") or phase303.get("state") or phase302.get("state") or phase301.get("state") or phase300.get("state") or phase299.get("state") or phase298.get("state") or phase297.get("state") or phase296.get("state") or phase295.get("state") or phase294.get("state") or phase293.get("state") or phase292.get("state") or phase291.get("state") or phase290.get("state") or phase289.get("state") or phase288.get("state") or phase287.get("state") or phase286.get("state") or phase285.get("state") or phase284.get("state") or phase283.get("state") or phase282.get("state") or phase281.get("state") or phase280.get("state") or phase279.get("state") or phase278.get("state") or phase277.get("state") or phase276.get("state") or phase275.get("state") or phase274.get("state") or phase273.get("state") or phase272.get("state") or phase271.get("state") or phase270.get("state") or phase269.get("state") or phase268.get("state") or phase267.get("state") or phase266.get("state") or phase265.get("state") or phase264.get("state") or phase263.get("state") or phase262.get("state") or phase261.get("state") or phase260.get("state") or phase259.get("state") or phase258.get("state") or phase257.get("state") or phase256.get("state") or phase255.get("state") or phase254.get("state") or phase253.get("state") or phase252.get("state") or phase251.get("state") or phase250.get("state") or phase249.get("state") or phase248.get("state") or phase247.get("state") or phase246.get("state") or phase245.get("state") or phase244.get("state") or phase243.get("state") or phase242.get("state") or phase241.get("state") or phase240.get("state") or phase239.get("state") or phase238.get("state") or phase237.get("state") or phase236.get("state") or phase235.get("state") or phase234.get("state") or phase233.get("state") or phase232.get("state") or phase231.get("state") or phase230.get("state") or phase229.get("state") or "not_started",
            "evidence": (
                f"Phase229 ranked {phase229.get('distinct_strategy_ids', '')} strategy ids and found "
                f"{phase229.get('positive_realistic_candidate_rows', '')} positive realistic candidates; "
                f"Phase230 tested {phase230.get('variant_group_rows', '')} original/inverse/oracle variant groups and found "
                f"{phase230.get('positive_expanded_group_rows', '')} positive expanded groups and "
                f"{phase230.get('positive_oracle_signed_group_rows', '')} positive oracle-signed upper-bound groups; "
                f"Phase231 replayed {phase231.get('candidate_rows', '')} material-new candidates and found "
                f"{phase231.get('synthetic_candidate_rows', '')} train+test synthetic candidates, led by "
                f"{phase231.get('best_candidate_id', '')} with test net P&L {phase231.get('best_test_net_pnl_inr', '')}; "
                f"Phase232 validated {phase232.get('validated_synthetic_candidate_rows', '')} candidate after cost stress, side-flip, random-side and holdout stability checks; "
                f"Phase233 passed fragility/realism with {phase233.get('neighbor_pass_rows', '')} passing neighbors and parent test 2x cost net P&L {phase233.get('parent_test_2x_cost_net_pnl_inr', '')}; "
                f"Phase234 selected {phase234.get('selected_route_id', '')} with real_anchor_route_ready={phase234.get('real_anchor_route_ready', '')} and {phase234.get('required_schema_present_rows', '')}/{phase234.get('required_schema_rows', '')} required real L2 schema rows present; "
                f"Phase235 real-anchor replay selected {phase235.get('real_anchor_trade_rows', '')} trades with net P&L {phase235.get('real_anchor_net_pnl_inr', '')}, but breadth was {phase235.get('real_anchor_dates', '')} dates and {phase235.get('real_anchor_symbols', '')} symbols; "
                f"Phase236 replayed {phase236.get('neighbor_variant_rows', '')} neighbors and found {phase236.get('positive_real_anchor_variant_rows', '')} positive real-anchor variants, but {phase236.get('breadth_passing_variant_rows', '')} breadth-passing variants; "
                f"Phase237 evaluated {phase237.get('expanded_variant_rows', '')} threshold-transfer variants and opened {phase237.get('best_candidate_id', '')} for Phase238 with net P&L {phase237.get('best_real_anchor_net_pnl_inr', '')}, {phase237.get('best_real_anchor_trade_rows', '')} trades, {phase237.get('best_real_anchor_dates', '')} dates and {phase237.get('best_real_anchor_symbols', '')} symbols; "
                f"Phase238 froze {phase238.get('candidate_id', '')} and found {phase238.get('local_unseen_validation_dates_available', '')} local unseen validation dates available; "
                f"Phase239 found Azure Files target unseen dates reachable with azure_ready={phase239.get('azure_storage_listing_ready', '')}, while local unseen dates remain {phase239.get('local_unseen_candidate_dates', '')}; "
                f"Phase240 started/resumed raw unseen L2 download with completed_files={phase240.get('completed_files', '')}, failed_files={phase240.get('failed_files', '')}, completed_dates={phase240.get('completed_dates', '')}; "
                f"Phase241 replayed the frozen candidate on one unseen date with trades={phase241.get('trade_rows', '')}, net P&L={phase241.get('net_pnl_inr', '')}, controls={phase241.get('control_pass_rows', '')}/{phase241.get('control_rows', '')}, survived={phase241.get('one_date_diagnostic_candidate_survived', '')}; "
                f"Phase242 closed {phase242.get('closed_candidate_id', '')} and opened {phase242.get('redesign_queue_rows', '')} redesign rows without more downloads or holdout tuning; "
                f"Phase243 found {phase243.get('survivor_candidate_rows', '')} cost-stress/random-side survivors, led by {phase243.get('best_candidate_id', '')}, with 2x-cost net {phase243.get('best_cost200_net_pnl_inr', '')} and random beat {phase243.get('best_random_beat_fraction', '')}; "
                f"Phase244 froze {phase244.get('candidate_id', '')} for future holdout with storage_decision_required={phase244.get('storage_decision_required', '')}, download_now_allowed={phase244.get('download_more_dates_now_allowed', '')}; "
                f"Phase245 found local space feasible by estimate with free_gb={phase245.get('free_gb_now', '')}, projected_required_gb={phase245.get('projected_required_gb', '')}, but still blocks downloads until policy choice; "
                f"Phase246 downloaded and replayed one fresh unseen date {phase246.get('trade_date', '')}, producing trades={phase246.get('trade_rows', '')}, net P&L={phase246.get('net_pnl_inr', '')}, controls={phase246.get('control_pass_rows', '')}/{phase246.get('control_rows', '')}, survived={phase246.get('one_date_diagnostic_candidate_survived', '')}; "
                f"Phase247 precommitted {phase247.get('redesign_candidate_rows', '')} L2-imbalance/regime-filter redesign families with holdout tuning dates {phase247.get('forbidden_tuning_dates', '')} excluded; "
                f"Phase248 evaluated {phase248.get('variant_rows', '')} combined-filter variants and found {phase248.get('survivor_candidate_rows', '')} controlled survivors, with {phase248.get('cost200_positive_variant_rows', '')} positive at 2x cost; "
                f"Phase249 closed {phase249.get('closed_scope', '')} and selected {phase249.get('selected_next_route', '')} as the next materially different route; "
                f"Phase250 precommitted pair/basket relative-value search with grouped_symbols={phase250.get('grouped_symbols', '')}, candidate_families={phase250.get('candidate_family_rows', '')}, no_download={phase250.get('download_more_dates_now_allowed', '')}, replay_now={phase250.get('replay_execution_allowed_now', '')}, profitability_claim_allowed={phase250.get('profitability_claim_allowed', '')}; "
                f"Phase251 executed {phase251.get('variant_rows', '')} pair/basket variants with full_top_five_depth_variants={phase251.get('full_top_five_depth_variant_rows', '')} and depth_beyond_l1_variants={phase251.get('depth_beyond_l1_variant_rows', '')}, finding base_positive={phase251.get('net_positive_variant_rows', '')}, cost200_positive={phase251.get('cost200_positive_variant_rows', '')} and survivors={phase251.get('survivor_candidate_rows', '')}; "
                f"Phase252 closed {phase252.get('closed_scope', '')} and selected {phase252.get('selected_next_route', '')} after confirming raw_depth_schema={phase252.get('raw_depth_schema_present_rows', '')}/{phase252.get('raw_depth_schema_rows', '')}; "
                f"Phase253 precommitted richer raw top-five depth materialization with usable_raw_roots={phase253.get('usable_raw_root_rows', '')}, schema={phase253.get('schema_present_rows', '')}/{phase253.get('schema_rows', '')}, feature_catalog_rows={phase253.get('feature_catalog_rows', '')} and phase254_allowed={phase253.get('phase254_materialization_allowed_next', '')}; "
                f"Phase254 materialized {phase254.get('event_bar_rows', '')} richer raw-depth event bars from {phase254.get('source_tick_rows', '')} source ticks across {phase254.get('symbols', '')} symbols, excluding {phase254.get('excluded_invalid_source_tick_rows', '')} invalid raw ticks before aggregation; "
                f"Phase255 audited {phase255.get('feature_rows', '')} features, including {phase255.get('full_depth_feature_rows', '')} full-depth features, found healthy_full_depth={phase255.get('healthy_full_depth_feature_rows', '')}, max_abs_full_depth_ic={phase255.get('max_abs_full_depth_spearman_ic', '')}, and opened strategy_search_allowed_next={phase255.get('strategy_search_allowed_next', '')}; "
                f"Phase256 searched {phase256.get('variant_rows', '')} full-depth cost-aware variants, found cost100_positive={phase256.get('cost100_positive_variant_rows', '')}, cost200_positive={phase256.get('cost200_positive_variant_rows', '')}, survivors={phase256.get('survivor_candidate_rows', '')}, with best_cost100={phase256.get('best_cost100_net_pnl_inr', '')} and best_cost200={phase256.get('best_cost200_net_pnl_inr', '')}; "
                f"Phase257 closed_taker_threshold={phase257.get('closed_taker_threshold_route', '')}, preserved_full_depth={phase257.get('full_top_five_depth_preserved', '')}, selected_next_route={phase257.get('selected_next_route', '')}, next_route_contract_rows={phase257.get('next_route_contract_rows', '')}; "
                f"Phase258 precommitted {phase258.get('selected_route', '')} with families={phase258.get('candidate_family_rows', '')}, controls={phase258.get('control_contract_rows', '')}, full_depth_required={phase258.get('full_top_five_depth_required', '')}, l1_only_allowed={phase258.get('l1_only_candidate_allowed', '')}; "
                f"Phase259 searched {phase259.get('variant_rows', '')} passive full-depth variants, found cost100_positive={phase259.get('cost100_positive_variant_rows', '')}, cost200_positive={phase259.get('cost200_positive_variant_rows', '')}, survivors={phase259.get('survivor_candidate_rows', '')}, best_cost100={phase259.get('best_cost100_expected_net_pnl_inr', '')}, best_cost200={phase259.get('best_cost200_expected_net_pnl_inr', '')}; "
                f"Phase260 closed Phase259 for promotion={phase260.get('close_phase259_for_promotion', '')}, kept full_passive_route_closed={phase260.get('full_passive_route_closed', '')}, and selected {phase260.get('selected_next_route', '')} with contract_rows={phase260.get('next_route_contract_rows', '')}; "
                f"Phase261 precommitted {phase261.get('selected_route', '')} with fill_grid={phase261.get('fill_probability_grid_rows', '')}, families={phase261.get('candidate_family_rows', '')}, full_depth_required={phase261.get('full_top_five_depth_required', '')}, levels_2_to_5_required={phase261.get('levels_2_to_5_materiality_required', '')}, l1_only_allowed={phase261.get('l1_only_candidate_allowed', '')}; "
                f"Phase262 searched {phase262.get('variant_rows', '')} passive full-depth/fill-model variants, found cost100_positive={phase262.get('cost100_positive_variant_rows', '')}, cost200_positive={phase262.get('cost200_positive_variant_rows', '')}, survivors={phase262.get('survivor_candidate_rows', '')}, best_cost100={phase262.get('best_cost100_expected_net_pnl_inr', '')}, best_cost200={phase262.get('best_cost200_expected_net_pnl_inr', '')}; "
                f"Phase263 closed_passive_route={phase263.get('close_passive_spread_capture_fill_model_route', '')}, preserved_full_depth={phase263.get('full_top_five_depth_preserved', '')}, and selected {phase263.get('selected_next_route', '')} with contract_rows={phase263.get('next_route_contract_rows', '')}; "
                f"Phase264 precommitted {phase264.get('selected_route', '')} with features={phase264.get('feature_catalog_rows', '')}, families={phase264.get('event_family_rows', '')}, labels={phase264.get('label_contract_rows', '')}, controls={phase264.get('control_contract_rows', '')}, full_depth_required={phase264.get('full_top_five_depth_required', '')}, levels_2_to_5_required={phase264.get('levels_2_to_5_materiality_required', '')}, l1_only_allowed={phase264.get('l1_only_candidate_allowed', '')}; "
                f"Phase265 searched {phase265.get('variant_rows', '')} full-depth liquidity-shock variants, full_depth_variants={phase265.get('full_top_five_depth_variant_rows', '')}, levels_2_to_5_variants={phase265.get('depth_beyond_l1_variant_rows', '')}, l1_only_variants={phase265.get('l1_only_variant_rows', '')}, cost100_positive={phase265.get('cost100_positive_variant_rows', '')}, cost150_positive={phase265.get('cost150_positive_variant_rows', '')}, cost200_positive={phase265.get('cost200_positive_variant_rows', '')}, survivors={phase265.get('survivor_candidate_rows', '')}, best={phase265.get('best_candidate_id', '')}, best_cost100={phase265.get('best_cost100_net_pnl_inr', '')}, best_cost200={phase265.get('best_cost200_net_pnl_inr', '')}; "
                f"Phase266 interpreted Phase265 with close_phase265_for_replay={phase266.get('close_phase265_for_replay', '')}, recognized_unaccepted_2x_pocket={phase266.get('recognize_promising_but_unaccepted_2x_pocket', '')}, full_depth_preserved={phase266.get('full_top_five_depth_preserved', '')}, threshold_relaxation_only_allowed={phase266.get('threshold_relaxation_only_allowed', '')}, selected_next_route={phase266.get('selected_next_route', '')}, best_cost200_avg={phase266.get('best_cost200_avg_net_per_event_inr', '')}, best_shuffle_margin={phase266.get('best_shuffle_label_margin_inr', '')}; "
                f"Phase267 precommitted a two-lane repair with exploratory_lane_enabled={phase267.get('exploratory_lane_enabled', '')}, exploratory_controls_are_filters={phase267.get('exploratory_controls_are_filters', '')}, acceptance_events={phase267.get('acceptance_min_event_rows', '')}, acceptance_symbols={phase267.get('acceptance_min_symbols', '')}, full_depth_required={phase267.get('full_top_five_depth_required', '')}, levels_2_to_5_required={phase267.get('levels_2_to_5_materiality_required', '')}, l1_only_allowed={phase267.get('l1_only_candidate_allowed', '')}; "
                f"Phase268 searched {phase268.get('variant_rows', '')} two-lane full-depth variants, found exploratory_candidates={phase268.get('exploratory_candidate_rows', '')}, annualized_research_leads={phase268.get('annualized_profitable_research_lead_rows', '')}, cost200_annualized_research_leads={phase268.get('cost200_annualized_profitable_research_lead_rows', '')}, acceptance_grade_candidates={phase268.get('acceptance_grade_candidate_rows', '')}, cost100_positive={phase268.get('cost100_positive_variant_rows', '')}, cost200_positive={phase268.get('cost200_positive_variant_rows', '')}, best={phase268.get('best_candidate_id', '')}, best_cost100_annualized={phase268.get('best_cost100_annualized_return_pct', '')}, best_cost200_annualized={phase268.get('best_cost200_annualized_return_pct', '')}, best_shuffle_margin={phase268.get('best_shuffle_label_margin_inr', '')}; "
                f"Phase269 ranked {phase269.get('phase268_annualized_profitable_research_lead_rows', '')} fixed-notional annualized research leads, preserved_research_leads={phase269.get('preserve_research_leads', '')}, portfolio_return_claim_allowed={0 if phase269.get('do_not_claim_portfolio_annual_return', '') == 1 else ''}, selected_next_route={phase269.get('selected_next_route', '')}; "
                f"Phase270 precommitted capital/concurrency/capacity return modeling with capital_contract_rows={phase270.get('capital_model_contract_rows', '')}, concurrency_capacity_rows={phase270.get('concurrency_capacity_contract_rows', '')}, unlimited_capital_allowed={phase270.get('unlimited_capital_assumption_allowed', '')}, fixed_proxy_as_portfolio_allowed={phase270.get('fixed_notional_proxy_as_portfolio_return_allowed', '')}; "
                f"Phase271 scheduled pooled and per-candidate fixed-capital scenarios with scopes={phase271.get('scope_rows', '')}, scenarios={phase271.get('scenario_rows', '')}, cost100_above12={phase271.get('cost100_annualized_above_12pct_scenario_rows', '')}, cost200_above12={phase271.get('cost200_annualized_above_12pct_scenario_rows', '')}, best={phase271.get('best_scenario_id', '')}, best_mechanical_annualized={phase271.get('best_mechanical_one_date_annualized_portfolio_return_pct', '')}, portfolio_claim_allowed={phase271.get('portfolio_claim_allowed', '')}; "
                f"Phase272 interpreted those pockets with priority_candidates={phase272.get('followthrough_priority_candidate_rows', '')}, pooled_above12={phase272.get('pooled_above12_scenario_rows', '')}, best_candidate={phase272.get('best_candidate_id', '')}, selected_next_route={phase272.get('selected_next_route', '')}; "
                f"Phase273 follow-through searched scopes={phase273.get('scope_rows', '')}, order_policies={phase273.get('order_policy_rows', '')}, scenarios={phase273.get('scenario_rows', '')}, cost100_above12={phase273.get('cost100_above12_scenario_rows', '')}, cost200_above12={phase273.get('cost200_above12_scenario_rows', '')}, best={phase273.get('best_scenario_id', '')}, best_mechanical_annualized={phase273.get('best_mechanical_one_date_annualized_portfolio_return_pct', '')}; "
                f"Phase274 interpreted Phase273 with cost200_survivor_profiles={phase274.get('cost200_survivor_scope_profile_rows', '')}, median_positive_profiles={phase274.get('median_positive_scope_profile_rows', '')}, worst_case_positive_profiles={phase274.get('worst_case_positive_scope_profile_rows', '')}, selected_next_route={phase274.get('selected_next_route', '')}; "
                f"Phase275 executed multiday synthetic follow-through with scenarios={phase275.get('scenario_rows', '')}, synthetic_dates={phase275.get('synthetic_date_rows', '')}, cost100_above12={phase275.get('cost100_above12_scenario_rows', '')}, cost200_above12={phase275.get('cost200_above12_scenario_rows', '')}, best={phase275.get('best_scenario_id', '')}, best_synthetic_annualized={phase275.get('best_synthetic_multiday_annualized_portfolio_return_pct', '')}; "
                f"Phase276 interpreted Phase275 as fragile with normal_cost_sparse_positive_profiles={phase276.get('normal_cost_sparse_positive_profile_rows', '')}, cost200_failed_profiles={phase276.get('cost200_failed_profile_rows', '')}, selected_next_route={phase276.get('selected_next_route', '')}; "
                f"Phase277 searched cost-robust full-depth redesign variants={phase277.get('variant_rows', '')}, scenarios={phase277.get('scenario_rows', '')}, cost200_above12={phase277.get('cost200_above12_scenario_rows', '')}, best_variant={phase277.get('best_variant_id', '')}, best_cost200_annualized={phase277.get('best_cost200_annualized_pct', '')}; "
                f"Phase278 interpreted Phase277 with close_filter_redesign={phase278.get('close_filter_redesign_for_acceptance', '')}, best_preserved_clue={phase278.get('best_preserved_clue_variant', '')}, selected_next_route={phase278.get('selected_next_route', '')}; "
                f"Phase279 precommitted target families={phase279.get('target_family_rows', '')}, allowed_for_phase280={phase279.get('phase280_allowed_target_family_rows', '')}, preserved_clues={phase279.get('preserved_clue_rows', '')}, cost200_required={phase279.get('cost200_required', '')}, full_depth_required={phase279.get('full_depth_required', '')}, l1_only_allowed={phase279.get('l1_only_allowed', '')}; "
                f"Phase280 searched material target-construction variants={phase280.get('variant_rows', '')}, scenarios={phase280.get('scenario_rows', '')}, cost200_above12={phase280.get('cost200_above12_scenario_rows', '')}, best_variant={phase280.get('best_variant_id', '')}, best_family={phase280.get('best_target_family', '')}, best_cost200_annualized={phase280.get('best_cost200_annualized_pct', '')}, l1_only_variants={phase280.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase280.get('net_edge_live_mask_rows', '')}; "
                f"Phase281 interpreted Phase280 with close_phase280={phase281.get('close_phase280_for_acceptance', '')}, material_clues={phase281.get('material_clue_variant_rows', '')}, near_misses={phase281.get('near_miss_variant_rows', '')}, best_preserved_clue={phase281.get('best_preserved_clue_variant', '')}, selected_next_route={phase281.get('selected_next_route', '')}, do_not_claim_portfolio_return={phase281.get('do_not_claim_portfolio_return', '')}; "
                f"Phase282 precommitted regime-conditioned full-depth ensemble search with seeds={phase282.get('phase283_search_seed_rows', '')}, ensembles={phase282.get('ensemble_family_rows', '')}, allowed_ensembles={phase282.get('phase283_allowed_ensemble_rows', '')}, regime_buckets={phase282.get('regime_bucket_rows', '')}, event_floor={phase282.get('min_event_floor_diagnostic', '')}, robust_portfolio_floor={phase282.get('min_events_for_robust_portfolio_claim', '')}, cost200_required={phase282.get('cost200_required', '')}, fixed_capital_required={phase282.get('fixed_capital_required', '')}, full_depth_required={phase282.get('full_depth_required', '')}, l1_only_allowed={phase282.get('l1_only_allowed', '')}, net_edge_live_mask_allowed={phase282.get('net_edge_live_mask_allowed', '')}; "
                f"Phase283 searched regime-conditioned full-depth ensembles with variants={phase283.get('variant_rows', '')}, scenarios={phase283.get('scenario_rows', '')}, sparse_above12={phase283.get('sparse_above12_scenario_rows', '')}, robust_floor_rows={phase283.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase283.get('best_variant_id', '')}, best_family={phase283.get('best_ensemble_family', '')}, best_bucket={phase283.get('best_bucket_id', '')}, best_cost200_annualized={phase283.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase283.get('best_scheduled_event_rows', '')}, l1_only_variants={phase283.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase283.get('net_edge_live_mask_rows', '')}; "
                f"Phase284 closed Phase283 for acceptance={phase284.get('close_phase283_for_acceptance', '')}, selected {phase284.get('selected_next_route', '')}, preserved best_clue={phase284.get('best_preserved_clue_variant', '')}, kept do_not_relax_cost_threshold={phase284.get('do_not_relax_cost_threshold', '')}, do_not_claim_portfolio_return={phase284.get('do_not_claim_portfolio_return', '')}, profitability_claim_allowed={phase284.get('profitability_claim_allowed', '')}; "
                f"Phase285 precommitted lifecycle/side/exit redesign with seeds={phase285.get('phase286_lifecycle_seed_rows', '')}, lifecycle_families={phase285.get('lifecycle_family_rows', '')}, entry_exit_grid={phase285.get('entry_exit_grid_rows', '')}, event_universe_rows={phase285.get('event_universe_rows', '')}, same_symbol_rejections={phase285.get('phase283_rejected_same_symbol_overlap_rows', '')}, max_concurrent_rejections={phase285.get('phase283_rejected_max_concurrent_rows', '')}, full_depth_required={phase285.get('full_depth_required', '')}, l1_only_allowed={phase285.get('l1_only_allowed', '')}, net_edge_live_mask_allowed={phase285.get('net_edge_live_mask_allowed', '')}; "
                f"Phase286 executed lifecycle search variants={phase286.get('variant_rows', '')}, scenarios={phase286.get('scenario_rows', '')}, sparse_above12={phase286.get('sparse_above12_scenario_rows', '')}, robust_floor={phase286.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase286.get('best_variant_id', '')}, best_family={phase286.get('best_lifecycle_family', '')}, best_grid={phase286.get('best_grid_id', '')}, best_cost200_annualized={phase286.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase286.get('best_scheduled_event_rows', '')}, l1_only_variants={phase286.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase286.get('net_edge_live_mask_rows', '')}; "
                f"Phase287 closed Phase286 for acceptance={phase287.get('close_phase286_for_acceptance', '')}, selected {phase287.get('selected_next_route', '')}, positive_full_depth_clues={phase287.get('positive_full_depth_clue_variant_rows', '')}, fixed_capital_denominator_required={phase287.get('do_not_relax_annualized_denominator', '')}, do_not_claim_portfolio_return={phase287.get('do_not_claim_portfolio_return', '')}, profitability_claim_allowed={phase287.get('profitability_claim_allowed', '')}; "
                f"Phase288 searched direct full-depth L2 liquidity-pressure variants={phase288.get('variant_rows', '')}, scenarios={phase288.get('scenario_rows', '')}, sparse_above12={phase288.get('sparse_above12_scenario_rows', '')}, robust_floor={phase288.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase288.get('best_variant_id', '')}, best_family={phase288.get('best_liquidity_family', '')}, best_pressure={phase288.get('best_pressure_column', '')}, best_side={phase288.get('best_side_mode', '')}, best_cost200_annualized={phase288.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase288.get('best_scheduled_event_rows', '')}, l1_only_variants={phase288.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase288.get('net_edge_live_mask_rows', '')}; "
                f"Phase289 closed Phase288 for acceptance={phase289.get('close_phase288_for_acceptance', '')}, selected {phase289.get('selected_next_route', '')}, positive_full_depth_clues={phase289.get('positive_full_depth_clue_variant_rows', '')}, fixed_capital_denominator_required={phase289.get('do_not_relax_annualized_denominator', '')}, do_not_claim_portfolio_return={phase289.get('do_not_claim_portfolio_return', '')}, profitability_claim_allowed={phase289.get('profitability_claim_allowed', '')}; "
                f"Phase290 searched adaptive pressure variants={phase290.get('variant_rows', '')}, scenarios={phase290.get('scenario_rows', '')}, sparse_above12={phase290.get('sparse_above12_scenario_rows', '')}, robust_floor={phase290.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase290.get('best_variant_id', '')}, best_family={phase290.get('best_adaptive_family', '')}, best_primary={phase290.get('best_primary_pressure_column', '')}, best_interaction={phase290.get('best_interaction_column', '')}, best_side={phase290.get('best_side_mode', '')}, best_bucket={phase290.get('best_market_bucket', '')}, best_cost200_annualized={phase290.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase290.get('best_scheduled_event_rows', '')}, l1_only_variants={phase290.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase290.get('net_edge_live_mask_rows', '')}; "
                f"Phase291 closed Phase290 for acceptance={phase291.get('close_phase290_for_acceptance', '')}, selected {phase291.get('selected_next_route', '')}, above12_but_too_sparse={phase291.get('above12_but_too_sparse_variant_rows', '')}, fixed_capital_denominator_required={phase291.get('do_not_relax_annualized_denominator', '')}, do_not_claim_portfolio_return={phase291.get('do_not_claim_portfolio_return', '')}, profitability_claim_allowed={phase291.get('profitability_claim_allowed', '')}; "
                f"Phase292 breadth repair searched variants={phase292.get('variant_rows', '')}, scenarios={phase292.get('scenario_rows', '')}, sparse_above12={phase292.get('sparse_above12_scenario_rows', '')}, robust_floor={phase292.get('robust_portfolio_floor_scenario_rows', '')}, best_variant={phase292.get('best_variant_id', '')}, best_family={phase292.get('best_repair_family', '')}, best_side={phase292.get('best_side_mode', '')}, best_bucket={phase292.get('best_market_bucket', '')}, best_cost200_annualized={phase292.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase292.get('best_scheduled_event_rows', '')}, l1_only_variants={phase292.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase292.get('net_edge_live_mask_rows', '')}; "
                f"Phase293 closed Phase292 for acceptance={phase293.get('close_phase292_for_acceptance', '')}, closed_same_contrarian_repair={phase293.get('close_same_contrarian_repair_family', '')}, selected {phase293.get('selected_next_route', '')}, positive_below12={phase293.get('positive_but_below12_variant_rows', '')}, best_phase292_variant={phase293.get('best_phase292_variant_id', '')}, best_family={phase293.get('best_repair_family', '')}, best_cost200_annualized={phase293.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase293.get('best_scheduled_event_rows', '')}, do_not_relax_annualized_denominator={phase293.get('do_not_relax_annualized_denominator', '')}, do_not_lower_cost_or_event_floor={phase293.get('do_not_lower_cost_or_event_floor', '')}, profitability_claim_allowed={phase293.get('profitability_claim_allowed', '')}; "
                f"Phase294 searched full-depth pressure/absorption continuation families={phase294.get('family_rows', '')}, variants={phase294.get('variant_rows', '')}, scenarios={phase294.get('scenario_rows', '')}, sparse_above12={phase294.get('sparse_above12_scenario_rows', '')}, robust_floor={phase294.get('robust_portfolio_floor_scenario_rows', '')}, robust_above12={phase294.get('robust_portfolio_above12_scenario_rows', '')}, discovery_survivors={phase294.get('discovery_survivor_variant_rows', '')}, robust_survivors={phase294.get('robust_survivor_variant_rows', '')}, best_variant={phase294.get('best_variant_id', '')}, best_family={phase294.get('best_continuation_family', '')}, best_cost200_annualized={phase294.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase294.get('best_scheduled_event_rows', '')}, l1_only_variants={phase294.get('l1_only_variant_rows', '')}, net_edge_live_masks={phase294.get('net_edge_live_mask_rows', '')}; "
                f"Phase295 closed Phase294 for acceptance={phase295.get('close_phase294_for_acceptance', '')}, closed_phase277_minor_repairs={phase295.get('close_phase277_event_universe_for_minor_repairs', '')}, selected {phase295.get('selected_next_route', '')}, positive_below12={phase295.get('positive_but_below12_variant_rows', '')}, best_phase294_variant={phase295.get('best_phase294_variant_id', '')}, best_family={phase295.get('best_continuation_family', '')}, best_cost200_annualized={phase295.get('best_cost200_annualized_pct', '')}, best_scheduled_events={phase295.get('best_scheduled_event_rows', '')}, do_not_relax_annualized_denominator={phase295.get('do_not_relax_annualized_denominator', '')}, do_not_lower_cost_or_event_floor={phase295.get('do_not_lower_cost_or_event_floor', '')}, profitability_claim_allowed={phase295.get('profitability_claim_allowed', '')}; "
                f"Phase326 precommitted expanded event-catalyst top-five depth join rows={phase326.get('event_symbol_work_order_rows', '')}, events={phase326.get('generated_event_rows', '')}, join_contract_rows={phase326.get('join_contract_rows', '')}, full_depth_required={phase326.get('full_depth_required', '')}, depth_beyond_l1_required={phase326.get('depth_beyond_l1_required', '')}, strategy_search_allowed_now={phase326.get('strategy_search_allowed_now', '')}, profitability_claim_allowed={phase326.get('profitability_claim_allowed', '')}; "
                f"Phase327 materialized expanded top-five depth rows={phase327.get('materialized_join_rows', '')}, events={phase327.get('materialized_events', '')}, symbols={phase327.get('materialized_symbols', '')}, full_depth_columns_present={phase327.get('full_depth_columns_present', '')}, depth_beyond_l1_required={phase327.get('depth_beyond_l1_required', '')}, strategy_search_allowed_now={phase327.get('strategy_search_allowed_now', '')}, profitability_claim_allowed={phase327.get('profitability_claim_allowed', '')}; "
                f"Phase328 audited expanded join quality rows={phase328.get('joined_rows', '')}, events={phase328.get('event_rows', '')}, symbols={phase328.get('symbol_rows', '')}, min_event_symbol_coverage={phase328.get('min_event_symbol_coverage', '')}, crossed_l1={phase328.get('crossed_or_locked_l1_rows', '')}, depth_material_rows={phase328.get('depth_beyond_l1_material_rows', '')}, strategy_search_allowed_now={phase328.get('strategy_search_allowed_now', '')}, profitability_claim_allowed={phase328.get('profitability_claim_allowed', '')}; "
                f"Phase329 precommitted expanded feature materialization with feature_catalog_rows={phase329.get('feature_catalog_rows', '')}, depth_beyond_l1_feature_rows={phase329.get('depth_beyond_l1_feature_rows', '')}, target_only_rows={phase329.get('lookahead_target_only_rows', '')}, expected_feature_rows={phase329.get('expected_feature_rows', '')}, strategy_search_allowed_now={phase329.get('strategy_search_allowed_now', '')}, profitability_claim_allowed={phase329.get('profitability_claim_allowed', '')}; "
                f"Phase330 materialized expanded feature matrix with rows={phase330.get('feature_matrix_rows', '')}, events={phase330.get('event_rows', '')}, symbols={phase330.get('symbol_rows', '')}, source_tick_rows={phase330.get('source_tick_rows', '')}, live_features={phase330.get('live_feature_columns', '')}, depth_features={phase330.get('depth_feature_columns', '')}, targets={phase330.get('target_columns', '')}, live_target_cols={phase330.get('target_columns_used_as_live_features', '')}, strategy_search_allowed_now={phase330.get('strategy_search_allowed_now', '')}, profitability_claim_allowed={phase330.get('profitability_claim_allowed', '')}; "
                f"Phase331 precommitted expanded strategy search with families={phase331.get('strategy_family_rows', '')}, depth_families={phase331.get('depth_beyond_l1_family_rows', '')}, grid_rows={phase331.get('search_grid_rows', '')}, variant_upper_bound={phase331.get('expanded_variant_upper_bound_rows', '')}, cost200_rows={phase331.get('cost200_grid_rows', '')}, passive_aware_rows={phase331.get('passive_aware_grid_rows', '')}, event_bucket_policies={phase331.get('event_bucket_policy_rows', '')}, fixed_capital_required={phase331.get('fixed_capital_required', '')}, passive_realism_required={phase331.get('passive_realism_penalties_required', '')}, profitability_claim_allowed={phase331.get('profitability_claim_allowed', '')}; "
                f"Phase332 executed expanded training-only search with scenarios={phase332.get('scenario_rows', '')}, cost200_scenarios={phase332.get('cost200_scenario_rows', '')}, passive_aware_scenarios={phase332.get('passive_aware_scenario_rows', '')}, above12={phase332.get('above12_annualized_scenario_rows', '')}, cost200_above12={phase332.get('cost200_above12_scenario_rows', '')}, cost200_acceptance_grade={phase332.get('cost200_acceptance_grade_candidate_rows', '')}, best={phase332.get('best_scenario_id', '')}, best_annualized={phase332.get('best_annualized_return_pct', '')}, best_cost200_annualized={phase332.get('best_cost200_annualized_return_pct', '')}, profitability_claim_allowed={phase332.get('profitability_claim_allowed', '')}; "
                f"Phase333 interpreted Phase332 with base_or_slippage_pockets={phase333.get('base_or_slippage_profitable_research_pockets_exist', '')}, cost200_bar_passed={phase333.get('cost200_profitability_bar_passed', '')}, cost200_acceptance={phase333.get('cost200_acceptance_grade_candidates_exist', '')}, near_miss_preserved={phase333.get('best_cost200_near_miss_preserved', '')}, preserved_family={phase333.get('preserved_family_for_redesign', '')}, passive_rescue={phase333.get('passive_aware_rescue_status', '')}, selected_next_route={phase333.get('selected_next_route', '')}, profitability_claim_allowed={phase333.get('profitability_claim_allowed', '')}; "
                f"Phase334 precommitted cost-stress margin redesign with lanes={phase334.get('design_lane_rows', '')}, contract_rows={phase334.get('search_contract_rows', '')}, work_order_rows={phase334.get('phase335_work_order_rows', '')}, preserved_family={phase334.get('preserved_family', '')}, prior_best_cost200={phase334.get('best_cost200_prior_annualized_return_pct', '')}, full_depth_required={phase334.get('full_depth_required', '')}, levels_2_to_5_required={phase334.get('levels_2_to_5_required', '')}, l1_only_allowed={phase334.get('l1_only_allowed', '')}, net_edge_live_mask_allowed={phase334.get('net_edge_live_mask_allowed', '')}, training_search_allowed_next={phase334.get('strategy_search_execution_allowed_next', '')}, profitability_claim_allowed={phase334.get('profitability_claim_allowed', '')}; "
                f"Phase335 executed cost-stress margin training-only redesign with scenarios={phase335.get('scenario_rows', '')}, lanes={phase335.get('design_lane_rows', '')}, cost200_scenarios={phase335.get('cost200_scenario_rows', '')}, passive_aware_scenarios={phase335.get('passive_aware_scenario_rows', '')}, above12={phase335.get('above12_annualized_scenario_rows', '')}, cost200_above12={phase335.get('cost200_above12_scenario_rows', '')}, cost200_acceptance_grade={phase335.get('cost200_acceptance_grade_candidate_rows', '')}, best_cost200={phase335.get('best_cost200_scenario_id', '')}, best_cost200_annualized={phase335.get('best_cost200_annualized_return_pct', '')}, best_acceptance_grade={phase335.get('best_acceptance_grade_cost200_scenario_id', '')}, best_acceptance_grade_annualized={phase335.get('best_acceptance_grade_cost200_annualized_return_pct', '')}, profitability_claim_allowed={phase335.get('profitability_claim_allowed', '')}; "
                f"Phase336 interpreted Phase335 with cost200_training_pockets={phase336.get('cost200_profitable_training_pockets_exist', '')}, acceptance_candidates={phase336.get('cost200_acceptance_grade_training_candidates_exist', '')}, candidate_rows={phase336.get('candidate_rows_preserved', '')}, best_candidate={phase336.get('best_acceptance_grade_candidate', '')}, best_annualized={phase336.get('best_acceptance_grade_annualized_return_pct', '')}, selected_next_route={phase336.get('selected_next_route', '')}, profitability_claim_allowed={phase336.get('profitability_claim_allowed', '')}; "
                f"Phase337 froze {phase337.get('candidate_rows_frozen', '')} candidates for holdout, reconciled_attached_passive_aware_charter={phase337.get('attached_passive_aware_charter_reconciled', '')}, best_frozen={phase337.get('best_frozen_candidate', '')}, best_frozen_annualized={phase337.get('best_frozen_annualized_return_pct', '')}, passive_fill_required={phase337.get('passive_fill_model_required', '')}, adverse_selection_required={phase337.get('adverse_selection_penalty_required', '')}, forced_flatten_required={phase337.get('forced_flatten_cost_required', '')}, maker_rebate_allowed={phase337.get('maker_rebate_allowed', '')}, phase338_allowed={phase337.get('phase338_execution_allowed_next', '')}, profitability_claim_allowed={phase337.get('profitability_claim_allowed', '')}."
            ),
            "current_next_action": phase337.get("next_action") or phase336.get("next_action") or phase335.get("next_action") or phase334.get("next_action") or phase333.get("next_action") or phase332.get("next_action") or phase331.get("next_action") or phase330.get("next_action") or phase329.get("next_action") or phase328.get("next_action") or phase327.get("next_action") or phase326.get("next_action") or phase325.get("next_action") or phase324.get("next_action") or phase323.get("next_action") or phase322.get("next_action") or phase321.get("next_action") or phase320.get("next_action") or phase319.get("next_action") or phase318.get("next_action") or phase317.get("next_action") or phase316.get("next_action") or phase315.get("next_action") or phase314.get("next_action") or phase313.get("next_action") or phase312.get("next_action") or phase311.get("next_action") or phase310.get("next_action") or phase309.get("next_action") or phase308.get("next_action") or phase307.get("next_action") or phase306.get("next_action") or phase305.get("next_action") or phase304.get("next_action") or phase303.get("next_action") or phase302.get("next_action") or phase301.get("next_action") or phase300.get("next_action") or phase299.get("next_action") or phase298.get("next_action") or phase297.get("next_action") or phase296.get("next_action") or phase295.get("next_action") or phase294.get("next_action") or phase293.get("next_action") or phase292.get("next_action") or phase291.get("next_action") or phase290.get("next_action") or phase289.get("next_action") or phase288.get("next_action") or phase287.get("next_action") or phase286.get("next_action") or phase285.get("next_action") or phase284.get("next_action") or phase283.get("next_action") or phase282.get("next_action") or phase281.get("next_action") or phase280.get("next_action") or phase279.get("next_action") or phase278.get("next_action") or phase277.get("next_action") or phase276.get("next_action") or phase275.get("next_action") or phase274.get("next_action") or phase273.get("next_action") or phase272.get("next_action") or phase271.get("next_action") or phase270.get("next_action") or phase269.get("next_action") or phase268.get("next_action") or phase267.get("next_action") or phase266.get("next_action") or phase265.get("next_action") or phase264.get("next_action") or phase263.get("next_action") or phase262.get("next_action") or phase261.get("next_action") or phase260.get("next_action") or phase259.get("next_action") or phase258.get("next_action") or phase257.get("next_action") or phase256.get("next_action") or phase255.get("next_action") or phase254.get("next_action") or phase253.get("next_action") or phase252.get("next_action") or phase251.get("next_action") or phase250.get("next_action") or phase249.get("next_action") or phase248.get("next_action") or phase247.get("next_action") or phase246.get("next_action") or phase245.get("next_action") or phase244.get("next_action") or phase243.get("next_action") or phase242.get("next_action") or phase241.get("next_action") or phase240.get("next_action") or phase239.get("next_action") or phase238.get("next_action") or phase237.get("next_action") or phase235.get("next_action") or phase234.get("next_action") or phase233.get("next_action") or phase232.get("next_action") or phase231.get("next_action") or phase230.get("next_action") or phase229.get("next_action") or "run_phase229_or_phase230_strategy_discovery",
        },
        {
            "branch": "dense_synthetic_replay",
            "status": "not_promoted",
            "evidence": "Partial/smoke dense replay artifacts remain non-promotional and do not override replay gates.",
            "current_next_action": "only_continue_if_precommitted_and_not_blocklisted",
        },
    ]
    return pd.DataFrame(branches)


def build_global_gates(phase_ledger: pd.DataFrame) -> pd.DataFrame:
    phase136 = phase_ledger[phase_ledger["phase"].astype(int).eq(136)] if not phase_ledger.empty else pd.DataFrame()
    phase148 = phase_ledger[phase_ledger["phase"].astype(int).eq(148)] if not phase_ledger.empty else pd.DataFrame()
    phase172 = phase_ledger[phase_ledger["phase"].astype(int).eq(172)] if not phase_ledger.empty else pd.DataFrame()
    phase174 = phase_ledger[phase_ledger["phase"].astype(int).eq(174)] if not phase_ledger.empty else pd.DataFrame()
    phase175 = phase_ledger[phase_ledger["phase"].astype(int).eq(175)] if not phase_ledger.empty else pd.DataFrame()
    phase176 = phase_ledger[phase_ledger["phase"].astype(int).eq(176)] if not phase_ledger.empty else pd.DataFrame()
    phase177 = phase_ledger[phase_ledger["phase"].astype(int).eq(177)] if not phase_ledger.empty else pd.DataFrame()
    phase178 = phase_ledger[phase_ledger["phase"].astype(int).eq(178)] if not phase_ledger.empty else pd.DataFrame()
    phase179 = phase_ledger[phase_ledger["phase"].astype(int).eq(179)] if not phase_ledger.empty else pd.DataFrame()
    phase180 = phase_ledger[phase_ledger["phase"].astype(int).eq(180)] if not phase_ledger.empty else pd.DataFrame()
    phase181 = phase_ledger[phase_ledger["phase"].astype(int).eq(181)] if not phase_ledger.empty else pd.DataFrame()
    phase182 = phase_ledger[phase_ledger["phase"].astype(int).eq(182)] if not phase_ledger.empty else pd.DataFrame()
    phase183 = phase_ledger[phase_ledger["phase"].astype(int).eq(183)] if not phase_ledger.empty else pd.DataFrame()
    phase184 = phase_ledger[phase_ledger["phase"].astype(int).eq(184)] if not phase_ledger.empty else pd.DataFrame()
    phase185 = phase_ledger[phase_ledger["phase"].astype(int).eq(185)] if not phase_ledger.empty else pd.DataFrame()
    phase186 = phase_ledger[phase_ledger["phase"].astype(int).eq(186)] if not phase_ledger.empty else pd.DataFrame()
    phase187 = phase_ledger[phase_ledger["phase"].astype(int).eq(187)] if not phase_ledger.empty else pd.DataFrame()
    phase188 = phase_ledger[phase_ledger["phase"].astype(int).eq(188)] if not phase_ledger.empty else pd.DataFrame()
    phase189 = phase_ledger[phase_ledger["phase"].astype(int).eq(189)] if not phase_ledger.empty else pd.DataFrame()
    phase190 = phase_ledger[phase_ledger["phase"].astype(int).eq(190)] if not phase_ledger.empty else pd.DataFrame()
    phase191 = phase_ledger[phase_ledger["phase"].astype(int).eq(191)] if not phase_ledger.empty else pd.DataFrame()
    phase192 = phase_ledger[phase_ledger["phase"].astype(int).eq(192)] if not phase_ledger.empty else pd.DataFrame()
    phase193 = phase_ledger[phase_ledger["phase"].astype(int).eq(193)] if not phase_ledger.empty else pd.DataFrame()
    phase194 = phase_ledger[phase_ledger["phase"].astype(int).eq(194)] if not phase_ledger.empty else pd.DataFrame()
    phase195 = phase_ledger[phase_ledger["phase"].astype(int).eq(195)] if not phase_ledger.empty else pd.DataFrame()
    phase196 = phase_ledger[phase_ledger["phase"].astype(int).eq(196)] if not phase_ledger.empty else pd.DataFrame()
    phase197 = phase_ledger[phase_ledger["phase"].astype(int).eq(197)] if not phase_ledger.empty else pd.DataFrame()
    phase198 = phase_ledger[phase_ledger["phase"].astype(int).eq(198)] if not phase_ledger.empty else pd.DataFrame()
    phase199 = phase_ledger[phase_ledger["phase"].astype(int).eq(199)] if not phase_ledger.empty else pd.DataFrame()
    phase200 = phase_ledger[phase_ledger["phase"].astype(int).eq(200)] if not phase_ledger.empty else pd.DataFrame()
    phase201 = phase_ledger[phase_ledger["phase"].astype(int).eq(201)] if not phase_ledger.empty else pd.DataFrame()
    phase202 = phase_ledger[phase_ledger["phase"].astype(int).eq(202)] if not phase_ledger.empty else pd.DataFrame()
    phase203 = phase_ledger[phase_ledger["phase"].astype(int).eq(203)] if not phase_ledger.empty else pd.DataFrame()
    phase204 = phase_ledger[phase_ledger["phase"].astype(int).eq(204)] if not phase_ledger.empty else pd.DataFrame()
    phase205 = phase_ledger[phase_ledger["phase"].astype(int).eq(205)] if not phase_ledger.empty else pd.DataFrame()
    phase206 = phase_ledger[phase_ledger["phase"].astype(int).eq(206)] if not phase_ledger.empty else pd.DataFrame()
    phase207 = phase_ledger[phase_ledger["phase"].astype(int).eq(207)] if not phase_ledger.empty else pd.DataFrame()
    phase208 = phase_ledger[phase_ledger["phase"].astype(int).eq(208)] if not phase_ledger.empty else pd.DataFrame()
    phase209 = phase_ledger[phase_ledger["phase"].astype(int).eq(209)] if not phase_ledger.empty else pd.DataFrame()
    phase210 = phase_ledger[phase_ledger["phase"].astype(int).eq(210)] if not phase_ledger.empty else pd.DataFrame()
    phase211 = phase_ledger[phase_ledger["phase"].astype(int).eq(211)] if not phase_ledger.empty else pd.DataFrame()
    phase212 = phase_ledger[phase_ledger["phase"].astype(int).eq(212)] if not phase_ledger.empty else pd.DataFrame()
    phase213 = phase_ledger[phase_ledger["phase"].astype(int).eq(213)] if not phase_ledger.empty else pd.DataFrame()
    phase214 = phase_ledger[phase_ledger["phase"].astype(int).eq(214)] if not phase_ledger.empty else pd.DataFrame()
    phase215 = phase_ledger[phase_ledger["phase"].astype(int).eq(215)] if not phase_ledger.empty else pd.DataFrame()
    phase216 = phase_ledger[phase_ledger["phase"].astype(int).eq(216)] if not phase_ledger.empty else pd.DataFrame()
    phase217 = phase_ledger[phase_ledger["phase"].astype(int).eq(217)] if not phase_ledger.empty else pd.DataFrame()
    phase218 = phase_ledger[phase_ledger["phase"].astype(int).eq(218)] if not phase_ledger.empty else pd.DataFrame()
    phase219 = phase_ledger[phase_ledger["phase"].astype(int).eq(219)] if not phase_ledger.empty else pd.DataFrame()
    phase220 = phase_ledger[phase_ledger["phase"].astype(int).eq(220)] if not phase_ledger.empty else pd.DataFrame()
    phase221 = phase_ledger[phase_ledger["phase"].astype(int).eq(221)] if not phase_ledger.empty else pd.DataFrame()
    phase222 = phase_ledger[phase_ledger["phase"].astype(int).eq(222)] if not phase_ledger.empty else pd.DataFrame()
    phase223 = phase_ledger[phase_ledger["phase"].astype(int).eq(223)] if not phase_ledger.empty else pd.DataFrame()
    phase224 = phase_ledger[phase_ledger["phase"].astype(int).eq(224)] if not phase_ledger.empty else pd.DataFrame()
    phase225 = phase_ledger[phase_ledger["phase"].astype(int).eq(225)] if not phase_ledger.empty else pd.DataFrame()
    phase226 = phase_ledger[phase_ledger["phase"].astype(int).eq(226)] if not phase_ledger.empty else pd.DataFrame()
    phase227 = phase_ledger[phase_ledger["phase"].astype(int).eq(227)] if not phase_ledger.empty else pd.DataFrame()
    phase228 = phase_ledger[phase_ledger["phase"].astype(int).eq(228)] if not phase_ledger.empty else pd.DataFrame()
    phase206_metrics = phase_status_from_metrics(206)
    real_replay_allowed = int(phase148["strategy_replay_allowed"].iloc[0]) if not phase148.empty and str(phase148["strategy_replay_allowed"].iloc[0]) != "" else 0
    receive_replay_allowed = int(phase172["strategy_replay_allowed"].iloc[0]) if not phase172.empty and str(phase172["strategy_replay_allowed"].iloc[0]) != "" else 0
    secure_replay_allowed = int(phase174["strategy_replay_allowed"].iloc[0]) if not phase174.empty and str(phase174["strategy_replay_allowed"].iloc[0]) != "" else 0
    schema_replay_allowed = int(phase175["strategy_replay_allowed"].iloc[0]) if not phase175.empty and str(phase175["strategy_replay_allowed"].iloc[0]) != "" else 0
    materializer_replay_allowed = int(phase176["strategy_replay_allowed"].iloc[0]) if not phase176.empty and str(phase176["strategy_replay_allowed"].iloc[0]) != "" else 0
    quality_replay_allowed = int(phase177["strategy_replay_allowed"].iloc[0]) if not phase177.empty and str(phase177["strategy_replay_allowed"].iloc[0]) != "" else 0
    handoff_replay_allowed = int(phase178["strategy_replay_allowed"].iloc[0]) if not phase178.empty and str(phase178["strategy_replay_allowed"].iloc[0]) != "" else 0
    precommit_replay_allowed = int(phase179["strategy_replay_allowed"].iloc[0]) if not phase179.empty and str(phase179["strategy_replay_allowed"].iloc[0]) != "" else 0
    cost_label_replay_allowed = int(phase180["strategy_replay_allowed"].iloc[0]) if not phase180.empty and str(phase180["strategy_replay_allowed"].iloc[0]) != "" else 0
    label_materialization_replay_allowed = int(phase181["strategy_replay_allowed"].iloc[0]) if not phase181.empty and str(phase181["strategy_replay_allowed"].iloc[0]) != "" else 0
    label_audit_replay_allowed = int(phase182["strategy_replay_allowed"].iloc[0]) if not phase182.empty and str(phase182["strategy_replay_allowed"].iloc[0]) != "" else 0
    replay_readiness_replay_allowed = int(phase183["strategy_replay_allowed"].iloc[0]) if not phase183.empty and str(phase183["strategy_replay_allowed"].iloc[0]) != "" else 0
    replay_readiness_pnl_allowed = int(phase183["pnl_allowed"].iloc[0]) if not phase183.empty and str(phase183["pnl_allowed"].iloc[0]) != "" else 0
    dry_run_test_rows_used = int(phase184["test_rows_used"].iloc[0]) if not phase184.empty and str(phase184["test_rows_used"].iloc[0]) != "" else 0
    dry_run_promotion_allowed = int(phase184["promotion_allowed"].iloc[0]) if not phase184.empty and str(phase184["promotion_allowed"].iloc[0]) != "" else 0
    dry_run_paper_live_allowed = int(phase184["paper_or_live_acceptance_allowed"].iloc[0]) if not phase184.empty and str(phase184["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    interpretation_test_rows_used = int(phase185["test_rows_used"].iloc[0]) if not phase185.empty and str(phase185["test_rows_used"].iloc[0]) != "" else 0
    interpretation_test_replay_allowed = int(phase185["test_replay_allowed_next"].iloc[0]) if not phase185.empty and str(phase185["test_replay_allowed_next"].iloc[0]) != "" else 0
    interpretation_promotion_allowed = int(phase185["promotion_allowed"].iloc[0]) if not phase185.empty and str(phase185["promotion_allowed"].iloc[0]) != "" else 0
    interpretation_paper_live_allowed = int(phase185["paper_or_live_acceptance_allowed"].iloc[0]) if not phase185.empty and str(phase185["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    closure_reuse_allowed = int(phase186["reuse_without_redesign_allowed"].iloc[0]) if not phase186.empty and str(phase186["reuse_without_redesign_allowed"].iloc[0]) != "" else 0
    closure_test_replay_allowed = int(phase186["test_replay_allowed_next"].iloc[0]) if not phase186.empty and str(phase186["test_replay_allowed_next"].iloc[0]) != "" else 0
    closure_promotion_allowed = int(phase186["promotion_allowed"].iloc[0]) if not phase186.empty and str(phase186["promotion_allowed"].iloc[0]) != "" else 0
    closure_paper_live_allowed = int(phase186["paper_or_live_acceptance_allowed"].iloc[0]) if not phase186.empty and str(phase186["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    sparse_test_rows_used = int(phase187["test_rows_used"].iloc[0]) if not phase187.empty and str(phase187["test_rows_used"].iloc[0]) != "" else 0
    sparse_test_replay_allowed = int(phase187["test_replay_allowed_next"].iloc[0]) if not phase187.empty and str(phase187["test_replay_allowed_next"].iloc[0]) != "" else 0
    sparse_promotion_allowed = int(phase187["promotion_allowed"].iloc[0]) if not phase187.empty and str(phase187["promotion_allowed"].iloc[0]) != "" else 0
    sparse_paper_live_allowed = int(phase187["paper_or_live_acceptance_allowed"].iloc[0]) if not phase187.empty and str(phase187["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    interp188_test_replay_allowed = int(phase188["test_replay_allowed_next"].iloc[0]) if not phase188.empty and str(phase188["test_replay_allowed_next"].iloc[0]) != "" else 0
    interp188_promotion_allowed = int(phase188["promotion_allowed"].iloc[0]) if not phase188.empty and str(phase188["promotion_allowed"].iloc[0]) != "" else 0
    interp188_paper_live_allowed = int(phase188["paper_or_live_acceptance_allowed"].iloc[0]) if not phase188.empty and str(phase188["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    decision189_test_precommit_allowed = int(phase189["untouched_test_replay_precommit_allowed"].iloc[0]) if not phase189.empty and str(phase189["untouched_test_replay_precommit_allowed"].iloc[0]) != "" else 0
    decision189_test_replay_allowed = int(phase189["test_replay_allowed_next"].iloc[0]) if not phase189.empty and str(phase189["test_replay_allowed_next"].iloc[0]) != "" else 0
    decision189_promotion_allowed = int(phase189["promotion_allowed"].iloc[0]) if not phase189.empty and str(phase189["promotion_allowed"].iloc[0]) != "" else 0
    decision189_paper_live_allowed = int(phase189["paper_or_live_acceptance_allowed"].iloc[0]) if not phase189.empty and str(phase189["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase190_test_replay_execution = int(phase190["test_replay_execution"].iloc[0]) if not phase190.empty and str(phase190["test_replay_execution"].iloc[0]) != "" else 0
    phase190_test_replay_allowed = int(phase190["test_replay_allowed_next"].iloc[0]) if not phase190.empty and str(phase190["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase190_promotion_allowed = int(phase190["promotion_allowed"].iloc[0]) if not phase190.empty and str(phase190["promotion_allowed"].iloc[0]) != "" else 0
    phase190_paper_live_allowed = int(phase190["paper_or_live_acceptance_allowed"].iloc[0]) if not phase190.empty and str(phase190["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase191_test_replay_execution = int(phase191["test_replay_execution"].iloc[0]) if not phase191.empty and str(phase191["test_replay_execution"].iloc[0]) != "" else 0
    phase191_test_result_allowed = int(phase191["test_result_allowed"].iloc[0]) if not phase191.empty and str(phase191["test_result_allowed"].iloc[0]) != "" else 0
    phase191_test_replay_allowed = int(phase191["test_replay_allowed_next"].iloc[0]) if not phase191.empty and str(phase191["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase191_promotion_allowed = int(phase191["promotion_allowed"].iloc[0]) if not phase191.empty and str(phase191["promotion_allowed"].iloc[0]) != "" else 0
    phase191_paper_live_allowed = int(phase191["paper_or_live_acceptance_allowed"].iloc[0]) if not phase191.empty and str(phase191["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase192_test_replay_execution = int(phase192["test_replay_execution"].iloc[0]) if not phase192.empty and str(phase192["test_replay_execution"].iloc[0]) != "" else 0
    phase192_test_result_allowed = int(phase192["test_result_allowed"].iloc[0]) if not phase192.empty and str(phase192["test_result_allowed"].iloc[0]) != "" else 0
    phase192_promotion_allowed = int(phase192["promotion_allowed"].iloc[0]) if not phase192.empty and str(phase192["promotion_allowed"].iloc[0]) != "" else 0
    phase192_paper_live_allowed = int(phase192["paper_or_live_acceptance_allowed"].iloc[0]) if not phase192.empty and str(phase192["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase193_test_replay_execution = int(phase193["test_replay_execution"].iloc[0]) if not phase193.empty and str(phase193["test_replay_execution"].iloc[0]) != "" else 0
    phase193_test_result_allowed = int(phase193["test_result_allowed"].iloc[0]) if not phase193.empty and str(phase193["test_result_allowed"].iloc[0]) != "" else 0
    phase193_promotion_allowed = int(phase193["promotion_allowed"].iloc[0]) if not phase193.empty and str(phase193["promotion_allowed"].iloc[0]) != "" else 0
    phase193_paper_live_allowed = int(phase193["paper_or_live_acceptance_allowed"].iloc[0]) if not phase193.empty and str(phase193["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase194_test_replay_allowed = int(phase194["test_replay_allowed_next"].iloc[0]) if not phase194.empty and str(phase194["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase194_promotion_allowed = int(phase194["promotion_allowed"].iloc[0]) if not phase194.empty and str(phase194["promotion_allowed"].iloc[0]) != "" else 0
    phase194_paper_live_allowed = int(phase194["paper_or_live_acceptance_allowed"].iloc[0]) if not phase194.empty and str(phase194["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase195_test_replay_allowed = int(phase195["test_replay_allowed_next"].iloc[0]) if not phase195.empty and str(phase195["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase195_promotion_allowed = int(phase195["promotion_allowed"].iloc[0]) if not phase195.empty and str(phase195["promotion_allowed"].iloc[0]) != "" else 0
    phase195_paper_live_allowed = int(phase195["paper_or_live_acceptance_allowed"].iloc[0]) if not phase195.empty and str(phase195["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase196_test_replay_allowed = int(phase196["test_replay_allowed_next"].iloc[0]) if not phase196.empty and str(phase196["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase196_promotion_allowed = int(phase196["promotion_allowed"].iloc[0]) if not phase196.empty and str(phase196["promotion_allowed"].iloc[0]) != "" else 0
    phase196_paper_live_allowed = int(phase196["paper_or_live_acceptance_allowed"].iloc[0]) if not phase196.empty and str(phase196["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase197_strategy_replay_allowed = int(phase197["strategy_replay_allowed"].iloc[0]) if not phase197.empty and str(phase197["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase197_test_replay_allowed = int(phase197["test_replay_allowed_next"].iloc[0]) if not phase197.empty and str(phase197["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase197_promotion_allowed = int(phase197["promotion_allowed"].iloc[0]) if not phase197.empty and str(phase197["promotion_allowed"].iloc[0]) != "" else 0
    phase197_paper_live_allowed = int(phase197["paper_or_live_acceptance_allowed"].iloc[0]) if not phase197.empty and str(phase197["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase198_test_replay_allowed = int(phase198["test_replay_allowed_next"].iloc[0]) if not phase198.empty and str(phase198["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase198_promotion_allowed = int(phase198["promotion_allowed"].iloc[0]) if not phase198.empty and str(phase198["promotion_allowed"].iloc[0]) != "" else 0
    phase198_paper_live_allowed = int(phase198["paper_or_live_acceptance_allowed"].iloc[0]) if not phase198.empty and str(phase198["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase199_strategy_replay_allowed = int(phase199["strategy_replay_allowed"].iloc[0]) if not phase199.empty and str(phase199["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase199_test_replay_allowed = int(phase199["test_replay_allowed_next"].iloc[0]) if not phase199.empty and str(phase199["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase199_precommit_allowed = int(phase199["untouched_test_replay_precommit_allowed"].iloc[0]) if not phase199.empty and str(phase199["untouched_test_replay_precommit_allowed"].iloc[0]) != "" else 0
    phase199_promotion_allowed = int(phase199["promotion_allowed"].iloc[0]) if not phase199.empty and str(phase199["promotion_allowed"].iloc[0]) != "" else 0
    phase199_paper_live_allowed = int(phase199["paper_or_live_acceptance_allowed"].iloc[0]) if not phase199.empty and str(phase199["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase200_strategy_replay_allowed = int(phase200["strategy_replay_allowed"].iloc[0]) if not phase200.empty and str(phase200["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase200_test_replay_allowed = int(phase200["test_replay_allowed_next"].iloc[0]) if not phase200.empty and str(phase200["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase200_promotion_allowed = int(phase200["promotion_allowed"].iloc[0]) if not phase200.empty and str(phase200["promotion_allowed"].iloc[0]) != "" else 0
    phase200_paper_live_allowed = int(phase200["paper_or_live_acceptance_allowed"].iloc[0]) if not phase200.empty and str(phase200["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase201_strategy_replay_allowed = int(phase201["strategy_replay_allowed"].iloc[0]) if not phase201.empty and str(phase201["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase201_test_replay_allowed = int(phase201["test_replay_allowed_next"].iloc[0]) if not phase201.empty and str(phase201["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase201_promotion_allowed = int(phase201["promotion_allowed"].iloc[0]) if not phase201.empty and str(phase201["promotion_allowed"].iloc[0]) != "" else 0
    phase201_paper_live_allowed = int(phase201["paper_or_live_acceptance_allowed"].iloc[0]) if not phase201.empty and str(phase201["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase202_strategy_replay_allowed = int(phase202["strategy_replay_allowed"].iloc[0]) if not phase202.empty and str(phase202["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase202_test_replay_allowed = int(phase202["test_replay_allowed_next"].iloc[0]) if not phase202.empty and str(phase202["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase202_promotion_allowed = int(phase202["promotion_allowed"].iloc[0]) if not phase202.empty and str(phase202["promotion_allowed"].iloc[0]) != "" else 0
    phase202_paper_live_allowed = int(phase202["paper_or_live_acceptance_allowed"].iloc[0]) if not phase202.empty and str(phase202["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase203_strategy_replay_allowed = int(phase203["strategy_replay_allowed"].iloc[0]) if not phase203.empty and str(phase203["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase203_test_replay_allowed = int(phase203["test_replay_allowed_next"].iloc[0]) if not phase203.empty and str(phase203["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase203_promotion_allowed = int(phase203["promotion_allowed"].iloc[0]) if not phase203.empty and str(phase203["promotion_allowed"].iloc[0]) != "" else 0
    phase203_paper_live_allowed = int(phase203["paper_or_live_acceptance_allowed"].iloc[0]) if not phase203.empty and str(phase203["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase204_strategy_replay_allowed = int(phase204["strategy_replay_allowed"].iloc[0]) if not phase204.empty and str(phase204["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase204_test_replay_allowed = int(phase204["test_replay_allowed_next"].iloc[0]) if not phase204.empty and str(phase204["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase204_promotion_allowed = int(phase204["promotion_allowed"].iloc[0]) if not phase204.empty and str(phase204["promotion_allowed"].iloc[0]) != "" else 0
    phase204_paper_live_allowed = int(phase204["paper_or_live_acceptance_allowed"].iloc[0]) if not phase204.empty and str(phase204["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase205_strategy_replay_allowed = int(phase205["strategy_replay_allowed"].iloc[0]) if not phase205.empty and str(phase205["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase205_test_replay_allowed = int(phase205["test_replay_allowed_next"].iloc[0]) if not phase205.empty and str(phase205["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase205_promotion_allowed = int(phase205["promotion_allowed"].iloc[0]) if not phase205.empty and str(phase205["promotion_allowed"].iloc[0]) != "" else 0
    phase205_paper_live_allowed = int(phase205["paper_or_live_acceptance_allowed"].iloc[0]) if not phase205.empty and str(phase205["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase206_model_fit_allowed = as_int(phase206_metrics.get("model_fit_allowed", 0))
    phase206_strategy_replay_allowed = int(phase206["strategy_replay_allowed"].iloc[0]) if not phase206.empty and str(phase206["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase206_test_replay_allowed = int(phase206["test_replay_allowed_next"].iloc[0]) if not phase206.empty and str(phase206["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase206_promotion_allowed = int(phase206["promotion_allowed"].iloc[0]) if not phase206.empty and str(phase206["promotion_allowed"].iloc[0]) != "" else 0
    phase206_paper_live_allowed = int(phase206["paper_or_live_acceptance_allowed"].iloc[0]) if not phase206.empty and str(phase206["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase207_metrics = phase_status_from_metrics(207)
    phase207_model_fit_allowed = as_int(phase207_metrics.get("model_fit_allowed", 0))
    phase207_strategy_replay_allowed = int(phase207["strategy_replay_allowed"].iloc[0]) if not phase207.empty and str(phase207["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase207_test_replay_allowed = int(phase207["test_replay_allowed_next"].iloc[0]) if not phase207.empty and str(phase207["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase207_promotion_allowed = int(phase207["promotion_allowed"].iloc[0]) if not phase207.empty and str(phase207["promotion_allowed"].iloc[0]) != "" else 0
    phase207_paper_live_allowed = int(phase207["paper_or_live_acceptance_allowed"].iloc[0]) if not phase207.empty and str(phase207["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase208_metrics = phase_status_from_metrics(208)
    phase208_model_fit_allowed = as_int(phase208_metrics.get("model_fit_allowed", 0))
    phase208_strategy_replay_allowed = int(phase208["strategy_replay_allowed"].iloc[0]) if not phase208.empty and str(phase208["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase208_test_replay_allowed = int(phase208["test_replay_allowed_next"].iloc[0]) if not phase208.empty and str(phase208["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase208_promotion_allowed = int(phase208["promotion_allowed"].iloc[0]) if not phase208.empty and str(phase208["promotion_allowed"].iloc[0]) != "" else 0
    phase208_paper_live_allowed = int(phase208["paper_or_live_acceptance_allowed"].iloc[0]) if not phase208.empty and str(phase208["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase209_metrics = phase_status_from_metrics(209)
    phase209_model_fit_execution_allowed = as_int(phase209_metrics.get("model_fit_execution_allowed", 0))
    phase209_strategy_replay_allowed = int(phase209["strategy_replay_allowed"].iloc[0]) if not phase209.empty and str(phase209["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase209_test_replay_allowed = int(phase209["test_replay_allowed_next"].iloc[0]) if not phase209.empty and str(phase209["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase209_promotion_allowed = int(phase209["promotion_allowed"].iloc[0]) if not phase209.empty and str(phase209["promotion_allowed"].iloc[0]) != "" else 0
    phase209_paper_live_allowed = int(phase209["paper_or_live_acceptance_allowed"].iloc[0]) if not phase209.empty and str(phase209["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase210_metrics = phase_status_from_metrics(210)
    phase210_model_fit_execution = as_int(phase210_metrics.get("model_fit_execution", 0))
    phase210_test_rows_used = as_int(phase210_metrics.get("test_rows_used", 0))
    phase210_strategy_replay_allowed = int(phase210["strategy_replay_allowed"].iloc[0]) if not phase210.empty and str(phase210["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase210_test_replay_allowed = int(phase210["test_replay_allowed_next"].iloc[0]) if not phase210.empty and str(phase210["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase210_promotion_allowed = int(phase210["promotion_allowed"].iloc[0]) if not phase210.empty and str(phase210["promotion_allowed"].iloc[0]) != "" else 0
    phase210_paper_live_allowed = int(phase210["paper_or_live_acceptance_allowed"].iloc[0]) if not phase210.empty and str(phase210["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase210_profitability_claim_allowed = as_int(phase210_metrics.get("profitability_claim_allowed", 0))
    phase211_metrics = phase_status_from_metrics(211)
    phase211_candidate_opened_for_replay = as_int(phase211_metrics.get("candidate_opened_for_replay", 0))
    phase211_strategy_replay_allowed = int(phase211["strategy_replay_allowed"].iloc[0]) if not phase211.empty and str(phase211["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase211_test_replay_allowed = int(phase211["test_replay_allowed_next"].iloc[0]) if not phase211.empty and str(phase211["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase211_promotion_allowed = int(phase211["promotion_allowed"].iloc[0]) if not phase211.empty and str(phase211["promotion_allowed"].iloc[0]) != "" else 0
    phase211_paper_live_allowed = int(phase211["paper_or_live_acceptance_allowed"].iloc[0]) if not phase211.empty and str(phase211["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase211_profitability_claim_allowed = as_int(phase211_metrics.get("profitability_claim_allowed", 0))
    phase212_metrics = phase_status_from_metrics(212)
    phase212_candidate_opened_for_replay = as_int(phase212_metrics.get("candidate_opened_for_replay", 0))
    phase212_model_fit_allowed_next = as_int(phase212_metrics.get("model_fit_allowed_next", 0))
    phase212_strategy_replay_allowed = int(phase212["strategy_replay_allowed"].iloc[0]) if not phase212.empty and str(phase212["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase212_test_replay_allowed = int(phase212["test_replay_allowed_next"].iloc[0]) if not phase212.empty and str(phase212["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase212_promotion_allowed = int(phase212["promotion_allowed"].iloc[0]) if not phase212.empty and str(phase212["promotion_allowed"].iloc[0]) != "" else 0
    phase212_paper_live_allowed = int(phase212["paper_or_live_acceptance_allowed"].iloc[0]) if not phase212.empty and str(phase212["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase212_profitability_claim_allowed = as_int(phase212_metrics.get("profitability_claim_allowed", 0))
    phase213_metrics = phase_status_from_metrics(213)
    phase213_model_fit_allowed_next = as_int(phase213_metrics.get("model_fit_allowed_next", 0))
    phase213_strategy_replay_allowed = int(phase213["strategy_replay_allowed"].iloc[0]) if not phase213.empty and str(phase213["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase213_test_replay_allowed = int(phase213["test_replay_allowed_next"].iloc[0]) if not phase213.empty and str(phase213["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase213_promotion_allowed = int(phase213["promotion_allowed"].iloc[0]) if not phase213.empty and str(phase213["promotion_allowed"].iloc[0]) != "" else 0
    phase213_paper_live_allowed = int(phase213["paper_or_live_acceptance_allowed"].iloc[0]) if not phase213.empty and str(phase213["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase213_profitability_claim_allowed = as_int(phase213_metrics.get("profitability_claim_allowed", 0))
    phase214_metrics = phase_status_from_metrics(214)
    phase214_model_fit_allowed_next = as_int(phase214_metrics.get("model_fit_allowed_next", 0))
    phase214_sealed_test_rows_used = as_int(phase214_metrics.get("sealed_test_rows_used", 0))
    phase214_strategy_replay_allowed = int(phase214["strategy_replay_allowed"].iloc[0]) if not phase214.empty and str(phase214["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase214_test_replay_allowed = int(phase214["test_replay_allowed_next"].iloc[0]) if not phase214.empty and str(phase214["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase214_promotion_allowed = int(phase214["promotion_allowed"].iloc[0]) if not phase214.empty and str(phase214["promotion_allowed"].iloc[0]) != "" else 0
    phase214_paper_live_allowed = int(phase214["paper_or_live_acceptance_allowed"].iloc[0]) if not phase214.empty and str(phase214["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase214_profitability_claim_allowed = as_int(phase214_metrics.get("profitability_claim_allowed", 0))
    phase215_metrics = phase_status_from_metrics(215)
    phase215_model_fit_allowed_next = as_int(phase215_metrics.get("model_fit_allowed_next", 0))
    phase215_strategy_replay_allowed = int(phase215["strategy_replay_allowed"].iloc[0]) if not phase215.empty and str(phase215["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase215_test_replay_allowed = int(phase215["test_replay_allowed_next"].iloc[0]) if not phase215.empty and str(phase215["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase215_promotion_allowed = int(phase215["promotion_allowed"].iloc[0]) if not phase215.empty and str(phase215["promotion_allowed"].iloc[0]) != "" else 0
    phase215_paper_live_allowed = int(phase215["paper_or_live_acceptance_allowed"].iloc[0]) if not phase215.empty and str(phase215["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase215_profitability_claim_allowed = as_int(phase215_metrics.get("profitability_claim_allowed", 0))
    phase216_metrics = phase_status_from_metrics(216)
    phase216_model_fit_allowed_next = as_int(phase216_metrics.get("model_fit_allowed_next", 0))
    phase216_strategy_replay_allowed = int(phase216["strategy_replay_allowed"].iloc[0]) if not phase216.empty and str(phase216["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase216_test_replay_allowed = int(phase216["test_replay_allowed_next"].iloc[0]) if not phase216.empty and str(phase216["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase216_promotion_allowed = int(phase216["promotion_allowed"].iloc[0]) if not phase216.empty and str(phase216["promotion_allowed"].iloc[0]) != "" else 0
    phase216_paper_live_allowed = int(phase216["paper_or_live_acceptance_allowed"].iloc[0]) if not phase216.empty and str(phase216["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase216_profitability_claim_allowed = as_int(phase216_metrics.get("profitability_claim_allowed", 0))
    phase217_metrics = phase_status_from_metrics(217)
    phase217_row_level_export_allowed = as_int(phase217_metrics.get("row_level_design_matrix_export_allowed", 0))
    phase217_model_fit_allowed_next = as_int(phase217_metrics.get("model_fit_allowed_next", 0))
    phase217_strategy_replay_allowed = int(phase217["strategy_replay_allowed"].iloc[0]) if not phase217.empty and str(phase217["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase217_test_replay_allowed = int(phase217["test_replay_allowed_next"].iloc[0]) if not phase217.empty and str(phase217["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase217_promotion_allowed = int(phase217["promotion_allowed"].iloc[0]) if not phase217.empty and str(phase217["promotion_allowed"].iloc[0]) != "" else 0
    phase217_paper_live_allowed = int(phase217["paper_or_live_acceptance_allowed"].iloc[0]) if not phase217.empty and str(phase217["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase217_profitability_claim_allowed = as_int(phase217_metrics.get("profitability_claim_allowed", 0))
    phase218_metrics = phase_status_from_metrics(218)
    phase218_dry_run_precommitted = as_int(phase218_metrics.get("model_fit_dry_run_precommitted_for_phase219", 0))
    phase218_model_fit_execution_allowed = as_int(phase218_metrics.get("model_fit_execution_allowed", 0))
    phase218_strategy_replay_allowed = int(phase218["strategy_replay_allowed"].iloc[0]) if not phase218.empty and str(phase218["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase218_test_replay_allowed = int(phase218["test_replay_allowed_next"].iloc[0]) if not phase218.empty and str(phase218["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase218_promotion_allowed = int(phase218["promotion_allowed"].iloc[0]) if not phase218.empty and str(phase218["promotion_allowed"].iloc[0]) != "" else 0
    phase218_paper_live_allowed = int(phase218["paper_or_live_acceptance_allowed"].iloc[0]) if not phase218.empty and str(phase218["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase218_profitability_claim_allowed = as_int(phase218_metrics.get("profitability_claim_allowed", 0))
    phase219_metrics = phase_status_from_metrics(219)
    phase219_model_fit_execution = as_int(phase219_metrics.get("model_fit_execution", 0))
    phase219_strategy_replay_allowed = int(phase219["strategy_replay_allowed"].iloc[0]) if not phase219.empty and str(phase219["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase219_test_replay_allowed = int(phase219["test_replay_allowed_next"].iloc[0]) if not phase219.empty and str(phase219["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase219_test_rows_used = as_int(phase219_metrics.get("test_rows_used", 0))
    phase219_promotion_allowed = int(phase219["promotion_allowed"].iloc[0]) if not phase219.empty and str(phase219["promotion_allowed"].iloc[0]) != "" else 0
    phase219_paper_live_allowed = int(phase219["paper_or_live_acceptance_allowed"].iloc[0]) if not phase219.empty and str(phase219["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase219_profitability_claim_allowed = as_int(phase219_metrics.get("profitability_claim_allowed", 0))
    phase220_metrics = phase_status_from_metrics(220)
    phase220_candidate_opened = as_int(phase220_metrics.get("candidate_opened_for_phase221_precommit", 0))
    phase220_strategy_replay_allowed = int(phase220["strategy_replay_allowed"].iloc[0]) if not phase220.empty and str(phase220["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase220_test_replay_allowed = int(phase220["test_replay_allowed_next"].iloc[0]) if not phase220.empty and str(phase220["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase220_promotion_allowed = int(phase220["promotion_allowed"].iloc[0]) if not phase220.empty and str(phase220["promotion_allowed"].iloc[0]) != "" else 0
    phase220_paper_live_allowed = int(phase220["paper_or_live_acceptance_allowed"].iloc[0]) if not phase220.empty and str(phase220["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase220_profitability_claim_allowed = as_int(phase220_metrics.get("profitability_claim_allowed", 0))
    phase221_metrics = phase_status_from_metrics(221)
    phase221_phase222_replay_precommitted = as_int(phase221_metrics.get("phase222_replay_dry_run_precommitted", 0))
    phase221_replay_execution_allowed = as_int(phase221_metrics.get("strategy_replay_execution_allowed", 0))
    phase221_strategy_replay_allowed_next = as_int(phase221_metrics.get("strategy_replay_allowed_next", 0))
    phase221_test_replay_allowed = int(phase221["test_replay_allowed_next"].iloc[0]) if not phase221.empty and str(phase221["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase221_promotion_allowed = int(phase221["promotion_allowed"].iloc[0]) if not phase221.empty and str(phase221["promotion_allowed"].iloc[0]) != "" else 0
    phase221_paper_live_allowed = int(phase221["paper_or_live_acceptance_allowed"].iloc[0]) if not phase221.empty and str(phase221["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase221_profitability_claim_allowed = as_int(phase221_metrics.get("profitability_claim_allowed", 0))
    phase222_metrics = phase_status_from_metrics(222)
    phase222_strategy_replay_execution = as_int(phase222_metrics.get("strategy_replay_execution", 0))
    phase222_test_replay_allowed = int(phase222["test_replay_allowed_next"].iloc[0]) if not phase222.empty and str(phase222["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase222_test_rows_used = as_int(phase222_metrics.get("test_rows_used", 0))
    phase222_promotion_allowed = int(phase222["promotion_allowed"].iloc[0]) if not phase222.empty and str(phase222["promotion_allowed"].iloc[0]) != "" else 0
    phase222_paper_live_allowed = int(phase222["paper_or_live_acceptance_allowed"].iloc[0]) if not phase222.empty and str(phase222["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase222_profitability_claim_allowed = as_int(phase222_metrics.get("profitability_claim_allowed", 0))
    phase223_metrics = phase_status_from_metrics(223)
    phase223_passing_interpretation_rows = as_int(phase223_metrics.get("passing_interpretation_rows", 0))
    phase223_broader_replay_allowed_next = as_int(phase223_metrics.get("broader_replay_allowed_next", 0))
    phase223_test_replay_allowed = int(phase223["test_replay_allowed_next"].iloc[0]) if not phase223.empty and str(phase223["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase223_test_rows_used = as_int(phase223_metrics.get("test_rows_used", 0))
    phase223_promotion_allowed = int(phase223["promotion_allowed"].iloc[0]) if not phase223.empty and str(phase223["promotion_allowed"].iloc[0]) != "" else 0
    phase223_paper_live_allowed = int(phase223["paper_or_live_acceptance_allowed"].iloc[0]) if not phase223.empty and str(phase223["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase223_profitability_claim_allowed = as_int(phase223_metrics.get("profitability_claim_allowed", 0))
    phase223_phase224_work_order_rows = as_int(phase223_metrics.get("phase224_work_order_rows", 0))
    phase224_metrics = phase_status_from_metrics(224)
    phase224_closed_broader = as_int(phase224_metrics.get("current_candidate_set_closed_for_broader_replay", 0))
    phase224_closed_test = as_int(phase224_metrics.get("current_candidate_set_closed_for_test", 0))
    phase224_reuse_without_redesign = as_int(phase224_metrics.get("reuse_without_material_redesign_allowed", 0))
    phase224_phase225_work_order_rows = as_int(phase224_metrics.get("phase225_work_order_rows", 0))
    phase224_model_fit_allowed_next = as_int(phase224_metrics.get("model_fit_allowed_next", 0))
    phase224_strategy_replay_allowed = as_int(phase224_metrics.get("strategy_replay_allowed", 0))
    phase224_broader_replay_allowed_next = as_int(phase224_metrics.get("broader_replay_allowed_next", 0))
    phase224_test_replay_allowed = int(phase224["test_replay_allowed_next"].iloc[0]) if not phase224.empty and str(phase224["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase224_promotion_allowed = int(phase224["promotion_allowed"].iloc[0]) if not phase224.empty and str(phase224["promotion_allowed"].iloc[0]) != "" else 0
    phase224_paper_live_allowed = int(phase224["paper_or_live_acceptance_allowed"].iloc[0]) if not phase224.empty and str(phase224["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase224_profitability_claim_allowed = as_int(phase224_metrics.get("profitability_claim_allowed", 0))
    phase225_metrics = phase_status_from_metrics(225)
    phase225_label_materialization_allowed_next = as_int(phase225_metrics.get("label_materialization_allowed_next", 0))
    phase225_phase226_work_order_rows = as_int(phase225_metrics.get("phase226_work_order_rows", 0))
    phase225_model_fit_allowed_next = as_int(phase225_metrics.get("model_fit_allowed_next", 0))
    phase225_strategy_replay_allowed = as_int(phase225_metrics.get("strategy_replay_allowed", 0))
    phase225_broader_replay_allowed_next = as_int(phase225_metrics.get("broader_replay_allowed_next", 0))
    phase225_test_replay_allowed = int(phase225["test_replay_allowed_next"].iloc[0]) if not phase225.empty and str(phase225["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase225_test_rows_used = as_int(phase225_metrics.get("test_rows_used", 0))
    phase225_promotion_allowed = int(phase225["promotion_allowed"].iloc[0]) if not phase225.empty and str(phase225["promotion_allowed"].iloc[0]) != "" else 0
    phase225_paper_live_allowed = int(phase225["paper_or_live_acceptance_allowed"].iloc[0]) if not phase225.empty and str(phase225["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase225_profitability_claim_allowed = as_int(phase225_metrics.get("profitability_claim_allowed", 0))
    phase226_metrics = phase_status_from_metrics(226)
    phase226_materialized_horizons = as_int(phase226_metrics.get("materialized_horizons", 0))
    phase226_actionable_rows = as_int(phase226_metrics.get("cost_aware_actionable_rows", 0))
    phase226_quality_pass_rows = as_int(phase226_metrics.get("quality_pass_rows", 0))
    phase226_model_fit_allowed_next = as_int(phase226_metrics.get("model_fit_allowed_next", 0))
    phase226_strategy_replay_allowed = as_int(phase226_metrics.get("strategy_replay_allowed", 0))
    phase226_broader_replay_allowed_next = as_int(phase226_metrics.get("broader_replay_allowed_next", 0))
    phase226_test_replay_allowed = int(phase226["test_replay_allowed_next"].iloc[0]) if not phase226.empty and str(phase226["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase226_test_rows_used = as_int(phase226_metrics.get("test_rows_used", 0))
    phase226_promotion_allowed = int(phase226["promotion_allowed"].iloc[0]) if not phase226.empty and str(phase226["promotion_allowed"].iloc[0]) != "" else 0
    phase226_paper_live_allowed = int(phase226["paper_or_live_acceptance_allowed"].iloc[0]) if not phase226.empty and str(phase226["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase226_profitability_claim_allowed = as_int(phase226_metrics.get("profitability_claim_allowed", 0))
    phase227_metrics = phase_status_from_metrics(227)
    phase227_fit_precommit_candidate_rows = as_int(phase227_metrics.get("fit_precommit_candidate_rows", 0))
    phase227_phase228_work_order_rows = as_int(phase227_metrics.get("phase228_work_order_rows", 0))
    phase227_model_fit_allowed_next = as_int(phase227_metrics.get("model_fit_allowed_next", 0))
    phase227_strategy_replay_allowed = as_int(phase227_metrics.get("strategy_replay_allowed", 0))
    phase227_broader_replay_allowed_next = as_int(phase227_metrics.get("broader_replay_allowed_next", 0))
    phase227_test_replay_allowed = int(phase227["test_replay_allowed_next"].iloc[0]) if not phase227.empty and str(phase227["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase227_test_rows_used = as_int(phase227_metrics.get("test_rows_used", 0))
    phase227_promotion_allowed = int(phase227["promotion_allowed"].iloc[0]) if not phase227.empty and str(phase227["promotion_allowed"].iloc[0]) != "" else 0
    phase227_paper_live_allowed = int(phase227["paper_or_live_acceptance_allowed"].iloc[0]) if not phase227.empty and str(phase227["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase227_profitability_claim_allowed = as_int(phase227_metrics.get("profitability_claim_allowed", 0))
    phase228_metrics = phase_status_from_metrics(228)
    phase228_closed_fit = as_int(phase228_metrics.get("current_label_set_closed_for_fit", 0))
    phase228_closed_replay = as_int(phase228_metrics.get("current_label_set_closed_for_replay", 0))
    phase228_phase229_work_order_rows = as_int(phase228_metrics.get("phase229_work_order_rows", 0))
    phase228_label_materialization_allowed_next = as_int(phase228_metrics.get("label_materialization_allowed_next", 0))
    phase228_threshold_widening_allowed = as_int(phase228_metrics.get("threshold_widening_allowed", 0))
    phase228_model_fit_allowed_next = as_int(phase228_metrics.get("model_fit_allowed_next", 0))
    phase228_strategy_replay_allowed = as_int(phase228_metrics.get("strategy_replay_allowed", 0))
    phase228_broader_replay_allowed_next = as_int(phase228_metrics.get("broader_replay_allowed_next", 0))
    phase228_test_replay_allowed = int(phase228["test_replay_allowed_next"].iloc[0]) if not phase228.empty and str(phase228["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase228_test_rows_used = as_int(phase228_metrics.get("test_rows_used", 0))
    phase228_promotion_allowed = int(phase228["promotion_allowed"].iloc[0]) if not phase228.empty and str(phase228["promotion_allowed"].iloc[0]) != "" else 0
    phase228_paper_live_allowed = int(phase228["paper_or_live_acceptance_allowed"].iloc[0]) if not phase228.empty and str(phase228["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase228_profitability_claim_allowed = as_int(phase228_metrics.get("profitability_claim_allowed", 0))
    secure_download_recorded = bool(not phase174.empty and "secure_download" in str(phase174["status"].iloc[0]))
    feature_schema_recorded = bool(not phase175.empty and "feature_schema" in str(phase175["status"].iloc[0]))
    phase176_status = str(phase176["status"].iloc[0]) if not phase176.empty else ""
    materializer_recorded = bool(not phase176.empty and ("materializer" in phase176_status or "receive_flow_features_materialized" in phase176_status))
    quality_audit_recorded = bool(not phase177.empty and "quality_audit" in str(phase177["status"].iloc[0]))
    handoff_recorded = bool(not phase178.empty and "handoff" in str(phase178["status"].iloc[0]))
    strategy_precommit_recorded = bool(not phase179.empty and "strategy_family_precommitted" in str(phase179["status"].iloc[0]))
    cost_label_precommit_recorded = bool(not phase180.empty and "cost_latency_label_precommitted" in str(phase180["status"].iloc[0]))
    label_materialization_recorded = bool(not phase181.empty and "labels_materialized" in str(phase181["status"].iloc[0]))
    label_audit_recorded = bool(not phase182.empty and "label_quality_leakage_audited" in str(phase182["status"].iloc[0]))
    replay_readiness_recorded = bool(not phase183.empty and "replay_readiness_precommitted" in str(phase183["status"].iloc[0]))
    dry_run_recorded = bool(not phase184.empty and "train_validation_replay_dry_run_complete" in str(phase184["status"].iloc[0]))
    interpretation_recorded = bool(not phase185.empty and "validation_interpretation_cost_dominated" in str(phase185["status"].iloc[0]))
    closure_recorded = bool(not phase186.empty and "current_family_set_closed" in str(phase186["status"].iloc[0]))
    sparse_candidate_recorded = bool(not phase187.empty and "cost_aware_sparse_candidate" in str(phase187["status"].iloc[0]))
    sparse_interpretation_recorded = bool(not phase188.empty and "sparse_candidate_interpreted" in str(phase188["status"].iloc[0]))
    decision189_recorded = bool(not phase189.empty and "test_replay_deferred" in str(phase189["status"].iloc[0]))
    phase190_recorded = bool(not phase190.empty and "diagnostic_test_spec_written" in str(phase190["status"].iloc[0]))
    phase191_recorded = bool(not phase191.empty and "diagnostic_test_replay_precommitted" in str(phase191["status"].iloc[0]))
    phase192_recorded = bool(not phase192.empty and "real_validation_date_downloaded" in str(phase192["status"].iloc[0]))
    phase193_recorded = bool(not phase193.empty and "validation_breadth_extended" in str(phase193["status"].iloc[0]))
    phase194_recorded = bool(not phase194.empty and "frozen_sparse_candidate_closed" in str(phase194["status"].iloc[0]))
    phase195_recorded = bool(not phase195.empty and "redesign_search" in str(phase195["status"].iloc[0]))
    phase196_recorded = bool(not phase196.empty and "expanded_feature_model_search" in str(phase196["status"].iloc[0]))
    phase197_recorded = bool(not phase197.empty and "non_receive_flow_feature_expansion" in str(phase197["status"].iloc[0]))
    phase198_recorded = bool(not phase198.empty and "non_receive_flow_context_model_search" in str(phase198["status"].iloc[0]))
    phase199_recorded = bool(not phase199.empty and "branch_paused_material_redesign" in str(phase199["status"].iloc[0]))
    phase200_recorded = bool(not phase200.empty and "material_new_passive_queue_hypothesis" in str(phase200["status"].iloc[0]))
    phase201_recorded = bool(not phase201.empty and "passive_queue_stage01_label_expansion" in str(phase201["status"].iloc[0]))
    phase202_recorded = bool(not phase202.empty and "passive_feature_redesign" in str(phase202["status"].iloc[0]))
    phase203_recorded = bool(not phase203.empty and "redesigned_passive_labels_materialized" in str(phase203["status"].iloc[0]))
    phase204_recorded = bool(not phase204.empty and "passive_redesign_closed_for_replay" in str(phase204["status"].iloc[0]))
    phase205_recorded = bool(not phase205.empty and "material_new_source_precommitted" in str(phase205["status"].iloc[0]))
    phase206_recorded = bool(not phase206.empty and "selected_source_nonoverlap_feature_contract" in str(phase206["status"].iloc[0]))
    phase207_recorded = bool(not phase207.empty and "allowed_feature_matrix" in str(phase207["status"].iloc[0]))
    phase208_recorded = bool(not phase208.empty and "feature_matrix_quality_gate" in str(phase208["status"].iloc[0]))
    phase209_recorded = bool(not phase209.empty and "model_fit_precommit_spec" in str(phase209["status"].iloc[0]))
    phase210_recorded = bool(not phase210.empty and "train_validation_model_fit_dry_run" in str(phase210["status"].iloc[0]))
    phase211_recorded = bool(not phase211.empty and "model_fit_validation_interpretation" in str(phase211["status"].iloc[0]))
    phase212_recorded = bool(not phase212.empty and "model_family_closure_or_redesign" in str(phase212["status"].iloc[0]))
    phase213_recorded = bool(not phase213.empty and "material_new_model_source" in str(phase213["status"].iloc[0]))
    phase214_recorded = bool(not phase214.empty and "event_surprise_label_materialization" in str(phase214["status"].iloc[0]))
    phase215_recorded = bool(not phase215.empty and "event_surprise_label_quality_interpretation" in str(phase215["status"].iloc[0]))
    phase216_recorded = bool(not phase216.empty and "event_surprise_event_only_target_precommit" in str(phase216["status"].iloc[0]))
    phase217_recorded = bool(not phase217.empty and "event_only_design_matrix_precommit" in str(phase217["status"].iloc[0]))
    phase218_recorded = bool(not phase218.empty and "event_only_model_fit_precommit" in str(phase218["status"].iloc[0]))
    phase219_recorded = bool(not phase219.empty and "event_only_train_validation_model_fit_dry_run" in str(phase219["status"].iloc[0]))
    phase220_recorded = bool(not phase220.empty and "event_only_model_fit_validation_interpretation" in str(phase220["status"].iloc[0]))
    phase221_recorded = bool(not phase221.empty and "event_only_signal_replay_precommit" in str(phase221["status"].iloc[0]))
    phase222_recorded = bool(not phase222.empty and "event_only_train_validation_signal_replay_dry_run" in str(phase222["status"].iloc[0]))
    phase223_recorded = bool(not phase223.empty and "event_only_signal_replay_validation_interpretation" in str(phase223["status"].iloc[0]))
    phase224_recorded = bool(not phase224.empty and "event_only_signal_replay_candidate_set_closed" in str(phase224["status"].iloc[0]))
    phase225_recorded = bool(not phase225.empty and "cost_aware_event_source_redesign_precommit" in str(phase225["status"].iloc[0]))
    phase226_recorded = bool(not phase226.empty and "cost_aware_event_label_materialization" in str(phase226["status"].iloc[0]))
    phase227_recorded = bool(not phase227.empty and "cost_aware_event_label_quality_interpretation" in str(phase227["status"].iloc[0]))
    phase228_recorded = bool(not phase228.empty and "cost_aware_label_set_closed" in str(phase228["status"].iloc[0]))
    branch_closed = bool(not phase136.empty and "closed_clean_falsification" in str(phase136["status"].iloc[0]))
    rows = [
        ("phase149_real_l2_replay_gate_closed", bool(real_replay_allowed == 0), real_replay_allowed, 0, "hard"),
        ("phase149_real_receive_flow_source_gate_open_or_explicitly_blocked", bool(receive_replay_allowed in (0, 1)), receive_replay_allowed, "0_or_1_tracked_by_phase172", "hard"),
        ("phase149_secure_download_gate_recorded", secure_download_recorded, int(secure_download_recorded), 1, "hard"),
        ("phase149_secure_orchestrator_replay_gate_closed", bool(secure_replay_allowed == 0), secure_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_feature_schema_recorded", feature_schema_recorded, int(feature_schema_recorded), 1, "hard"),
        ("phase149_receive_flow_feature_schema_replay_gate_closed", bool(schema_replay_allowed == 0), schema_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_materializer_recorded", materializer_recorded, int(materializer_recorded), 1, "hard"),
        ("phase149_receive_flow_materializer_replay_gate_closed", bool(materializer_replay_allowed == 0), materializer_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_quality_audit_recorded", quality_audit_recorded, int(quality_audit_recorded), 1, "hard"),
        ("phase149_receive_flow_quality_audit_replay_gate_closed", bool(quality_replay_allowed == 0), quality_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_handoff_precommit_recorded", handoff_recorded, int(handoff_recorded), 1, "hard"),
        ("phase149_receive_flow_handoff_replay_gate_closed", bool(handoff_replay_allowed == 0), handoff_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_strategy_family_precommit_recorded", strategy_precommit_recorded, int(strategy_precommit_recorded), 1, "hard"),
        ("phase149_receive_flow_strategy_family_replay_gate_closed", bool(precommit_replay_allowed == 0), precommit_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_latency_label_precommit_recorded", cost_label_precommit_recorded, int(cost_label_precommit_recorded), 1, "hard"),
        ("phase149_receive_flow_cost_latency_label_replay_gate_closed", bool(cost_label_replay_allowed == 0), cost_label_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_label_materialization_recorded", label_materialization_recorded, int(label_materialization_recorded), 1, "hard"),
        ("phase149_receive_flow_label_materialization_replay_gate_closed", bool(label_materialization_replay_allowed == 0), label_materialization_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_label_quality_leakage_audit_recorded", label_audit_recorded, int(label_audit_recorded), 1, "hard"),
        ("phase149_receive_flow_label_quality_leakage_replay_gate_closed", bool(label_audit_replay_allowed == 0), label_audit_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_replay_readiness_precommit_recorded", replay_readiness_recorded, int(replay_readiness_recorded), 1, "hard"),
        ("phase149_receive_flow_replay_readiness_replay_gate_closed", bool(replay_readiness_replay_allowed == 0), replay_readiness_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_replay_readiness_pnl_gate_closed", bool(replay_readiness_pnl_allowed == 0), replay_readiness_pnl_allowed, 0, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_recorded", dry_run_recorded, int(dry_run_recorded), 1, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_test_gate_closed", bool(dry_run_test_rows_used == 0), dry_run_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_promotion_gate_closed", bool(dry_run_promotion_allowed == 0), dry_run_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_paper_live_gate_closed", bool(dry_run_paper_live_allowed == 0), dry_run_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_recorded", interpretation_recorded, int(interpretation_recorded), 1, "hard"),
        ("phase149_receive_flow_validation_interpretation_test_rows_closed", bool(interpretation_test_rows_used == 0), interpretation_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_test_replay_closed", bool(interpretation_test_replay_allowed == 0), interpretation_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_promotion_closed", bool(interpretation_promotion_allowed == 0), interpretation_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_paper_live_closed", bool(interpretation_paper_live_allowed == 0), interpretation_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_recorded", closure_recorded, int(closure_recorded), 1, "hard"),
        ("phase149_receive_flow_current_family_reuse_without_redesign_closed", bool(closure_reuse_allowed == 0), closure_reuse_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_test_replay_closed", bool(closure_test_replay_allowed == 0), closure_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_promotion_closed", bool(closure_promotion_allowed == 0), closure_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_paper_live_closed", bool(closure_paper_live_allowed == 0), closure_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_recorded", sparse_candidate_recorded, int(sparse_candidate_recorded), 1, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_test_rows_closed", bool(sparse_test_rows_used == 0), sparse_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_test_replay_closed", bool(sparse_test_replay_allowed == 0), sparse_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_promotion_closed", bool(sparse_promotion_allowed == 0), sparse_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_paper_live_closed", bool(sparse_paper_live_allowed == 0), sparse_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_recorded", sparse_interpretation_recorded, int(sparse_interpretation_recorded), 1, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_test_replay_closed", bool(interp188_test_replay_allowed == 0), interp188_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_promotion_closed", bool(interp188_promotion_allowed == 0), interp188_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_paper_live_closed", bool(interp188_paper_live_allowed == 0), interp188_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_test_precommit_decision_recorded", decision189_recorded, int(decision189_recorded), 1, "hard"),
        ("phase149_receive_flow_test_precommit_allowed_closed", bool(decision189_test_precommit_allowed == 0), decision189_test_precommit_allowed, 0, "hard"),
        ("phase149_receive_flow_test_replay_still_closed", bool(decision189_test_replay_allowed == 0), decision189_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_test_precommit_decision_promotion_closed", bool(decision189_promotion_allowed == 0), decision189_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_test_precommit_decision_paper_live_closed", bool(decision189_paper_live_allowed == 0), decision189_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase190_diagnostic_spec_recorded", phase190_recorded, int(phase190_recorded), 1, "hard"),
        ("phase149_receive_flow_phase190_test_replay_not_executed", bool(phase190_test_replay_execution == 0), phase190_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase190_test_replay_closed", bool(phase190_test_replay_allowed == 0), phase190_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase190_promotion_closed", bool(phase190_promotion_allowed == 0), phase190_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase190_paper_live_closed", bool(phase190_paper_live_allowed == 0), phase190_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_diagnostic_precommit_recorded", phase191_recorded, int(phase191_recorded), 1, "hard"),
        ("phase149_receive_flow_phase191_test_replay_not_executed", bool(phase191_test_replay_execution == 0), phase191_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase191_test_result_closed", bool(phase191_test_result_allowed == 0), phase191_test_result_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_test_replay_closed", bool(phase191_test_replay_allowed == 0), phase191_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_promotion_closed", bool(phase191_promotion_allowed == 0), phase191_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_paper_live_closed", bool(phase191_paper_live_allowed == 0), phase191_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase192_real_validation_download_recorded", phase192_recorded, int(phase192_recorded), 1, "hard"),
        ("phase149_receive_flow_phase192_test_replay_not_executed", bool(phase192_test_replay_execution == 0), phase192_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase192_test_result_closed", bool(phase192_test_result_allowed == 0), phase192_test_result_allowed, 0, "hard"),
        ("phase149_receive_flow_phase192_promotion_closed", bool(phase192_promotion_allowed == 0), phase192_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase192_paper_live_closed", bool(phase192_paper_live_allowed == 0), phase192_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase193_validation_extension_recorded", phase193_recorded, int(phase193_recorded), 1, "hard"),
        ("phase149_receive_flow_phase193_test_replay_not_executed", bool(phase193_test_replay_execution == 0), phase193_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase193_test_result_closed", bool(phase193_test_result_allowed == 0), phase193_test_result_allowed, 0, "hard"),
        ("phase149_receive_flow_phase193_promotion_closed", bool(phase193_promotion_allowed == 0), phase193_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase193_paper_live_closed", bool(phase193_paper_live_allowed == 0), phase193_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase194_fragility_decision_recorded", phase194_recorded, int(phase194_recorded), 1, "hard"),
        ("phase149_receive_flow_phase194_test_replay_closed", bool(phase194_test_replay_allowed == 0), phase194_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase194_promotion_closed", bool(phase194_promotion_allowed == 0), phase194_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase194_paper_live_closed", bool(phase194_paper_live_allowed == 0), phase194_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase195_redesign_search_recorded", phase195_recorded, int(phase195_recorded), 1, "hard"),
        ("phase149_receive_flow_phase195_test_replay_closed", bool(phase195_test_replay_allowed == 0), phase195_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase195_promotion_closed", bool(phase195_promotion_allowed == 0), phase195_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase195_paper_live_closed", bool(phase195_paper_live_allowed == 0), phase195_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase196_expanded_model_search_recorded", phase196_recorded, int(phase196_recorded), 1, "hard"),
        ("phase149_receive_flow_phase196_test_replay_closed", bool(phase196_test_replay_allowed == 0), phase196_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase196_promotion_closed", bool(phase196_promotion_allowed == 0), phase196_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase196_paper_live_closed", bool(phase196_paper_live_allowed == 0), phase196_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_non_receive_flow_feature_precommit_recorded", phase197_recorded, int(phase197_recorded), 1, "hard"),
        ("phase149_receive_flow_phase197_strategy_replay_closed", bool(phase197_strategy_replay_allowed == 0), phase197_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_test_replay_closed", bool(phase197_test_replay_allowed == 0), phase197_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_promotion_closed", bool(phase197_promotion_allowed == 0), phase197_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_paper_live_closed", bool(phase197_paper_live_allowed == 0), phase197_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase198_context_model_search_recorded", phase198_recorded, int(phase198_recorded), 1, "hard"),
        ("phase149_receive_flow_phase198_test_replay_closed", bool(phase198_test_replay_allowed == 0), phase198_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase198_promotion_closed", bool(phase198_promotion_allowed == 0), phase198_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase198_paper_live_closed", bool(phase198_paper_live_allowed == 0), phase198_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_branch_decision_recorded", phase199_recorded, int(phase199_recorded), 1, "hard"),
        ("phase149_receive_flow_phase199_strategy_replay_closed", bool(phase199_strategy_replay_allowed == 0), phase199_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_test_precommit_closed", bool(phase199_precommit_allowed == 0), phase199_precommit_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_test_replay_closed", bool(phase199_test_replay_allowed == 0), phase199_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_promotion_closed", bool(phase199_promotion_allowed == 0), phase199_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_paper_live_closed", bool(phase199_paper_live_allowed == 0), phase199_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_material_hypothesis_precommit_recorded", phase200_recorded, int(phase200_recorded), 1, "hard"),
        ("phase149_receive_flow_phase200_strategy_replay_closed", bool(phase200_strategy_replay_allowed == 0), phase200_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_test_replay_closed", bool(phase200_test_replay_allowed == 0), phase200_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_promotion_closed", bool(phase200_promotion_allowed == 0), phase200_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_paper_live_closed", bool(phase200_paper_live_allowed == 0), phase200_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_stage01_label_expansion_recorded", phase201_recorded, int(phase201_recorded), 1, "hard"),
        ("phase149_receive_flow_phase201_strategy_replay_closed", bool(phase201_strategy_replay_allowed == 0), phase201_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_test_replay_closed", bool(phase201_test_replay_allowed == 0), phase201_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_promotion_closed", bool(phase201_promotion_allowed == 0), phase201_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_paper_live_closed", bool(phase201_paper_live_allowed == 0), phase201_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_passive_feature_redesign_recorded", phase202_recorded, int(phase202_recorded), 1, "hard"),
        ("phase149_receive_flow_phase202_strategy_replay_closed", bool(phase202_strategy_replay_allowed == 0), phase202_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_test_replay_closed", bool(phase202_test_replay_allowed == 0), phase202_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_promotion_closed", bool(phase202_promotion_allowed == 0), phase202_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_paper_live_closed", bool(phase202_paper_live_allowed == 0), phase202_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_redesigned_label_materialization_recorded", phase203_recorded, int(phase203_recorded), 1, "hard"),
        ("phase149_receive_flow_phase203_strategy_replay_closed", bool(phase203_strategy_replay_allowed == 0), phase203_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_test_replay_closed", bool(phase203_test_replay_allowed == 0), phase203_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_promotion_closed", bool(phase203_promotion_allowed == 0), phase203_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_paper_live_closed", bool(phase203_paper_live_allowed == 0), phase203_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_passive_redesign_closure_recorded", phase204_recorded, int(phase204_recorded), 1, "hard"),
        ("phase149_receive_flow_phase204_strategy_replay_closed", bool(phase204_strategy_replay_allowed == 0), phase204_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_test_replay_closed", bool(phase204_test_replay_allowed == 0), phase204_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_promotion_closed", bool(phase204_promotion_allowed == 0), phase204_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_paper_live_closed", bool(phase204_paper_live_allowed == 0), phase204_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_material_new_source_precommit_recorded", phase205_recorded, int(phase205_recorded), 1, "hard"),
        ("phase149_receive_flow_phase205_strategy_replay_closed", bool(phase205_strategy_replay_allowed == 0), phase205_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_test_replay_closed", bool(phase205_test_replay_allowed == 0), phase205_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_promotion_closed", bool(phase205_promotion_allowed == 0), phase205_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_paper_live_closed", bool(phase205_paper_live_allowed == 0), phase205_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_nonoverlap_feature_contract_recorded", phase206_recorded, int(phase206_recorded), 1, "hard"),
        ("phase149_receive_flow_phase206_model_fit_closed", bool(phase206_model_fit_allowed == 0), phase206_model_fit_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_strategy_replay_closed", bool(phase206_strategy_replay_allowed == 0), phase206_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_test_replay_closed", bool(phase206_test_replay_allowed == 0), phase206_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_promotion_closed", bool(phase206_promotion_allowed == 0), phase206_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_paper_live_closed", bool(phase206_paper_live_allowed == 0), phase206_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_allowed_feature_matrix_recorded", phase207_recorded, int(phase207_recorded), 1, "hard"),
        ("phase149_receive_flow_phase207_model_fit_closed", bool(phase207_model_fit_allowed == 0), phase207_model_fit_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_strategy_replay_closed", bool(phase207_strategy_replay_allowed == 0), phase207_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_test_replay_closed", bool(phase207_test_replay_allowed == 0), phase207_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_promotion_closed", bool(phase207_promotion_allowed == 0), phase207_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_paper_live_closed", bool(phase207_paper_live_allowed == 0), phase207_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase208_feature_matrix_quality_gate_recorded", phase208_recorded, int(phase208_recorded), 1, "hard"),
        ("phase149_receive_flow_phase208_model_fit_closed", bool(phase208_model_fit_allowed == 0), phase208_model_fit_allowed, 0, "hard"),
        ("phase149_receive_flow_phase208_strategy_replay_closed", bool(phase208_strategy_replay_allowed == 0), phase208_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase208_test_replay_closed", bool(phase208_test_replay_allowed == 0), phase208_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase208_promotion_closed", bool(phase208_promotion_allowed == 0), phase208_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase208_paper_live_closed", bool(phase208_paper_live_allowed == 0), phase208_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase209_model_fit_precommit_spec_recorded", phase209_recorded, int(phase209_recorded), 1, "hard"),
        ("phase149_receive_flow_phase209_model_fit_execution_closed", bool(phase209_model_fit_execution_allowed == 0), phase209_model_fit_execution_allowed, 0, "hard"),
        ("phase149_receive_flow_phase209_strategy_replay_closed", bool(phase209_strategy_replay_allowed == 0), phase209_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase209_test_replay_closed", bool(phase209_test_replay_allowed == 0), phase209_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase209_promotion_closed", bool(phase209_promotion_allowed == 0), phase209_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase209_paper_live_closed", bool(phase209_paper_live_allowed == 0), phase209_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase210_train_validation_model_fit_recorded", phase210_recorded, int(phase210_recorded), 1, "hard"),
        ("phase149_receive_flow_phase210_model_fit_executed", bool(phase210_model_fit_execution == 1), phase210_model_fit_execution, 1, "hard"),
        ("phase149_receive_flow_phase210_test_rows_closed", bool(phase210_test_rows_used == 0), phase210_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase210_strategy_replay_closed", bool(phase210_strategy_replay_allowed == 0), phase210_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase210_test_replay_closed", bool(phase210_test_replay_allowed == 0), phase210_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase210_promotion_closed", bool(phase210_promotion_allowed == 0), phase210_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase210_paper_live_closed", bool(phase210_paper_live_allowed == 0), phase210_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase210_profitability_claim_closed", bool(phase210_profitability_claim_allowed == 0), phase210_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase211_validation_interpretation_recorded", phase211_recorded, int(phase211_recorded), 1, "hard"),
        ("phase149_receive_flow_phase211_candidate_replay_closed", bool(phase211_candidate_opened_for_replay == 0), phase211_candidate_opened_for_replay, 0, "hard"),
        ("phase149_receive_flow_phase211_strategy_replay_closed", bool(phase211_strategy_replay_allowed == 0), phase211_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase211_test_replay_closed", bool(phase211_test_replay_allowed == 0), phase211_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase211_promotion_closed", bool(phase211_promotion_allowed == 0), phase211_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase211_paper_live_closed", bool(phase211_paper_live_allowed == 0), phase211_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase211_profitability_claim_closed", bool(phase211_profitability_claim_allowed == 0), phase211_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase212_closure_redesign_recorded", phase212_recorded, int(phase212_recorded), 1, "hard"),
        ("phase149_receive_flow_phase212_candidate_replay_closed", bool(phase212_candidate_opened_for_replay == 0), phase212_candidate_opened_for_replay, 0, "hard"),
        ("phase149_receive_flow_phase212_model_fit_closed", bool(phase212_model_fit_allowed_next == 0), phase212_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase212_strategy_replay_closed", bool(phase212_strategy_replay_allowed == 0), phase212_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase212_test_replay_closed", bool(phase212_test_replay_allowed == 0), phase212_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase212_promotion_closed", bool(phase212_promotion_allowed == 0), phase212_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase212_paper_live_closed", bool(phase212_paper_live_allowed == 0), phase212_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase212_profitability_claim_closed", bool(phase212_profitability_claim_allowed == 0), phase212_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase213_material_source_recorded", phase213_recorded, int(phase213_recorded), 1, "hard"),
        ("phase149_receive_flow_phase213_model_fit_closed", bool(phase213_model_fit_allowed_next == 0), phase213_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase213_strategy_replay_closed", bool(phase213_strategy_replay_allowed == 0), phase213_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase213_test_replay_closed", bool(phase213_test_replay_allowed == 0), phase213_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase213_promotion_closed", bool(phase213_promotion_allowed == 0), phase213_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase213_paper_live_closed", bool(phase213_paper_live_allowed == 0), phase213_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase213_profitability_claim_closed", bool(phase213_profitability_claim_allowed == 0), phase213_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase214_label_materialization_recorded", phase214_recorded, int(phase214_recorded), 1, "hard"),
        ("phase149_receive_flow_phase214_model_fit_closed", bool(phase214_model_fit_allowed_next == 0), phase214_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase214_sealed_test_rows_closed", bool(phase214_sealed_test_rows_used == 0), phase214_sealed_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase214_strategy_replay_closed", bool(phase214_strategy_replay_allowed == 0), phase214_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase214_test_replay_closed", bool(phase214_test_replay_allowed == 0), phase214_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase214_promotion_closed", bool(phase214_promotion_allowed == 0), phase214_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase214_paper_live_closed", bool(phase214_paper_live_allowed == 0), phase214_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase214_profitability_claim_closed", bool(phase214_profitability_claim_allowed == 0), phase214_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase215_label_quality_interpretation_recorded", phase215_recorded, int(phase215_recorded), 1, "hard"),
        ("phase149_receive_flow_phase215_model_fit_closed", bool(phase215_model_fit_allowed_next == 0), phase215_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase215_strategy_replay_closed", bool(phase215_strategy_replay_allowed == 0), phase215_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase215_test_replay_closed", bool(phase215_test_replay_allowed == 0), phase215_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase215_promotion_closed", bool(phase215_promotion_allowed == 0), phase215_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase215_paper_live_closed", bool(phase215_paper_live_allowed == 0), phase215_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase215_profitability_claim_closed", bool(phase215_profitability_claim_allowed == 0), phase215_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase216_event_only_target_precommit_recorded", phase216_recorded, int(phase216_recorded), 1, "hard"),
        ("phase149_receive_flow_phase216_model_fit_closed", bool(phase216_model_fit_allowed_next == 0), phase216_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase216_strategy_replay_closed", bool(phase216_strategy_replay_allowed == 0), phase216_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase216_test_replay_closed", bool(phase216_test_replay_allowed == 0), phase216_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase216_promotion_closed", bool(phase216_promotion_allowed == 0), phase216_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase216_paper_live_closed", bool(phase216_paper_live_allowed == 0), phase216_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase216_profitability_claim_closed", bool(phase216_profitability_claim_allowed == 0), phase216_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase217_design_matrix_precommit_recorded", phase217_recorded, int(phase217_recorded), 1, "hard"),
        ("phase149_receive_flow_phase217_row_level_export_closed", bool(phase217_row_level_export_allowed == 0), phase217_row_level_export_allowed, 0, "hard"),
        ("phase149_receive_flow_phase217_model_fit_closed", bool(phase217_model_fit_allowed_next == 0), phase217_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase217_strategy_replay_closed", bool(phase217_strategy_replay_allowed == 0), phase217_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase217_test_replay_closed", bool(phase217_test_replay_allowed == 0), phase217_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase217_promotion_closed", bool(phase217_promotion_allowed == 0), phase217_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase217_paper_live_closed", bool(phase217_paper_live_allowed == 0), phase217_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase217_profitability_claim_closed", bool(phase217_profitability_claim_allowed == 0), phase217_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase218_model_fit_precommit_recorded", phase218_recorded, int(phase218_recorded), 1, "hard"),
        ("phase149_receive_flow_phase218_phase219_fit_dry_run_precommitted", bool(phase218_dry_run_precommitted == 1), phase218_dry_run_precommitted, 1, "hard"),
        ("phase149_receive_flow_phase218_model_fit_execution_closed", bool(phase218_model_fit_execution_allowed == 0), phase218_model_fit_execution_allowed, 0, "hard"),
        ("phase149_receive_flow_phase218_strategy_replay_closed", bool(phase218_strategy_replay_allowed == 0), phase218_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase218_test_replay_closed", bool(phase218_test_replay_allowed == 0), phase218_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase218_promotion_closed", bool(phase218_promotion_allowed == 0), phase218_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase218_paper_live_closed", bool(phase218_paper_live_allowed == 0), phase218_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase218_profitability_claim_closed", bool(phase218_profitability_claim_allowed == 0), phase218_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase219_model_fit_dry_run_recorded", phase219_recorded, int(phase219_recorded), 1, "hard"),
        ("phase149_receive_flow_phase219_model_fit_execution_recorded", bool(phase219_model_fit_execution == 1), phase219_model_fit_execution, 1, "hard"),
        ("phase149_receive_flow_phase219_strategy_replay_closed", bool(phase219_strategy_replay_allowed == 0), phase219_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase219_test_replay_closed", bool(phase219_test_replay_allowed == 0), phase219_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase219_test_rows_closed", bool(phase219_test_rows_used == 0), phase219_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase219_promotion_closed", bool(phase219_promotion_allowed == 0), phase219_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase219_paper_live_closed", bool(phase219_paper_live_allowed == 0), phase219_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase219_profitability_claim_closed", bool(phase219_profitability_claim_allowed == 0), phase219_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase220_validation_interpretation_recorded", phase220_recorded, int(phase220_recorded), 1, "hard"),
        ("phase149_receive_flow_phase220_phase221_candidate_opened", bool(phase220_candidate_opened == 1), phase220_candidate_opened, 1, "hard"),
        ("phase149_receive_flow_phase220_strategy_replay_closed", bool(phase220_strategy_replay_allowed == 0), phase220_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase220_test_replay_closed", bool(phase220_test_replay_allowed == 0), phase220_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase220_promotion_closed", bool(phase220_promotion_allowed == 0), phase220_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase220_paper_live_closed", bool(phase220_paper_live_allowed == 0), phase220_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase220_profitability_claim_closed", bool(phase220_profitability_claim_allowed == 0), phase220_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase221_signal_replay_precommit_recorded", phase221_recorded, int(phase221_recorded), 1, "hard"),
        ("phase149_receive_flow_phase221_phase222_replay_dry_run_precommitted", bool(phase221_phase222_replay_precommitted == 1), phase221_phase222_replay_precommitted, 1, "hard"),
        ("phase149_receive_flow_phase221_replay_execution_closed", bool(phase221_replay_execution_allowed == 0), phase221_replay_execution_allowed, 0, "hard"),
        ("phase149_receive_flow_phase221_next_replay_scope_opened", bool(phase221_strategy_replay_allowed_next == 1), phase221_strategy_replay_allowed_next, 1, "hard"),
        ("phase149_receive_flow_phase221_test_replay_closed", bool(phase221_test_replay_allowed == 0), phase221_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase221_promotion_closed", bool(phase221_promotion_allowed == 0), phase221_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase221_paper_live_closed", bool(phase221_paper_live_allowed == 0), phase221_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase221_profitability_claim_closed", bool(phase221_profitability_claim_allowed == 0), phase221_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase222_signal_replay_dry_run_recorded", phase222_recorded, int(phase222_recorded), 1, "hard"),
        ("phase149_receive_flow_phase222_strategy_replay_execution_recorded", bool(phase222_strategy_replay_execution == 1), phase222_strategy_replay_execution, 1, "hard"),
        ("phase149_receive_flow_phase222_test_replay_closed", bool(phase222_test_replay_allowed == 0), phase222_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase222_test_rows_closed", bool(phase222_test_rows_used == 0), phase222_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase222_promotion_closed", bool(phase222_promotion_allowed == 0), phase222_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase222_paper_live_closed", bool(phase222_paper_live_allowed == 0), phase222_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase222_profitability_claim_closed", bool(phase222_profitability_claim_allowed == 0), phase222_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase223_validation_interpretation_recorded", phase223_recorded, int(phase223_recorded), 1, "hard"),
        ("phase149_receive_flow_phase223_no_passing_interpretation_rows", bool(phase223_passing_interpretation_rows == 0), phase223_passing_interpretation_rows, 0, "hard"),
        ("phase149_receive_flow_phase223_phase224_work_order_recorded", bool(phase223_phase224_work_order_rows == 1), phase223_phase224_work_order_rows, 1, "hard"),
        ("phase149_receive_flow_phase223_broader_replay_closed", bool(phase223_broader_replay_allowed_next == 0), phase223_broader_replay_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase223_test_replay_closed", bool(phase223_test_replay_allowed == 0), phase223_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase223_test_rows_closed", bool(phase223_test_rows_used == 0), phase223_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase223_promotion_closed", bool(phase223_promotion_allowed == 0), phase223_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase223_paper_live_closed", bool(phase223_paper_live_allowed == 0), phase223_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase223_profitability_claim_closed", bool(phase223_profitability_claim_allowed == 0), phase223_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase224_closure_or_redesign_recorded", phase224_recorded, int(phase224_recorded), 1, "hard"),
        ("phase149_receive_flow_phase224_candidate_set_closed_for_broader", bool(phase224_closed_broader == 1), phase224_closed_broader, 1, "hard"),
        ("phase149_receive_flow_phase224_candidate_set_closed_for_test", bool(phase224_closed_test == 1), phase224_closed_test, 1, "hard"),
        ("phase149_receive_flow_phase224_reuse_without_redesign_closed", bool(phase224_reuse_without_redesign == 0), phase224_reuse_without_redesign, 0, "hard"),
        ("phase149_receive_flow_phase224_phase225_work_order_recorded", bool(phase224_phase225_work_order_rows == 1), phase224_phase225_work_order_rows, 1, "hard"),
        ("phase149_receive_flow_phase224_model_fit_closed", bool(phase224_model_fit_allowed_next == 0), phase224_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase224_strategy_replay_closed", bool(phase224_strategy_replay_allowed == 0), phase224_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase224_broader_replay_closed", bool(phase224_broader_replay_allowed_next == 0), phase224_broader_replay_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase224_test_replay_closed", bool(phase224_test_replay_allowed == 0), phase224_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase224_promotion_closed", bool(phase224_promotion_allowed == 0), phase224_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase224_paper_live_closed", bool(phase224_paper_live_allowed == 0), phase224_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase224_profitability_claim_closed", bool(phase224_profitability_claim_allowed == 0), phase224_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase225_cost_aware_redesign_precommit_recorded", phase225_recorded, int(phase225_recorded), 1, "hard"),
        ("phase149_receive_flow_phase225_label_materialization_next_opened", bool(phase225_label_materialization_allowed_next == 1), phase225_label_materialization_allowed_next, 1, "hard"),
        ("phase149_receive_flow_phase225_phase226_work_order_recorded", bool(phase225_phase226_work_order_rows == 1), phase225_phase226_work_order_rows, 1, "hard"),
        ("phase149_receive_flow_phase225_model_fit_closed", bool(phase225_model_fit_allowed_next == 0), phase225_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase225_strategy_replay_closed", bool(phase225_strategy_replay_allowed == 0), phase225_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase225_broader_replay_closed", bool(phase225_broader_replay_allowed_next == 0), phase225_broader_replay_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase225_test_replay_closed", bool(phase225_test_replay_allowed == 0), phase225_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase225_test_rows_closed", bool(phase225_test_rows_used == 0), phase225_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase225_promotion_closed", bool(phase225_promotion_allowed == 0), phase225_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase225_paper_live_closed", bool(phase225_paper_live_allowed == 0), phase225_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase225_profitability_claim_closed", bool(phase225_profitability_claim_allowed == 0), phase225_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase226_label_materialization_recorded", phase226_recorded, int(phase226_recorded), 1, "hard"),
        ("phase149_receive_flow_phase226_available_horizons_materialized", bool(phase226_materialized_horizons == 2), phase226_materialized_horizons, 2, "hard"),
        ("phase149_receive_flow_phase226_actionable_rows_recorded", bool(phase226_actionable_rows > 0), phase226_actionable_rows, ">0", "hard"),
        ("phase149_receive_flow_phase226_quality_failure_recorded", bool(phase226_quality_pass_rows == 0), phase226_quality_pass_rows, 0, "hard"),
        ("phase149_receive_flow_phase226_model_fit_closed", bool(phase226_model_fit_allowed_next == 0), phase226_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase226_strategy_replay_closed", bool(phase226_strategy_replay_allowed == 0), phase226_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase226_broader_replay_closed", bool(phase226_broader_replay_allowed_next == 0), phase226_broader_replay_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase226_test_replay_closed", bool(phase226_test_replay_allowed == 0), phase226_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase226_test_rows_closed", bool(phase226_test_rows_used == 0), phase226_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase226_promotion_closed", bool(phase226_promotion_allowed == 0), phase226_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase226_paper_live_closed", bool(phase226_paper_live_allowed == 0), phase226_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase226_profitability_claim_closed", bool(phase226_profitability_claim_allowed == 0), phase226_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase227_label_quality_interpretation_recorded", phase227_recorded, int(phase227_recorded), 1, "hard"),
        ("phase149_receive_flow_phase227_no_fit_precommit_candidates", bool(phase227_fit_precommit_candidate_rows == 0), phase227_fit_precommit_candidate_rows, 0, "hard"),
        ("phase149_receive_flow_phase227_phase228_work_order_recorded", bool(phase227_phase228_work_order_rows == 1), phase227_phase228_work_order_rows, 1, "hard"),
        ("phase149_receive_flow_phase227_model_fit_closed", bool(phase227_model_fit_allowed_next == 0), phase227_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase227_strategy_replay_closed", bool(phase227_strategy_replay_allowed == 0), phase227_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase227_broader_replay_closed", bool(phase227_broader_replay_allowed_next == 0), phase227_broader_replay_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase227_test_replay_closed", bool(phase227_test_replay_allowed == 0), phase227_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase227_test_rows_closed", bool(phase227_test_rows_used == 0), phase227_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase227_promotion_closed", bool(phase227_promotion_allowed == 0), phase227_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase227_paper_live_closed", bool(phase227_paper_live_allowed == 0), phase227_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase227_profitability_claim_closed", bool(phase227_profitability_claim_allowed == 0), phase227_profitability_claim_allowed, 0, "hard"),
        ("phase149_receive_flow_phase228_closure_or_relaxation_recorded", phase228_recorded, int(phase228_recorded), 1, "hard"),
        ("phase149_receive_flow_phase228_current_label_set_closed_for_fit", bool(phase228_closed_fit == 1), phase228_closed_fit, 1, "hard"),
        ("phase149_receive_flow_phase228_current_label_set_closed_for_replay", bool(phase228_closed_replay == 1), phase228_closed_replay, 1, "hard"),
        ("phase149_receive_flow_phase228_phase229_work_order_recorded", bool(phase228_phase229_work_order_rows == 1), phase228_phase229_work_order_rows, 1, "hard"),
        ("phase149_receive_flow_phase228_label_materialization_closed", bool(phase228_label_materialization_allowed_next == 0), phase228_label_materialization_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase228_threshold_widening_closed", bool(phase228_threshold_widening_allowed == 0), phase228_threshold_widening_allowed, 0, "hard"),
        ("phase149_receive_flow_phase228_model_fit_closed", bool(phase228_model_fit_allowed_next == 0), phase228_model_fit_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase228_strategy_replay_closed", bool(phase228_strategy_replay_allowed == 0), phase228_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase228_broader_replay_closed", bool(phase228_broader_replay_allowed_next == 0), phase228_broader_replay_allowed_next, 0, "hard"),
        ("phase149_receive_flow_phase228_test_replay_closed", bool(phase228_test_replay_allowed == 0), phase228_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase228_test_rows_closed", bool(phase228_test_rows_used == 0), phase228_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_phase228_promotion_closed", bool(phase228_promotion_allowed == 0), phase228_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase228_paper_live_closed", bool(phase228_paper_live_allowed == 0), phase228_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase228_profitability_claim_closed", bool(phase228_profitability_claim_allowed == 0), phase228_profitability_claim_allowed, 0, "hard"),
        ("phase149_deep_book_branch_closed", branch_closed, int(branch_closed), 1, "hard"),
        ("phase149_no_promoted_strategy_replay", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate", "pass", "observed", "required", "severity"])


def summarize(phase_ledger: pd.DataFrame, branch_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    outputs_with_acceptance = int(phase_ledger["has_acceptance_summary"].astype(bool).sum()) if not phase_ledger.empty else 0
    script_phases = int(phase_ledger["has_runner"].astype(bool).sum()) if not phase_ledger.empty else 0
    receive_rows = branch_summary.loc[branch_summary["branch"].astype(str).eq("real_receive_flow_source"), "current_next_action"] if not branch_summary.empty else pd.Series(dtype=str)
    next_action = receive_rows.iloc[0] if not receive_rows.empty else "inspect_phase149_branch_status_summary"
    return pd.DataFrame(
        [
            ("phase149_phase_rows", int(len(phase_ledger)), "Phase rows discovered from scripts and outputs"),
            ("phase149_runner_phase_rows", script_phases, "Phase rows with at least one runner"),
            ("phase149_acceptance_phase_rows", outputs_with_acceptance, "Phase rows with acceptance summaries"),
            ("phase149_branch_rows", int(len(branch_summary)), "Current research branches summarized"),
            ("phase149_hard_gate_rows", int(len(hard)), "Hard global-state gates evaluated"),
            ("phase149_hard_gate_pass_rows", int(hard["pass"].astype(bool).sum()) if not hard.empty else 0, "Hard global-state gates passed"),
            ("phase149_strategy_replay_allowed", 0, "Phase149 never unlocks strategy replay"),
            ("phase149_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase149 Research State Auditor",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase149 reconciles current phase scripts, output evidence, branch states, and replay gates.",
        "It does not run strategies, contact Azure, import data, or unlock replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase149_research_state_auditor_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase149(output_dir: Path, base_dir: Path, scripts_root: Path, outputs_root: Path, plan_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    scripts = discover_script_phases(scripts_root)
    outputs = discover_output_phases(outputs_root)
    phase_ledger = build_phase_ledger(scripts, outputs)
    branch_summary = build_branch_summary(phase_ledger)
    gates = build_global_gates(phase_ledger)
    acceptance = summarize(phase_ledger, branch_summary, gates)

    scripts.to_csv(output_dir / "phase149_script_phase_inventory.csv", index=False)
    outputs.to_csv(output_dir / "phase149_output_phase_inventory.csv", index=False)
    phase_ledger.to_csv(output_dir / "phase149_phase_status_ledger.csv", index=False)
    branch_summary.to_csv(output_dir / "phase149_branch_status_summary.csv", index=False)
    gates.to_csv(output_dir / "phase149_global_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase149_research_state_auditor_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Branch Status Summary": branch_summary,
            "Global Gate Evaluation": gates,
            "Phase Status Ledger": phase_ledger.tail(80),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase149_research_state_auditor",
        **reproducibility_fields(
            artifact_id="phase149",
            generated_utc=generated_utc,
            inputs={
                "scripts_root": str(scripts_root),
                "outputs_root": str(outputs_root),
                "plan_path": str(plan_path),
            },
            parameters={
                "policy": "read_only_research_state_reconciliation",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "script_phase_inventory": str(output_dir / "phase149_script_phase_inventory.csv"),
                "output_phase_inventory": str(output_dir / "phase149_output_phase_inventory.csv"),
                "phase_status_ledger": str(output_dir / "phase149_phase_status_ledger.csv"),
                "branch_status_summary": str(output_dir / "phase149_branch_status_summary.csv"),
                "global_gate_evaluation": str(output_dir / "phase149_global_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase149_research_state_auditor_acceptance_summary.csv"),
                "report": str(output_dir / "phase149_research_state_auditor_report.md"),
                "manifest": str(output_dir / "phase149_research_state_auditor_manifest.json"),
            },
            random_seed="none_deterministic_state_audit",
            scenario_ids="phase149_research_state_auditor",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase149_research_state_auditor_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit current research phase state and gates.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--scripts-root", type=Path, default=DEFAULT_SCRIPTS_ROOT)
    parser.add_argument("--outputs-root", type=Path, default=DEFAULT_OUTPUTS_ROOT)
    parser.add_argument("--plan-path", type=Path, default=DEFAULT_PLAN_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase149(args.output_dir, args.base_dir, args.scripts_root, args.outputs_root, args.plan_path)

if __name__ == "__main__":
    main()
