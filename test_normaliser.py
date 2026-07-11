from src.etl.normaliser import normalize_year, normalize_ticker

print(normalize_year("FY2024"))
print(normalize_year("2023"))

print(normalize_ticker("tcs.ns"))
print(normalize_ticker("reliance.bo"))