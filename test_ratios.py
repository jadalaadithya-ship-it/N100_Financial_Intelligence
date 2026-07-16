from src.analytics.ratios import *

print("Net Profit Margin :", net_profit_margin(100, 1000))
print("Operating Profit Margin :", operating_profit_margin(250, 1000))
print("ROE :", return_on_equity(200, 500, 500))
print("ROCE :", return_on_capital_employed(300, 50, 500, 500, 500))
print("ROA :", return_on_assets(200, 2500))
print("OPM Check 1 :", check_opm_difference(250, 1000, 25))
print("OPM Check 2 :", check_opm_difference(250, 1000, 30))