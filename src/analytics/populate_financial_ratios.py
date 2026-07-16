import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import sqlite3
import pandas as pd

from src.etl.loader import load_excel
from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    asset_turnover
)
profit = load_excel("profitandloss.xlsx")
balance = load_excel("balancesheet.xlsx")

merged = pd.merge(
    profit,
    balance,
    on=["company_id", "year"],
    how="inner"
)

rows = []

for _, row in merged.iterrows():
    rows.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "net_profit_margin_pct":
            net_profit_margin(row["net_profit"], row["sales"]),

        "operating_profit_margin_pct":
            operating_profit_margin(
                row["operating_profit"],
                row["sales"]
            ),

        "return_on_equity_pct":
            return_on_equity(
                row["net_profit"],
                row["equity_capital"],
                row["reserves"]
            ),

        "debt_to_equity":
            debt_to_equity(
                row["borrowings"],
                row["equity_capital"],
                row["reserves"]
            ),

        "asset_turnover":
            asset_turnover(
                row["sales"],
                row["total_assets"]
            )
    })

df = pd.DataFrame(rows)

print(df.head())
print("Rows:", len(df))
conn = sqlite3.connect("db/nifty100.db")

df.to_sql(
    "financial_ratios_computed",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("financial_ratios_computed table created successfully!")