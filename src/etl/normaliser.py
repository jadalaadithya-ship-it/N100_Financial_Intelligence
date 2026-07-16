import pandas as pd


def normalize_year(year):
    if pd.isna(year):
        return None

    year = str(year)
    digits = "".join(filter(str.isdigit, year))

    if len(digits) >= 4:
        return int(digits[-4:])

    return None


def normalize_ticker(ticker):
    if pd.isna(ticker):
        return None

    ticker = str(ticker).strip().upper()
    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")

    return ticker