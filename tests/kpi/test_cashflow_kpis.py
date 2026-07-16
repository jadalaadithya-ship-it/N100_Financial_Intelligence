import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.cashflow_kpis import *

fcf = free_cash_flow(1000, -300)

print("Test 1:", fcf == 700)
print("Test 2:", cfo_quality_score(1200, 1000) == "High Quality")
print("Test 3:", cfo_quality_score(700, 1000) == "Moderate")
print("Test 4:", cfo_quality_score(300, 1000) == "Accrual Risk")
print("Test 5:", capex_intensity(-300, 5000) == "Moderate")
print("Test 6:", fcf_conversion_rate(fcf, 900) > 70)

print("Test 7:", capital_allocation_pattern(100, -50, -30) == "Reinvestor")
print("Test 8:", capital_allocation_pattern(100, -50, -30, "High Quality") == "Shareholder Returns")
print("Test 9:", capital_allocation_pattern(-100, 50, 20) == "Distress Signal")
print("Test 10:", capital_allocation_pattern(100, 50, 20) == "Cash Accumulator")