import streamlit as st
import plotly.express as px

from utils.db import (
    get_companies,
    get_company_trends,
)

st.title("📈 Company Trends")

companies = get_companies()

company_name = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company_name,
    "id"
].iloc[0]

df = get_company_trends(company_id)

if df.empty:
    st.warning("No data available.")
    st.stop()

metric = st.selectbox(
    "Select Metric",
    [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "asset_turnover",
    ],
)

fig = px.line(
    df,
    x="year",
    y=metric,
    markers=True,
    title=f"{company_name} - {metric}"
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)