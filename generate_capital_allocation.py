import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import capital_allocation_pattern

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    c.company_id,
    c.year,
    c.operating_activity,
    c.investing_activity,
    c.financing_activity
FROM cashflow c
"""

df = pd.read_sql(query, conn)

rows = []

for _, row in df.iterrows():

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]

    rows.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": "+" if cfo >= 0 else "-",
        "cfi_sign": "+" if cfi >= 0 else "-",
        "cff_sign": "+" if cff >= 0 else "-",
        "pattern_label": capital_allocation_pattern(
            cfo,
            cfi,
            cff,
            None
        )
    })

output = pd.DataFrame(rows)

output.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print("Rows:", len(output))
print("capital_allocation.csv created successfully!")