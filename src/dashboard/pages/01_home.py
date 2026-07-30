import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import (
    get_companies,
    get_ratios,
    get_sectors,
    get_companies_with_ratios,
)

st.title("🏠 Nifty 100 Dashboard")

# --------------------------
# Year Selector
# --------------------------

year = st.sidebar.selectbox(
    "Select Year",
    [
        "Mar 2019",
        "Mar 2020",
        "Mar 2021",
        "Mar 2022",
        "Mar 2023",
        "Mar 2024",
    ],
)

# --------------------------
# Load Data
# --------------------------

companies = get_companies()
sectors = get_sectors()

ratio_list = []

for company in companies["id"]:
    df = get_ratios(company, year)

    if not df.empty:
        ratio_list.append(df)

if ratio_list:
    ratios = pd.concat(ratio_list, ignore_index=True)
else:
    ratios = pd.DataFrame()

# --------------------------
# KPI Cards
# --------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Companies",
        len(companies),
    )

with c2:
    if not ratios.empty:
        st.metric(
            "Average ROE",
            f"{ratios['return_on_equity_pct'].mean():.2f} %",
        )

with c3:
    if not ratios.empty:
        st.metric(
            "Median D/E",
            f"{ratios['debt_to_equity'].median():.2f}",
        )

c4, c5, c6 = st.columns(3)

with c4:
    if not ratios.empty:
        st.metric(
            "Average Net Profit Margin",
            f"{ratios['net_profit_margin_pct'].mean():.2f} %",
        )

with c5:
    if not ratios.empty:
        st.metric(
            "Average OPM",
            f"{ratios['operating_profit_margin_pct'].mean():.2f} %",
        )

with c6:
    if not ratios.empty:
        st.metric(
            "Average Asset Turnover",
            f"{ratios['asset_turnover'].mean():.2f}",
        )

st.divider()

# --------------------------
# Sector Distribution
# --------------------------

st.subheader("📊 Sector Distribution")

sector_count = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    hole=0.45,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

# --------------------------
# Top 5 Companies by ROE
# --------------------------

st.subheader("🏆 Top 5 Companies by ROE")

top = get_companies_with_ratios(year).head(5)

st.dataframe(
    top,
    use_container_width=True,
    hide_index=True,
)