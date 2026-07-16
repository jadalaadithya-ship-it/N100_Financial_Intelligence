import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

computed = pd.read_sql(
    "SELECT company_id, year, return_on_equity_pct FROM financial_ratios_computed",
    conn
)

source = pd.read_sql(
    "SELECT company_id, year, return_on_equity_pct FROM financial_ratios",
    conn
)

merged = pd.merge(
    computed,
    source,
    on=["company_id", "year"],
    suffixes=("_computed", "_source")
)

anomalies = 0

with open("output/ratio_edge_cases.log", "w") as log:

    for _, row in merged.iterrows():

        if pd.isna(row["return_on_equity_pct_source"]):
            continue

        diff = abs(
            row["return_on_equity_pct_computed"]
            - row["return_on_equity_pct_source"]
        )

        if diff > 5:
            anomalies += 1

            log.write(
                f"{row['company_id']} "
                f"{row['year']} "
                f"ROE Difference={diff:.2f}% "
                f"| Category: Formula discrepancy\n"
            )

    if anomalies == 0:
        log.write("No ROE anomalies found.\n")

print("ratio_edge_cases.log created successfully!")

conn.close()