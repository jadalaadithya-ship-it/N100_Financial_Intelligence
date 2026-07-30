from src.dashboard.utils.db import get_companies_with_ratios

df = get_companies_with_ratios("Mar 2024")

print(df.head())