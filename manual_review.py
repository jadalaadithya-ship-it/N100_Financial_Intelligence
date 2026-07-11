import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

companies = [
    "TCS",
    "RELIANCE",
    "INFY",
    "HDFCBANK",
    "ITC"
]

for company in companies:
    print("\n" + "=" * 50)
    print(company)
    print("=" * 50)

    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM profitandloss
        WHERE company_id='{company}'
        ORDER BY year
        """,
        conn,
    )

    print(df)

conn.close()
