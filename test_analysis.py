from src.etl.loader import load_excel

analysis = load_excel("analysis.xlsx")

print(analysis.columns.tolist())