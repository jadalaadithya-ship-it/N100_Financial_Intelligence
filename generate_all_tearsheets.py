import sqlite3
from pathlib import Path

import pandas as pd

from src.reports.tearsheet import generate_tearsheet

PROJECT_ROOT = Path(__file__).resolve().parent

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT id FROM companies",
    conn,
)

success = 0
failed = []

for company in companies["id"]:

    try:
        generate_tearsheet(company)
        success += 1

    except Exception as e:
        failed.append(
            {
                "company_id": company,
                "error": str(e),
            }
        )

pd.DataFrame(failed).to_csv(
    "output/skipped_tearsheets.csv",
    index=False,
)

print()
print("PDFs Generated :", success)
print("Failed :", len(failed))