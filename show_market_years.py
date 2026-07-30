import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT DISTINCT year FROM market_cap ORDER BY year",
    conn
)

print(df)