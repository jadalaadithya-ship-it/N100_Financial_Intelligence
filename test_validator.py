from src.etl.loader import load_excel
from src.etl.validator import (
    check_primary_key,
    check_company_year_duplicates,
    check_foreign_key,
    check_balance_sheet,
    check_opm,
    check_positive_sales,
   dq07_year_format,
    dq08_positive_operating_profit,
    dq09_operating_profit_formula,
    dq10_tax_percentage,
    dq11_tax_rate_range,
    dq12_dividend_payout,
    dq13_url_validation,
    dq14_eps_sign,
    dq15_strict_balance,
    dq16_coverage_check,
    save_validation_report
)
companies = load_excel("companies.xlsx")
profit = load_excel("profitandloss.xlsx")
balance = load_excel("balancesheet.xlsx")

print("Running Data Quality Checks...\n")

check_primary_key(companies, "id", "companies.xlsx")
check_company_year_duplicates(profit, "profitandloss.xlsx")
check_foreign_key(
    companies,
    profit,
    "id",
    "company_id",
    "profitandloss.xlsx"
)
check_balance_sheet(balance, "balancesheet.xlsx")
check_opm(profit, "profitandloss.xlsx")
check_positive_sales(profit, "profitandloss.xlsx")
dq07_year_format(profit, "profitandloss.xlsx")
dq08_positive_operating_profit(profit)
dq09_operating_profit_formula(profit)
dq10_tax_percentage(profit)
dq11_tax_rate_range(profit)
dq12_dividend_payout(profit)
dq13_url_validation(companies)
dq14_eps_sign(profit)
dq15_strict_balance(balance)
dq16_coverage_check(profit)

save_validation_report()