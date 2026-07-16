def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = (Net Profit / Sales) * 100
    """

    if sales == 0 or sales is None:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin = (Operating Profit / Sales) * 100
    """

    if sales == 0 or sales is None:
        return None

    return (operating_profit / sales) * 100
def check_opm_difference(operating_profit, sales, stored_opm):
    """
    Compare calculated OPM with stored OPM.
    Returns True if difference <= 1%, else False.
    """

    calculated = operating_profit_margin(operating_profit, sales)

    if calculated is None or stored_opm is None:
        return None

    return abs(calculated - stored_opm) <= 1


def return_on_equity(net_profit, equity_capital, reserves):
    """
    ROE = Net Profit / (Equity + Reserves) * 100
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    operating_profit,
    interest,
    equity_capital,
    reserves,
    borrowings,
):
    """
    ROCE = EBIT / Capital Employed * 100
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    ebit = operating_profit + interest

    return (ebit / capital) * 100


def return_on_assets(net_profit, total_assets):
    """
    ROA = Net Profit / Total Assets * 100
    """

    if total_assets == 0 or total_assets is None:
        return None

    return (net_profit / total_assets) * 100