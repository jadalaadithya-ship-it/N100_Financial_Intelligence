from src.etl.loader import load_excel

cashflow = load_excel("cashflow.xlsx")

print(cashflow.columns.tolist())