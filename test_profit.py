from src.etl.loader import load_excel

profit = load_excel("profitandloss.xlsx")

print(profit.columns.tolist())