import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

# Latest ratios
ratios = pd.read_sql("""
SELECT *
FROM financial_ratios_computed
""", conn)

pl = pd.read_sql("""
SELECT *
FROM profitandloss
""", conn)

cf = pd.read_sql("""
SELECT *
FROM cashflow
""", conn)

records = []

companies = ratios["company_id"].unique()

for company in companies:

    r = ratios[ratios.company_id == company].sort_values("year").iloc[-1]

    p = pl[pl.company_id == company].sort_values("year")

    c = cf[cf.company_id == company].sort_values("year")

    # ---------- PROS ----------

    if r["return_on_equity_pct"] > 20:
        records.append([company, "PRO", "High ROE"])

    if r["operating_profit_margin_pct"] > 20:
        records.append([company, "PRO", "Healthy Operating Margin"])

    if r["net_profit_margin_pct"] > 10:
        records.append([company, "PRO", "Strong Net Profit Margin"])

    if r["debt_to_equity"] < 0.5:
        records.append([company, "PRO", "Low Debt"])

    if len(c) >= 3:
        if (c.tail(3)["operating_activity"] > 0).all():
            records.append([company, "PRO", "Positive Operating Cash Flow"])

    if len(p) >= 2:
        if p.iloc[-1]["sales"] > p.iloc[-2]["sales"]:
            records.append([company, "PRO", "Revenue Growing"])

    # ---------- CONS ----------

    if r["return_on_equity_pct"] < 10:
        records.append([company, "CON", "Weak ROE"])

    if r["debt_to_equity"] > 2:
        records.append([company, "CON", "High Debt"])

    if r["net_profit_margin_pct"] < 5:
        records.append([company, "CON", "Low Profit Margin"])

    if len(c) >= 3:
        if (c.tail(3)["operating_activity"] < 0).all():
            records.append([company, "CON", "Negative Operating Cash Flow"])

    if len(p) >= 2:
        if p.iloc[-1]["sales"] < p.iloc[-2]["sales"]:
            records.append([company, "CON", "Declining Revenue"])

    if len(p) > 0:
        if p.iloc[-1]["net_profit"] < 0:
            records.append([company, "CON", "Net Loss"])

pros_cons = pd.DataFrame(
    records,
    columns=[
        "company_id",
        "type",
        "statement",
    ],
)

pros_cons.to_csv(
    OUTPUT_DIR / "pros_cons_generated.csv",
    index=False,
)

print(pros_cons.head())

print()

print("Total Statements:", len(pros_cons))