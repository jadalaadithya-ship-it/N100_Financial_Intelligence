import sqlite3
from loader import load_excel

conn = sqlite3.connect("db/nifty100.db")

load_excel("companies.xlsx").to_sql("companies", conn, if_exists="append", index=False)
load_excel("profitandloss.xlsx").to_sql("profitandloss", conn, if_exists="append", index=False)
load_excel("balancesheet.xlsx").to_sql("balancesheet", conn, if_exists="append", index=False)
load_excel("cashflow.xlsx").to_sql("cashflow", conn, if_exists="append", index=False)
load_excel("analysis.xlsx").to_sql("analysis", conn, if_exists="append", index=False)
load_excel("documents.xlsx").to_sql("documents", conn, if_exists="append", index=False)
load_excel("financial_ratios.xlsx", header=0).to_sql("financial_ratios", conn, if_exists="append", index=False)
load_excel("market_cap.xlsx", header=0).to_sql("market_cap", conn, if_exists="append", index=False)
load_excel("peer_groups.xlsx", header=0).to_sql("peer_groups", conn, if_exists="append", index=False)
load_excel("sectors.xlsx", header=0).to_sql("sectors", conn, if_exists="append", index=False)
load_excel("stock_prices.xlsx", header=0).to_sql("stock_prices", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("All datasets loaded successfully!")