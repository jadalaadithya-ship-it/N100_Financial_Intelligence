def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow = Operating Activity + Investing Activity
    """
    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):
    """
    CFO / PAT Ratio
    """
    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity
    """
    if sales == 0:
        return None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion Rate
    """
    if operating_profit == 0:
        return None

    return (fcf / operating_profit) * 100
def capital_allocation_pattern(cfo, cfi, cff, cfo_quality=None):
    """
    Classify capital allocation pattern based on
    CFO, CFI and CFF signs.
    """

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    if signs == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if signs == ("+", "+", "-"):
        return "Liquidating Assets"

    if signs == ("-", "+", "+"):
        return "Distress Signal"

    if signs == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if signs == ("+", "+", "+"):
        return "Cash Accumulator"

    if signs == ("-", "-", "-"):
        return "Pre-Revenue"

    if signs == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"