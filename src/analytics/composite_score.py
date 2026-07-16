def composite_score(
    roe,
    net_profit_margin,
    asset_turnover,
    debt_to_equity
):
    """
    Simple composite score (0–100).
    """

    score = 0

    score += min(max(roe, 0), 25) * 2
    score += min(max(net_profit_margin, 0), 25)
    score += min(max(asset_turnover, 0), 2) * 10
    score += max(0, 20 - debt_to_equity * 10)

    return round(score, 2)