from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _status_class(value: object) -> str:
    text = str(value).lower()
    if text in {"pass", "available", "computed_proxy", "sample_proxy", "proxy_available", "implemented", "implemented_proxy"}:
        return "ok"
    if text in {"warn", "partial_current", "partial_proxy"}:
        return "warn"
    if text in {"fail", "blocked", "missing", "not_supported_by_current_product"}:
        return "bad"
    return "neutral"


def _table(frame: pd.DataFrame, columns: list[str] | None = None, max_rows: int = 20) -> str:
    if frame.empty:
        return "<p class='muted'>No rows.</p>"
    data = frame.copy()
    if columns is not None:
        data = data[[column for column in columns if column in data.columns]]
    data = data.head(max_rows)
    header = "".join(f"<th>{html.escape(str(column))}</th>" for column in data.columns)
    rows = []
    for record in data.to_dict("records"):
        cells = []
        for column in data.columns:
            value = record[column]
            text = "" if pd.isna(value) else str(value)
            cls = _status_class(value) if column in {"status", "current_status", "gate_status", "implementation_status", "priority", "acceptance_status"} else ""
            cells.append(f"<td class='{cls}'>{html.escape(text)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table><thead><tr>" + header + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def _metric_card(label: str, value: object, note: str = "") -> str:
    return (
        "<div class='card'>"
        f"<div class='card-label'>{html.escape(label)}</div>"
        f"<div class='card-value'>{html.escape(str(value))}</div>"
        f"<div class='card-note'>{html.escape(note)}</div>"
        "</div>"
    )


def _bar_rows(frame: pd.DataFrame, label_col: str, value_col: str) -> str:
    if frame.empty:
        return "<p class='muted'>No rows.</p>"
    max_value = max(float(frame[value_col].max()), 1.0)
    rows = []
    for record in frame.to_dict("records"):
        label = str(record[label_col])
        value = float(record[value_col])
        width = max(2.0, 100.0 * value / max_value)
        rows.append(
            "<div class='bar-row'>"
            f"<div class='bar-label'>{html.escape(label)}</div>"
            f"<div class='bar-track'><div class='bar-fill' style='width:{width:.2f}%'></div></div>"
            f"<div class='bar-value'>{value:.0f}</div>"
            "</div>"
        )
    return "".join(rows)


def build_dashboard(paths: dict[str, Path]) -> tuple[str, str, pd.DataFrame, dict]:
    quality = _read_csv(paths["quality"])
    holdout = _read_csv(paths["holdout"])
    lifecycle_risk = _read_csv(paths["lifecycle_risk"])
    robustness_dimension = _read_csv(paths["robustness_dimension"])
    acceptance = _read_csv(paths["acceptance"])
    blockers = _read_csv(paths["blockers"])
    metric_catalog = _read_csv(paths["metric_catalog"])
    predictive = _read_csv(paths["predictive"])
    trading = _read_csv(paths["trading"])
    markout = _read_csv(paths["markout"])
    gaps = _read_csv(paths["gaps"])

    quality_status = quality["status"].value_counts().rename_axis("status").reset_index(name="checks")
    gate_blockers = blockers["gate_id"].value_counts().rename_axis("gate_id").reset_index(name="blockers").sort_values("gate_id")
    metric_status = metric_catalog.groupby(["metric_category", "current_status"], sort=True).size().reset_index(name="metrics")
    gap_priority = gaps["priority"].value_counts().rename_axis("priority").reset_index(name="gaps").sort_values("priority")
    top_predictive = predictive.sort_values("balanced_accuracy_proxy", ascending=False)
    top_trading = trading.sort_values("mean_net_return", ascending=False)
    top_markout = markout.sort_values("adverse_selection_rate_6bar_proxy", ascending=True)
    lifecycle_overview = (
        lifecycle_risk.groupby("fill_model", sort=True)
        .agg(
            strategy_profiles=("strategy_id", "size"),
            orders=("orders", "sum"),
            mean_fill_ratio=("mean_fill_ratio", "mean"),
            risk_adjusted_net_pnl_inr=("risk_adjusted_net_pnl_inr", "sum"),
            daily_halt_rows=("daily_halt_rows", "sum"),
            position_limit_breach_rows=("position_limit_breach_rows", "sum"),
        )
        .reset_index()
    )
    robustness_status = robustness_dimension["dimension_status"].value_counts().rename_axis("dimension_status").reset_index(name="strategies")

    summary_rows = [
        ("quality_checks", int(len(quality)), "Phase 14 quality rows"),
        ("quality_warn_checks", int((quality["status"].astype(str) == "warn").sum()), "Current quality warnings"),
        ("quality_fail_checks", int((quality["status"].astype(str) == "fail").sum()), "Current quality failures"),
        ("holdout_proxy_rows", int(len(holdout)), "Phase 14 holdout generator proxy rows"),
        ("holdout_proxy_available_rows", int((holdout["realism_status"].astype(str) == "holdout_proxy_available_not_acceptance").sum()), "Holdout proxy rows structurally available"),
        ("full_run_lifecycle_risk_rows", int(len(lifecycle_risk)), "Phase 12 full-run fill-adjusted risk rows"),
        ("full_run_lifecycle_fill_models", int(lifecycle_risk["fill_model"].nunique()), "Phase 12 full-run fill models"),
        ("full_run_lifecycle_daily_halt_rows", int(lifecycle_risk["daily_halt_rows"].sum()), "Phase 12 full-run lifecycle halt rows"),
        ("robustness_dimension_rows", int(len(robustness_dimension)), "Phase 13 robustness dimension rows"),
        ("robustness_dimension_registered_rows", int(robustness_dimension["registered_for_phase13_proxy"].astype(bool).sum()), "Phase 13 registered robustness proxy rows"),
        ("strategies", int(acceptance["strategy_id"].nunique()), "Phase 15 strategies"),
        ("promoted_strategies", int(acceptance["promotion_allowed"].astype(bool).sum()), "Promotion allowed count"),
        ("acceptance_blockers", int(len(blockers)), "Phase 15 blocker rows"),
        ("metric_catalog_rows", int(len(metric_catalog)), "Phase 16 metric catalog rows"),
        ("acceptance_grade_metrics", int(metric_catalog["acceptance_eligible_now"].astype(bool).sum()), "Acceptance-grade metrics"),
        ("missing_metrics", int((metric_catalog["current_status"].astype(str) == "missing").sum()), "Missing metric rows"),
        ("p1_gaps", int((gaps["priority"].astype(str) == "P1").sum()), "Phase 17 P1 backlog rows"),
    ]
    summary = pd.DataFrame(summary_rows, columns=["metric", "value", "note"])
    inputs_manifest = {key: str(value) for key, value in paths.items()}
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "inputs": inputs_manifest,
        "summary": {row["metric"]: int(row["value"]) for row in summary.to_dict("records")},
        "scope": "static_validation_dashboard_not_promotion_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="dashboard",
            generated_utc=generated_utc,
            inputs=inputs_manifest,
            parameters={"scope": manifest["scope"], "summary_metrics": list(summary["metric"])},
            outputs={
                "html": "outputs/dashboard/synthetic_l2_validation_dashboard.html",
                "markdown": "outputs/dashboard/synthetic_l2_validation_dashboard.md",
                "summary": "outputs/dashboard/validation_dashboard_summary.csv",
                "manifest": "outputs/dashboard/validation_dashboard_manifest.json",
            },
            random_seed="not_applicable_deterministic_static_dashboard",
            scenario_ids="current_workspace_phase14_phase15_phase16_phase17_evidence",
            cost_model_version="outputs/phase12/cost_schedule.csv_and_zerodha_order_formula_v2_or_not_applicable",
            latency_model_version="outputs/phase12/execution_profiles.csv_or_phase8_feed_profiles_v1_or_not_applicable",
        )
    )

    cards = "".join(_metric_card(row["metric"], row["value"], row["note"]) for row in summary.to_dict("records"))
    css = """
    body { font-family: Inter, Segoe UI, Arial, sans-serif; margin: 24px; color: #172033; background: #f7f8fb; }
    h1, h2 { color: #111827; }
    .muted { color: #6b7280; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin: 18px 0; }
    .card { background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 14px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
    .card-label { color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }
    .card-value { color: #111827; font-size: 28px; font-weight: 700; margin-top: 4px; }
    .card-note { color: #6b7280; font-size: 12px; margin-top: 4px; }
    section { background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; margin: 16px 0; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { border-bottom: 1px solid #edf0f4; padding: 8px; text-align: left; vertical-align: top; }
    th { color: #374151; background: #f9fafb; }
    .ok { color: #047857; font-weight: 600; }
    .warn { color: #b45309; font-weight: 600; }
    .bad { color: #b91c1c; font-weight: 600; }
    .bar-row { display: grid; grid-template-columns: 150px 1fr 50px; gap: 10px; align-items: center; margin: 7px 0; }
    .bar-track { background: #eef2ff; height: 14px; border-radius: 999px; overflow: hidden; }
    .bar-fill { background: #4f46e5; height: 100%; border-radius: 999px; }
    .bar-label, .bar-value { font-size: 13px; color: #374151; }
    """
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>SyntheticL2 Validation Dashboard</title>
  <style>{css}</style>
</head>
<body>
  <h1>SyntheticL2 Validation Dashboard</h1>
  <p class="muted">Generated UTC: {html.escape(manifest['generated_utc'])}. Static dashboard for research traceability only; not promotion evidence.</p>
  <div class="cards">{cards}</div>
  <section><h2>Phase 14 Quality Status</h2>{_bar_rows(quality_status, 'status', 'checks')}{_table(quality, ['level', 'check_name', 'value', 'status', 'evidence'], 24)}</section>
  <section><h2>Phase 14 Holdout Generator Realism Proxy</h2>{_table(holdout, ['quarter_profile', 'feed_profile', 'holdout_role', 'scenario_days', 'symbols', 'regimes', 'realism_status', 'acceptance_eligible_now'], 20)}</section>
  <section><h2>Phase 13 Robustness Dimension Proxy</h2>{_table(robustness_status, None, 10)}{_table(robustness_dimension, ['strategy_id', 'registered_for_phase13_proxy', 'initial_engineering_seeds_run', 'required_full_validation_seeds', 'execution_profiles_evaluated', 'parameter_sets_run', 'parameter_sets_planned', 'walk_forward_status', 'holdout_status', 'dimension_status'], 14)}</section>
  <section><h2>Phase 12 Full-Run Lifecycle Risk Proxy</h2>{_table(lifecycle_overview, ['fill_model', 'strategy_profiles', 'orders', 'mean_fill_ratio', 'risk_adjusted_net_pnl_inr', 'daily_halt_rows', 'position_limit_breach_rows'], 10)}{_table(lifecycle_risk, ['strategy_id', 'execution_profile', 'fill_model', 'orders', 'mean_fill_ratio', 'risk_adjusted_net_pnl_inr', 'max_intraday_drawdown_inr', 'daily_halt_rows'], 18)}</section>
  <section><h2>Phase 15 Acceptance Blockers</h2>{_bar_rows(gate_blockers, 'gate_id', 'blockers')}{_table(acceptance, ['strategy_id', 'passed_gates', 'blocked_gates', 'promotion_allowed', 'acceptance_status', 'support_level'], 20)}</section>
  <section><h2>Phase 16 Metric Coverage</h2>{_table(metric_status, None, 20)}{_table(metric_catalog, ['metric_category', 'metric_name', 'current_status', 'acceptance_eligible_now', 'evidence_note'], 40)}</section>
  <section><h2>Top Predictive Proxy Diagnostics</h2>{_table(top_predictive, ['strategy_id', 'balanced_accuracy_proxy', 'precision_long_proxy', 'precision_short_proxy', 'rank_auc_proxy', 'incremental_r2_proxy'], 12)}</section>
  <section><h2>Top Trading Proxy Rows</h2>{_table(top_trading, ['strategy_id', 'execution_profile', 'trades', 'mean_net_return', 'win_rate_net', 'sample_max_drawdown_units', 'sample_profit_factor'], 15)}</section>
  <section><h2>Best Lower-Adverse-Selection Markout Rows</h2>{_table(top_markout, ['strategy_id', 'execution_profile', 'markout_sample_trades', 'adverse_selection_rate_6bar_proxy', 'mean_mae_proxy', 'mean_mfe_proxy'], 15)}</section>
  <section><h2>Phase 17 Gap Backlog</h2>{_bar_rows(gap_priority, 'priority', 'gaps')}{_table(gaps, ['priority', 'work_package_id', 'deliverable', 'implementation_status', 'evidence_status', 'recommended_next_action'], 40)}</section>
</body>
</html>"""

    md_lines = [
        "# SyntheticL2 Validation Dashboard Summary",
        "",
        f"Generated UTC: {manifest['generated_utc']}",
        "",
        "This dashboard is static research traceability output, not strategy promotion evidence.",
        "",
        "## Summary Metrics",
        "",
        _markdown_table(summary),
        "",
        "## Quality Status",
        "",
        _markdown_table(quality_status),
        "",
        "## Holdout Generator Realism Proxy",
        "",
        _markdown_table(holdout),
        "",
        "## Phase 12 Full-Run Lifecycle Risk Proxy",
        "",
        _markdown_table(lifecycle_overview),
        "",
        "## Phase 13 Robustness Dimension Proxy",
        "",
        _markdown_table(robustness_status),
        "",
        "## Acceptance Blockers by Gate",
        "",
        _markdown_table(gate_blockers),
        "",
        "## Metric Status",
        "",
        _markdown_table(metric_status),
        "",
        "## Gap Priority",
        "",
        _markdown_table(gap_priority),
        "",
    ]
    return html_doc, "\n".join(md_lines), summary, manifest


def run_dashboard(output_dir: Path, paths: dict[str, Path]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    html_doc, markdown_doc, summary, manifest = build_dashboard(paths)
    (output_dir / "synthetic_l2_validation_dashboard.html").write_text(html_doc, encoding="utf-8")
    (output_dir / "synthetic_l2_validation_dashboard.md").write_text(markdown_doc, encoding="utf-8")
    summary.to_csv(output_dir / "validation_dashboard_summary.csv", index=False)
    (output_dir / "validation_dashboard_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a static SyntheticL2 validation dashboard from Phase 14-17 outputs.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/dashboard"))
    parser.add_argument("--quality", type=Path, default=Path("outputs/phase14/quality_gate_summary.csv"))
    parser.add_argument("--holdout", type=Path, default=Path("outputs/phase14/holdout_generator_realism_summary.csv"))
    parser.add_argument("--lifecycle-risk", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_summary.csv"))
    parser.add_argument("--robustness-dimension", type=Path, default=Path("outputs/phase13/robustness_dimension_summary.csv"))
    parser.add_argument("--acceptance", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    parser.add_argument("--blockers", type=Path, default=Path("outputs/phase15/acceptance_blockers.csv"))
    parser.add_argument("--metric-catalog", type=Path, default=Path("outputs/phase16/metric_catalog.csv"))
    parser.add_argument("--predictive", type=Path, default=Path("outputs/phase16/predictive_proxy_diagnostics.csv"))
    parser.add_argument("--trading", type=Path, default=Path("outputs/phase16/trading_metric_scoreboard.csv"))
    parser.add_argument("--markout", type=Path, default=Path("outputs/phase16/markout_mae_mfe_summary.csv"))
    parser.add_argument("--gaps", type=Path, default=Path("outputs/phase17/implementation_gap_backlog.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "quality": args.quality,
        "holdout": args.holdout,
        "lifecycle_risk": args.lifecycle_risk,
        "robustness_dimension": args.robustness_dimension,
        "acceptance": args.acceptance,
        "blockers": args.blockers,
        "metric_catalog": args.metric_catalog,
        "predictive": args.predictive,
        "trading": args.trading,
        "markout": args.markout,
        "gaps": args.gaps,
    }
    run_dashboard(args.output_dir, paths)


if __name__ == "__main__":
    main()
