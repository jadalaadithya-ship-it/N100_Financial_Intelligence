import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.ratios import *

print("Test 1:", debt_to_equity(500, 1000, 500) == 500 / 1500)
print("Test 2:", debt_to_equity(0, 1000, 500) == 0)
print("Test 3:", debt_to_equity(500, -1000, 500) is None)

print("Test 4:", high_leverage_flag(6, "IT") is True)
print("Test 5:", high_leverage_flag(6, "Financials") is False)

print("Test 6:", interest_coverage_ratio(300, 50, 100) == 3.5)
print("Test 7:", interest_coverage_ratio(300, 50, 0) is None)

print("Test 8:", asset_turnover(5000, 2500) == 2.0)