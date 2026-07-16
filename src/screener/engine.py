import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import sqlite3
import pandas as pd
import yaml

from src.analytics.composite_score import composite_score


def load_config():
    """
    Load screener configuration from YAML.
    """
    with open("config/screener_config.yaml", "r") as file:
        return yaml.safe_load(file)


def load_ratios():
    """
    Load computed financial ratios from SQLite.
    """
    conn = sqlite3.connect("db/nifty100.db")

    df = pd.read_sql(
        "SELECT * FROM financial_ratios_computed",
        conn
    )

    conn.close()

    return df


def apply_filter(df, config):
    """
    Apply screener filters and compute composite score.
    """

    mapping = {
        "roe_min": ("return_on_equity_pct", ">="),
        "debt_to_equity_max": ("debt_to_equity", "<="),
        "free_cash_flow_min": ("free_cash_flow_cr", ">="),
        "revenue_cagr_5yr_min": ("revenue_cagr_5yr", ">="),
        "pat_cagr_5yr_min": ("pat_cagr_5yr", ">="),
        "opm_min": ("operating_profit_margin_pct", ">="),
        "pe_ratio_max": ("pe_ratio", "<="),
        "pb_ratio_max": ("pb_ratio", "<="),
        "dividend_yield_min": ("dividend_yield_pct", ">="),
        "interest_coverage_min": ("interest_coverage", ">="),
        "market_cap_min": ("market_cap_crore", ">="),
        "net_profit_min": ("net_profit", ">="),
        "eps_cagr_min": ("eps_cagr_5yr", ">="),
        "asset_turnover_min": ("asset_turnover", ">="),
        "sales_min": ("sales", ">=")
    }

    for key, value in config.items():

        if key not in mapping:
            continue

        column, operator = mapping[key]

        if column not in df.columns:
            continue

        if operator == ">=":
            df = df[df[column] >= value]
        else:
            df = df[df[column] <= value]

    df = df.copy()

    df["composite_quality_score"] = df.apply(
        lambda row: composite_score(
            row["return_on_equity_pct"],
            row["net_profit_margin_pct"],
            row["asset_turnover"],
            row["debt_to_equity"]
        ),
        axis=1
    )

    df = df.sort_values(
        by="composite_quality_score",
        ascending=False
    )

    return df