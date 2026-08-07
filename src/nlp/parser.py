import re
import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("SELECT * FROM analysis", conn)

parsed_rows = []
failed_rows = []

pattern = r"(\d+)\s*Years?:?\s*([\d.]+)%"

columns_to_parse = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for _, row in df.iterrows():
    company = row["company_id"]

    for metric in columns_to_parse:
        value = str(row[metric])

        match = re.search(pattern, value)

        if match:
            parsed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))
            })
        else:
            failed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "raw_value": value
            })

parsed_df = pd.DataFrame(parsed_rows)
failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    OUTPUT_DIR / "parse_failures.csv",
    index=False
)

print("Parsing Complete")
print("Parsed Rows:", len(parsed_df))
print("Failed Rows:", len(failed_df))