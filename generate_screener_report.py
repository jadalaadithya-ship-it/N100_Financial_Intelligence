import pandas as pd

from src.screener.engine import (
    load_config,
    load_ratios,
    apply_filter
)

config = load_config()
df = load_ratios()

writer = pd.ExcelWriter(
    "output/screener_output.xlsx",
    engine="openpyxl"
)

for preset, rules in config.items():

    result = apply_filter(df.copy(), rules)

    result.to_excel(
        writer,
        sheet_name=preset[:31],
        index=False
    )

writer.close()

print("screener_output.xlsx created successfully!")