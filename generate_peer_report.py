import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

peer = pd.read_sql("SELECT * FROM peer_percentiles", conn)

writer = pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
)

for group in sorted(peer["peer_group_name"].unique()):

    df = peer[
        peer["peer_group_name"] == group
    ]

    sheet = group[:31]

    df.to_excel(
        writer,
        sheet_name=sheet,
        index=False
    )

writer.close()

conn.close()

print("peer_comparison.xlsx created successfully!")