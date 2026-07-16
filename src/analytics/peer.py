import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import sqlite3
import pandas as pd


def compute_peer_percentiles():

    conn = sqlite3.connect("db/nifty100.db")

    peer = pd.read_sql(
        "SELECT * FROM peer_groups",
        conn
    )

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios_computed",
        conn
    )

    df = pd.merge(
        peer,
        ratios,
        on="company_id",
        how="inner"
    )

    df["roe_percentile"] = (
        df.groupby("peer_group_name")["return_on_equity_pct"]
        .rank(pct=True) * 100
    )

    output = pd.DataFrame({
        "company_id": df["company_id"],
        "peer_group_name": df["peer_group_name"],
        "metric": "ROE",
        "value": df["return_on_equity_pct"],
        "percentile_rank": df["roe_percentile"],
        "year": df["year"]
    })

    output.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    return output