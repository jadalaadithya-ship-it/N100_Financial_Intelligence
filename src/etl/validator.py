from pathlib import Path
import pandas as pd

OUTPUT_FOLDER = Path("output")
OUTPUT_FOLDER.mkdir(exist_ok=True)

validation_results = []


def log_failure(rule, severity, dataset, message):
    validation_results.append({
        "Rule": rule,
        "Severity": severity,
        "Dataset": dataset,
        "Message": message
    })


def check_primary_key(df, column_name, dataset):
    duplicates = df[df[column_name].duplicated()]

    if duplicates.empty:
        print(f"DQ-01 Passed : {dataset}")
    else:
        print(f"DQ-01 Failed : {dataset}")

        for value in duplicates[column_name]:
            log_failure(
                "DQ-01",
                "CRITICAL",
                dataset,
                f"Duplicate Primary Key : {value}"
            )
def check_company_year_duplicates(df, dataset):
    duplicates = df[df.duplicated(subset=["company_id", "year"], keep=False)]

    if duplicates.empty:
        print(f"DQ-02 Passed : {dataset}")
    else:
        print(f"DQ-02 Failed : {dataset}")

        for _, row in duplicates.iterrows():
            log_failure(
                "DQ-02",
                "CRITICAL",
                dataset,
                f"Duplicate ({row['company_id']}, {row['year']})"
            )
def check_foreign_key(parent_df, child_df, parent_key, child_key, dataset):
    parent_values = set(parent_df[parent_key])

    missing = child_df[~child_df[child_key].isin(parent_values)]

    if missing.empty:
        print(f"DQ-03 Passed : {dataset}")
    else:
        print(f"DQ-03 Failed : {dataset}")
        print("\nMissing Foreign Keys:")
        print(missing[[child_key]].drop_duplicates())
def check_balance_sheet(df, dataset):
    """
    DQ-04:
    Validate Total Assets == Total Liabilities
    """

    tolerance = 1

    invalid = df[
        (df["total_assets"] - df["total_liabilities"]).abs() > tolerance
    ]

    if invalid.empty:
        print(f"DQ-04 Passed : {dataset}")
    else:
        print(f"DQ-04 Failed : {dataset}")

        for _, row in invalid.iterrows():
            log_failure(
                "DQ-04",
                "CRITICAL",
                dataset,
                f"{row['company_id']} {row['year']} Assets={row['total_assets']} Liabilities={row['total_liabilities']}"
            )
def check_opm(df, dataset):
    """
    DQ-05:
    Validate Operating Profit Margin (OPM)
    OPM = (Operating Profit / Sales) * 100
    """

    tolerance = 1

    valid = df[
        df["sales"].notna() &
        df["operating_profit"].notna() &
        df["opm_percentage"].notna() &
        (df["sales"] != 0)
    ]

    calculated_opm = (
        valid["operating_profit"] / valid["sales"]
    ) * 100

    invalid = valid[
        (calculated_opm - valid["opm_percentage"]).abs() > tolerance
    ]

    if invalid.empty:
        print(f"DQ-05 Passed : {dataset}")
    else:
        print(f"DQ-05 Failed : {dataset}")

        for _, row in invalid.iterrows():
            log_failure(
                "DQ-05",
                "WARNING",
                dataset,
                f"{row['company_id']} {row['year']}"
            )
def save_validation_report():
    if not validation_results:
        print("No validation failures found.")
        return

    df = pd.DataFrame(validation_results)

    output_file = OUTPUT_FOLDER / "validation_failures.csv"
    df.to_csv(output_file, index=False)

    print(f"\nValidation report saved: {output_file}")
def check_positive_sales(df, dataset):
    """
    DQ-06:
    Sales should be greater than zero.
    """

    invalid = df[
        df["sales"].notna() &
        (df["sales"] <= 0)
    ]

    if invalid.empty:
        print(f"DQ-06 Passed : {dataset}")
    else:
        print(f"DQ-06 Failed : {dataset}")

        for _, row in invalid.iterrows():
            log_failure(
                "DQ-06",
                "CRITICAL",
                dataset,
                f"{row['company_id']} {row['year']} Sales={row['sales']}"
            )
import re

def dq07_year_format(df, dataset):
    """
    DQ-07:
    Validate year values in the raw dataset.
    """

    valid_prefixes = ("Mar ", "Dec ", "Jun ", "Sep ", "TTM")

    invalid = df[
        ~df["year"].astype(str).str.startswith(valid_prefixes)
    ]

    if invalid.empty:
        print(f"DQ-07 Passed : {dataset}")
    else:
        print(f"DQ-07 Failed : {dataset}")

        for _, row in invalid.iterrows():
            log_failure(
                "DQ-07",
                "CRITICAL",
                dataset,
                f"Invalid Year: {row['year']}"
            )
def dq08_positive_operating_profit(df):
    failed = df[df["operating_profit"] < 0]

    if failed.empty:
        print("DQ-08 Passed : profitandloss.xlsx")
    else:
        print("DQ-08 Failed : profitandloss.xlsx")

    return failed
def dq09_operating_profit_formula(df):
    """
    DQ-09:
    Operating Profit should approximately equal Sales - Expenses.
    """

    tolerance = 1

    expected = df["sales"] - df["expenses"]

    failed = df[
        (expected - df["operating_profit"]).abs() > tolerance
    ]

    if failed.empty:
        print("DQ-09 Passed : profitandloss.xlsx")
    else:
        print("DQ-09 Failed : profitandloss.xlsx")

    return failed
def dq10_tax_percentage(df):
    """
    DQ-10:
    Tax percentage should be between 0 and 100.
    """

    failed = df[
        df["tax_percentage"].notna() &
        (
            (df["tax_percentage"] < 0) |
            (df["tax_percentage"] > 100)
        )
    ]

    if failed.empty:
        print("DQ-10 Passed : profitandloss.xlsx")
    else:
        print("DQ-10 Failed : profitandloss.xlsx")

    return failed
def dq11_tax_rate_range(df):
    """
    DQ-11:
    Tax rate should be between 0 and 60 percent.
    """

    failed = df[
        df["tax_percentage"].notna() &
        (
            (df["tax_percentage"] < 0) |
            (df["tax_percentage"] > 60)
        )
    ]

    if failed.empty:
        print("DQ-11 Passed : profitandloss.xlsx")
    else:
        print("DQ-11 Failed : profitandloss.xlsx")

        for _, row in failed.iterrows():
            log_failure(
                "DQ-11",
                "WARNING",
                "profitandloss.xlsx",
                f"{row['company_id']} {row['year']} Tax={row['tax_percentage']}"
            )
def dq12_dividend_payout(df):
    """
    DQ-12:
    Dividend payout should not exceed 200%.
    """

    failed = df[
        df["dividend_payout"].notna() &
        (df["dividend_payout"] > 200)
    ]

    if failed.empty:
        print("DQ-12 Passed : profitandloss.xlsx")
    else:
        print("DQ-12 Failed : profitandloss.xlsx")

        for _, row in failed.iterrows():
            log_failure(
                "DQ-12",
                "WARNING",
                "profitandloss.xlsx",
                f"{row['company_id']} {row['year']} Dividend={row['dividend_payout']}"
            )
def dq13_url_validation(df):
    """
    DQ-13:
    Website URL should start with http:// or https://
    """

    failed = df[
        df["website"].notna() &
        ~df["website"].astype(str).str.startswith(("http://", "https://"))
    ]

    if failed.empty:
        print("DQ-13 Passed : companies.xlsx")
    else:
        print("DQ-13 Failed : companies.xlsx")

        for _, row in failed.iterrows():
            log_failure(
                "DQ-13",
                "WARNING",
                "companies.xlsx",
                f"{row['id']} Website={row['website']}"
            )
def dq14_eps_sign(df):
    """
    DQ-14:
    If Net Profit is positive, EPS should also be positive.
    """

    failed = df[
        (df["net_profit"] > 0) &
        (df["eps"] <= 0)
    ]

    if failed.empty:
        print("DQ-14 Passed : profitandloss.xlsx")
    else:
        print("DQ-14 Failed : profitandloss.xlsx")

        for _, row in failed.iterrows():
            log_failure(
                "DQ-14",
                "WARNING",
                "profitandloss.xlsx",
                f"{row['company_id']} {row['year']} NetProfit={row['net_profit']} EPS={row['eps']}"
            )
def dq15_strict_balance(df):
    """
    DQ-15:
    Total Assets must exactly equal Total Liabilities.
    """

    failed = df[
        df["total_assets"] != df["total_liabilities"]
    ]

    if failed.empty:
        print("DQ-15 Passed : balancesheet.xlsx")
    else:
        print("DQ-15 Failed : balancesheet.xlsx")

        for _, row in failed.iterrows():
            log_failure(
                "DQ-15",
                "WARNING",
                "balancesheet.xlsx",
                f"{row['company_id']} {row['year']}"
            )
def dq16_coverage_check(df):
    """
    DQ-16:
    Every company should have at least 5 years of data.
    """

    coverage = df.groupby("company_id")["year"].nunique()

    failed = coverage[coverage < 5]

    if failed.empty:
        print("DQ-16 Passed : profitandloss.xlsx")
    else:
        print("DQ-16 Failed : profitandloss.xlsx")

        for company, years in failed.items():
            log_failure(
                "DQ-16",
                "WARNING",
                "profitandloss.xlsx",
                f"{company} has only {years} years of data"
            )