import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

companies = ["TCS", "RELIANCE", "INFY"]

for company in companies:
    print("=" * 60)
    print(company)
    print("=" * 60)

    df = pd.read_sql(f"""
        SELECT *
        FROM financial_ratios_computed
        WHERE company_id='{company}'
        LIMIT 5
    """, conn)

    print(df)

conn.close()