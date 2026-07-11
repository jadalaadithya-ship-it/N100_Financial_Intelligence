from src.etl.loader import load_excel

files = [
    "documents.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]

for file in files:
    header = 0 if file in [
        "financial_ratios.xlsx",
        "market_cap.xlsx",
        "peer_groups.xlsx",
        "sectors.xlsx",
        "stock_prices.xlsx"
    ] else 1

    df = load_excel(file, header=header)
    print(f"\n{file}")
    print(df.columns.tolist())