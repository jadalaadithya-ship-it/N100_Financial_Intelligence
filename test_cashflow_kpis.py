from src.analytics.cashflow_kpis import *

fcf = free_cash_flow(1000, -300)

print("Free Cash Flow:", fcf)
print("CFO Quality:", cfo_quality_score(1200, 1000))
print("CapEx Intensity:", capex_intensity(-300, 5000))
print("FCF Conversion:", fcf_conversion_rate(fcf, 900))
print()

print(capital_allocation_pattern(100, -50, -30))
print(capital_allocation_pattern(100, -50, -30, "High Quality"))
print(capital_allocation_pattern(100, 50, -20))
print(capital_allocation_pattern(-100, 50, 20))
print(capital_allocation_pattern(-100, -50, 20))
print(capital_allocation_pattern(100, 50, 20))
print(capital_allocation_pattern(-100, -50, -20))
print(capital_allocation_pattern(100, -50, 20))