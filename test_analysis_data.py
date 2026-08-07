import sqlite3
import pandas as pd

print("Connecting to database...")

conn = sqlite3.connect("db/nifty100.db")

print("Connected!")

df = pd.read_sql("SELECT * FROM analysis LIMIT 10", conn)

print("Rows:", len(df))
print(df)

print("\nColumns:")
print(df.columns.tolist())

conn.close()

print("Done!")