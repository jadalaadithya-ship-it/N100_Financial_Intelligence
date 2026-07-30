from src.dashboard.utils.db import get_companies

df = get_companies()

print(df.head())
print(df.columns.tolist())