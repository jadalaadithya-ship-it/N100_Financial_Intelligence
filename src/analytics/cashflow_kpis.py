import sqlite3
from pathlib import Path

import pandas as pd
def capital_allocation_pattern(cfo, cfi, cff, quality=None):
    """
    Classify capital allocation pattern based on
    CFO, CFI and CFF signs.
    """

    cfo_positive = cfo >= 0
    cfi_positive = cfi >= 0
    cff_positive = cff >= 0

    # (+ - -)
    if cfo_positive and not cfi_positive and not cff_positive:
        return "Shareholder Returns"

    # (+ - +)
    if cfo_positive and not cfi_positive and cff_positive:
        return "Growth Funded"

    # (+ + +)
    if cfo_positive and cfi_positive and cff_positive:
        return "Cash Accumulator"

    # (- + +)
    if not cfo_positive and cfi_positive and cff_positive:
        return "Distress Signal"

    # (+ + -)
    if cfo_positive and cfi_positive and not cff_positive:
        return "Asset Divestment"

    return "Other"

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    c.company_id,
    c.year,
    c.operating_activity,
    c.investing_activity,
    c.financing_activity,
    p.sales,
    p.net_profit
FROM cashflow c
JOIN profitandloss p
ON c.company_id = p.company_id
AND c.year = p.year
"""

df = pd.read_sql(query, conn)

records = []

for company, group in df.groupby("company_id"):

    group = group.sort_values("year")

    latest = group.iloc[-1]

    cfo = latest["operating_activity"]
    pat = latest["net_profit"]
    sales = latest["sales"]
    cfi = abs(latest["investing_activity"])
    cff = latest["financing_activity"]

    # CFO / PAT
    if pat != 0:
        cfo_pat = cfo / pat
    else:
        cfo_pat = None

    # CapEx Intensity
    if sales != 0:
        capex = (cfi / sales) * 100
    else:
        capex = None

    # Cash Flow Quality
    if cfo_pat is None:
        quality = "N/A"
    elif cfo_pat >= 1:
        quality = "High Quality"
    elif cfo_pat >= 0.8:
        quality = "Moderate"
    else:
        quality = "Accrual Risk"

    # Distress Flag
    distress = (
        cfo < 0 and cff > 0
    )

    records.append({
        "company_id": company,
        "year": latest["year"],
        "cfo_pat_ratio": round(cfo_pat, 2) if cfo_pat is not None else None,
        "capex_intensity_pct": round(capex, 2) if capex is not None else None,
        "cashflow_quality": quality,
        "distress_flag": distress
    })

result = pd.DataFrame(records)

result.to_excel(
    OUTPUT_DIR / "cashflow_intelligence.xlsx",
    index=False,
)

result[result["distress_flag"] == True].to_csv(
    OUTPUT_DIR / "distress_alerts.csv",
    index=False,
)

print(result.head())
print()
print("Companies:", len(result))
print("Distress Alerts:", result["distress_flag"].sum())