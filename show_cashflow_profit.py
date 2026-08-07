import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    c.company_id,
    c.year,
    c.operating_activity,
    c.investing_activity,
    c.financing_activity,
    p.net_profit
FROM cashflow c
JOIN profitandloss p
ON c.company_id = p.company_id
AND c.year = p.year
LIMIT 10
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()