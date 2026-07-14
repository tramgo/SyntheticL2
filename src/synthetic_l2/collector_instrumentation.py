from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic_ns
from uuid import uuid4

import pandas as pd


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CollectorInstrumentation:
    """Small collector-side helper for Stage A2 Class B capture evidence.

    The live Zerodha collector should create one instance per websocket process,
    call ``open_session`` when a connection/subscription is established, call
    ``enrich_ticks`` inside every on_ticks callback before parquet persistence,
    record broker/session counters as they are observed, then call
    ``close_session`` and ``flush`` on shutdown/reconnect.
    """

    output_dir: Path
    collector_run_id: str = field(default_factory=lambda: f"collector_run_{uuid4().hex}")
    session_id: str | None = None
    local_sequence_id: int = 0
    callback_batch_id: int = 0
    session_rows: list[dict] = field(default_factory=list)
    sequence_rows: list[dict] = field(default_factory=list)
    drop_counter_rows: list[dict] = field(default_factory=list)

    def open_session(self, subscribed_symbols: list[str], exchange: str = "NSE", reason: str = "connect") -> str:
        self.session_id = f"{self.collector_run_id}_session_{len(self.session_rows) + 1:04d}"
        self.session_rows.append(
            {
                "collector_run_id": self.collector_run_id,
                "session_id": self.session_id,
                "exchange": exchange,
                "opened_utc": utc_now_iso(),
                "closed_utc": "",
                "open_reason": reason,
                "close_reason": "",
                "subscribed_symbols": ";".join(subscribed_symbols),
                "subscribed_symbol_count": len(subscribed_symbols),
                "first_local_sequence_id": self.local_sequence_id + 1,
                "last_local_sequence_id": "",
                "tick_rows": 0,
            }
        )
        return self.session_id

    def enrich_ticks(self, ticks: list[dict]) -> list[dict]:
        if self.session_id is None:
            raise RuntimeError("open_session must be called before enrich_ticks")
        self.callback_batch_id += 1
        callback_received_utc = utc_now_iso()
        callback_received_monotonic_ns = monotonic_ns()
        enriched = []
        for tick in ticks:
            self.local_sequence_id += 1
            row = dict(tick)
            row.update(
                {
                    "collector_run_id": self.collector_run_id,
                    "session_id": self.session_id,
                    "callback_batch_id": self.callback_batch_id,
                    "local_sequence_id": self.local_sequence_id,
                    "callback_received_utc": callback_received_utc,
                    "callback_received_monotonic_ns": callback_received_monotonic_ns,
                }
            )
            enriched.append(row)
            self.sequence_rows.append(
                {
                    "collector_run_id": self.collector_run_id,
                    "session_id": self.session_id,
                    "callback_batch_id": self.callback_batch_id,
                    "local_sequence_id": self.local_sequence_id,
                    "symbol": row.get("tradingsymbol") or row.get("requested_symbol") or row.get("symbol", ""),
                    "callback_received_utc": callback_received_utc,
                    "callback_received_monotonic_ns": callback_received_monotonic_ns,
                }
            )
        self.session_rows[-1]["tick_rows"] = int(self.session_rows[-1]["tick_rows"]) + len(enriched)
        self.session_rows[-1]["last_local_sequence_id"] = self.local_sequence_id
        return enriched

    def record_drop_counters(
        self,
        symbol: str,
        dropped_count: int = 0,
        duplicate_count: int = 0,
        stale_count: int = 0,
        out_of_order_count: int = 0,
        source: str = "collector_callback",
    ) -> None:
        if self.session_id is None:
            raise RuntimeError("open_session must be called before record_drop_counters")
        self.drop_counter_rows.append(
            {
                "collector_run_id": self.collector_run_id,
                "session_id": self.session_id,
                "symbol": symbol,
                "observed_utc": utc_now_iso(),
                "source": source,
                "dropped_count": int(dropped_count),
                "duplicate_count": int(duplicate_count),
                "stale_count": int(stale_count),
                "out_of_order_count": int(out_of_order_count),
            }
        )

    def close_session(self, reason: str = "normal_close") -> None:
        if self.session_id is None:
            return
        self.session_rows[-1]["closed_utc"] = utc_now_iso()
        self.session_rows[-1]["close_reason"] = reason
        self.session_id = None

    def frames(self) -> dict[str, pd.DataFrame]:
        return {
            "session_ledger": pd.DataFrame(self.session_rows),
            "tick_sequence_diagnostics": pd.DataFrame(self.sequence_rows),
            "drop_counter_ledger": pd.DataFrame(self.drop_counter_rows),
        }

    def flush(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for name, frame in self.frames().items():
            frame.to_csv(self.output_dir / f"{name}.csv", index=False)
