from src.screener.engine import *

config = load_config()
df = load_ratios()

print("Total Rows:", len(df))

for preset, rules in config.items():

    result = apply_filter(df, rules)

    print("\n" + "=" * 50)
    print(preset.upper())
    print("=" * 50)

    print("Rows:", len(result))

    print(result.head())