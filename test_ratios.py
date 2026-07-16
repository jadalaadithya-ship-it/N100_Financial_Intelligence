from src.analytics.ratios import *

print("Net Profit Margin :", net_profit_margin(100, 1000))
print("Operating Profit Margin :", operating_profit_margin(250, 1000))
print("ROE :", return_on_equity(200, 500, 500))
print("ROCE :", return_on_capital_employed(300, 50, 500, 500, 500))
print("ROA :", return_on_assets(200, 2500))
print("OPM Check 1 :", check_opm_difference(250, 1000, 25))
print("OPM Check 2 :", check_opm_difference(250, 1000, 30))
print("Debt to Equity :", debt_to_equity(500, 1000, 500))
print("Debt Free D/E :", debt_to_equity(0, 1000, 500))

print("High Leverage :", high_leverage_flag(6, "IT"))
print("Financial High Leverage :", high_leverage_flag(6, "Financials"))

icr = interest_coverage_ratio(300, 50, 100)
print("Interest Coverage :", icr)

print("ICR Label :", icr_label(0))
print("ICR Warning :", icr_warning(1.2))

print("Net Debt :", net_debt(1000, 250))

print("Asset Turnover :", asset_turnover(5000, 2500))