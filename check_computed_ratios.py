import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios_computed")

print("Rows:", cursor.fetchone()[0])

conn.close()