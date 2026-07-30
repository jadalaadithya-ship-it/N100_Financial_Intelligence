import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print(pd.read_sql(
    "SELECT DISTINCT year FROM financial_ratios_computed ORDER BY year",
    conn,
))