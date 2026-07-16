from src.analytics.composite_score import composite_score

score = composite_score(
    roe=20,
    net_profit_margin=15,
    asset_turnover=1.5,
    debt_to_equity=0.5
)

print("Composite Score:", score)