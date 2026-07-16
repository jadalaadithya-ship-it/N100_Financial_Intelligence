from src.analytics.peer import compute_peer_percentiles

df = compute_peer_percentiles()

print(
    df[
        [
            "peer_group_name",
            "company_id",
            "metric",
            "value",
            "percentile_rank",
            "year"
        ]
    ].head(10)
)