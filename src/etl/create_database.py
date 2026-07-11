import sqlite3
from pathlib import Path

DB_FOLDER = Path("db")
DB_FOLDER.mkdir(exist_ok=True)

DATABASE = DB_FOLDER / "nifty100.db"

connection = sqlite3.connect(DATABASE)

print("Database created successfully!")

connection.close()