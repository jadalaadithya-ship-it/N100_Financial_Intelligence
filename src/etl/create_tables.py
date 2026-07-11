import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")
SCHEMA_PATH = Path("db/schema.sql")

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Tables created successfully!")