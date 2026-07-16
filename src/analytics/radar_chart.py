import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_radar(company):

    conn = sqlite3.connect("db/nifty100.db")

    df = pd.read_sql(
        f"""
        SELECT *
        FROM financial_ratios_computed
        WHERE company_id='{company}'
        ORDER BY year DESC
        LIMIT 1
        """,
        conn
    )

    conn.close()

    if df.empty:
        print("Company not found")
        return

    labels = [
        "ROE",
        "NPM",
        "Asset Turnover",
        "Debt/Equity"
    ]

    values = [
        float(df["return_on_equity_pct"].iloc[0]),
        float(df["net_profit_margin_pct"].iloc[0]),
        float(df["asset_turnover"].iloc[0]),
        float(df["debt_to_equity"].iloc[0])
    ]

    values += values[:1]

    angles = np.linspace(
        0,
        2*np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    plt.figure(figsize=(6,6))

    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2)

    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels)

    plt.title(company)

    plt.savefig(
        f"reports/radar_charts/{company}_radar.png"
    )

    plt.close()

    print(f"{company} radar chart saved.")