from src.etl.loader import load_excel

balance = load_excel("balancesheet.xlsx")

print(balance.columns.tolist())