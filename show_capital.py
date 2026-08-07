import pandas as pd

df = pd.read_csv("output/capital_allocation.csv")

print(df.head(10))
print()
print(df.columns.tolist())
print()
print("Rows:", len(df))