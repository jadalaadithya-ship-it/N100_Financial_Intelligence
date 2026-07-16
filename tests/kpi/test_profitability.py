import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.ratios import *

print("Test 1:", net_profit_margin(100, 1000) == 10)
print("Test 2:", net_profit_margin(100, 0) is None)

print("Test 3:", operating_profit_margin(250, 1000) == 25)
print("Test 4:", operating_profit_margin(250, 0) is None)

print("Test 5:", return_on_equity(200, 500, 500) == 20)
print("Test 6:", return_on_equity(200, -500, 200) is None)

print("Test 7:", return_on_assets(100, 1000) == 10)

print("Test 8:", check_opm_difference(250, 1000, 30) is False)