from src.etl.loader import load_excel

datasets = [
    ("companies.xlsx", 1),
    ("profitandloss.xlsx", 1),
    ("balancesheet.xlsx", 1),
    ("cashflow.xlsx", 1),
    ("analysis.xlsx", 1),
    ("documents.xlsx", 1),
    ("prosandcons.xlsx", 1),
    ("sectors.xlsx", 0),
    ("stock_prices.xlsx", 0),
    ("market_cap.xlsx", 0),
    ("financial_ratios.xlsx", 0),
    ("peer_groups.xlsx", 0)
]

print("=" * 60)
print("Loading All Datasets")
print("=" * 60)

for file_name, header in datasets:
    try:
        df = load_excel(file_name, header)
        print(f"{file_name:<25} Rows: {df.shape[0]:<5} Columns: {df.shape[1]}")
    except Exception as e:
        print(f"{file_name:<25} ERROR -> {e}")