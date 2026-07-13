from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd


ZERODHA_CHARGES_SOURCE_URL = "https://zerodha.com/charges/"
ZERODHA_STT_SOURCE_URL = "https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated"
ZERODHA_CHARGE_COMPONENTS_SOURCE_URL = "https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/what-are-the-various-statutory-charges-like-stamp-duty-and-taxes-etc"
ZERODHA_TRANSACTION_CHARGE_REVISION_URL = "https://zerodha.com/marketintel/bulletin/391488/revision-in-transactions-charges-from-1st-october-2024"
ZERODHA_CHARGES_SOURCE_NAME = "Zerodha published equity intraday NSE charge schedule"
ZERODHA_CHARGES_ACCESS_DATE = "2026-07-14"
ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION = "zerodha_equity_intraday_nse_order_formula_v2_2026_07_14"

BROKERAGE_RATE = 0.0003
BROKERAGE_CAP_PER_EXECUTED_ORDER_INR = 20.0
STT_INTRADAY_SELL_SIDE_RATE = 0.00025
NSE_TRANSACTION_CHARGE_RATE = 0.0000307
SEBI_CHARGE_RATE = 10.0 / 10_000_000.0
STAMP_DUTY_BUY_SIDE_RATE = 0.00003
GST_RATE = 0.18


@dataclass(frozen=True)
class ZerodhaIntradayCharges:
    buy_value_inr: float
    sell_value_inr: float
    buy_quantity: float
    sell_quantity: float
    buy_orders: int
    sell_orders: int
    brokerage: float
    stt: float
    transaction_charge: float
    sebi_charge: float
    stamp_duty: float
    gst: float
    total_charges: float
    turnover: float
    effective_bps_on_buy_value: float
    effective_bps_on_turnover: float
    breakeven_bps_on_buy_value: float
    stt_rounding_policy: str
    model_version: str


def _round_nearest_rupee(value: float) -> float:
    return float(int(value + 0.5))


def _brokerage(order_value: float, orders: int) -> float:
    if orders <= 0 or order_value <= 0:
        return 0.0
    per_order_value = order_value / float(orders)
    return float(orders) * min(per_order_value * BROKERAGE_RATE, BROKERAGE_CAP_PER_EXECUTED_ORDER_INR)


def calculate_equity_intraday_nse_charges(
    *,
    buy_value_inr: float,
    sell_value_inr: float,
    buy_quantity: float = 1.0,
    sell_quantity: float = 1.0,
    buy_orders: int = 1,
    sell_orders: int = 1,
) -> ZerodhaIntradayCharges:
    buy_value = float(max(buy_value_inr, 0.0))
    sell_value = float(max(sell_value_inr, 0.0))
    turnover = buy_value + sell_value
    brokerage = _brokerage(buy_value, int(buy_orders)) + _brokerage(sell_value, int(sell_orders))
    if buy_quantity > 0 and sell_quantity > 0:
        average_intraday_price = turnover / float(buy_quantity + sell_quantity)
        stt_base = average_intraday_price * float(sell_quantity)
    else:
        stt_base = sell_value
    stt = _round_nearest_rupee(stt_base * STT_INTRADAY_SELL_SIDE_RATE)
    transaction_charge = turnover * NSE_TRANSACTION_CHARGE_RATE
    sebi_charge = turnover * SEBI_CHARGE_RATE
    stamp_duty = buy_value * STAMP_DUTY_BUY_SIDE_RATE
    gst = GST_RATE * (brokerage + transaction_charge + sebi_charge)
    total = brokerage + stt + transaction_charge + sebi_charge + stamp_duty + gst
    return ZerodhaIntradayCharges(
        buy_value_inr=buy_value,
        sell_value_inr=sell_value,
        buy_quantity=float(buy_quantity),
        sell_quantity=float(sell_quantity),
        buy_orders=int(buy_orders),
        sell_orders=int(sell_orders),
        brokerage=brokerage,
        stt=stt,
        transaction_charge=transaction_charge,
        sebi_charge=sebi_charge,
        stamp_duty=stamp_duty,
        gst=gst,
        total_charges=total,
        turnover=turnover,
        effective_bps_on_buy_value=(total / buy_value * 10_000.0) if buy_value else 0.0,
        effective_bps_on_turnover=(total / turnover * 10_000.0) if turnover else 0.0,
        breakeven_bps_on_buy_value=(total / buy_value * 10_000.0) if buy_value else 0.0,
        stt_rounding_policy="nearest_rupee_from_documented_intraday_average_price_method",
        model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    )


def charge_component_catalog() -> pd.DataFrame:
    rows: list[dict[str, Any]] = [
        {
            "component": "brokerage",
            "formula": "min(0.03% of executed order value, Rs 20) per buy/sell executed order",
            "side": "buy_and_sell",
            "rate": BROKERAGE_RATE,
            "source_url": ZERODHA_CHARGES_SOURCE_URL,
            "rounding_or_cap": "Rs 20 cap per executed order",
        },
        {
            "component": "stt",
            "formula": "0.025% on equity intraday sell side; rounded to nearest rupee",
            "side": "sell",
            "rate": STT_INTRADAY_SELL_SIDE_RATE,
            "source_url": ZERODHA_STT_SOURCE_URL,
            "rounding_or_cap": "nearest rupee",
        },
        {
            "component": "nse_transaction_charge",
            "formula": "0.00307% of buy plus sell turnover",
            "side": "buy_and_sell",
            "rate": NSE_TRANSACTION_CHARGE_RATE,
            "source_url": ZERODHA_CHARGES_SOURCE_URL,
            "rounding_or_cap": "unrounded analytical estimate",
        },
        {
            "component": "sebi_charge",
            "formula": "Rs 10 per crore of buy plus sell turnover",
            "side": "buy_and_sell",
            "rate": SEBI_CHARGE_RATE,
            "source_url": ZERODHA_CHARGES_SOURCE_URL,
            "rounding_or_cap": "unrounded analytical estimate",
        },
        {
            "component": "stamp_duty",
            "formula": "0.003% on buy side",
            "side": "buy",
            "rate": STAMP_DUTY_BUY_SIDE_RATE,
            "source_url": ZERODHA_CHARGES_SOURCE_URL,
            "rounding_or_cap": "unrounded analytical estimate",
        },
        {
            "component": "gst",
            "formula": "18% of brokerage plus SEBI charges plus transaction charges",
            "side": "buy_and_sell",
            "rate": GST_RATE,
            "source_url": ZERODHA_CHARGES_SOURCE_URL,
            "rounding_or_cap": "unrounded analytical estimate",
        },
    ]
    return pd.DataFrame(rows)


def representative_charge_scenarios() -> pd.DataFrame:
    notionals = [10_000.0, 25_000.0, 50_000.0, 100_000.0, 250_000.0, 500_000.0]
    rows = []
    for notional in notionals:
        charges = calculate_equity_intraday_nse_charges(
            buy_value_inr=notional,
            sell_value_inr=notional,
            buy_quantity=1.0,
            sell_quantity=1.0,
            buy_orders=1,
            sell_orders=1,
        )
        rows.append(asdict(charges))
    return pd.DataFrame(rows)
