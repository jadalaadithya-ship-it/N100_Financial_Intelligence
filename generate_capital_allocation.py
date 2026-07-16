import pandas as pd

from src.analytics.cashflow_kpis import capital_allocation_pattern

data = [
    ["TCS", "Mar 2024", 1000, -400, -300, "High Quality"],
    ["RELIANCE", "Mar 2024", 800, -500, -100, "High Quality"],
    ["INFY", "Mar 2024", -200, 100, 300, None],
    ["ITC", "Mar 2024", 400, 200, 100, None],
]

rows = []

for company, year, cfo, cfi, cff, quality in data:
    rows.append({
        "company_id": company,
        "year": year,
        "cfo_sign": "+" if cfo >= 0 else "-",
        "cfi_sign": "+" if cfi >= 0 else "-",
        "cff_sign": "+" if cff >= 0 else "-",
        "pattern_label": capital_allocation_pattern(cfo, cfi, cff, quality)
    })

df = pd.DataFrame(rows)

df.to_csv("output/capital_allocation.csv", index=False)

print("capital_allocation.csv created successfully!")