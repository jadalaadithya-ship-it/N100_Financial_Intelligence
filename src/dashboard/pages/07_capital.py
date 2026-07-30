import streamlit as st
import plotly.express as px

from utils.db import get_capital_data

st.title("💰 Capital Dashboard")

year = st.sidebar.selectbox(
    "Select Year",
    [
        2019,
        2020,
        2021,
        2022,
        2023,
        2024,
    ],
)

df = get_capital_data(year)

if df.empty:
    st.warning("No capital data available.")
    st.stop()

st.subheader("Capital Market Data")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df.head(10),
        x="company_name",
        y="market_cap_crore",
        title="Top 10 Market Cap",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df.head(10),
        x="company_name",
        y="pe_ratio",
        title="Top 10 P/E Ratio",
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    fig = px.bar(
        df.head(10),
        x="company_name",
        y="pb_ratio",
        title="Top 10 P/B Ratio",
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.bar(
        df.head(10),
        x="company_name",
        y="dividend_yield_pct",
        title="Dividend Yield",
    )
    st.plotly_chart(fig, use_container_width=True)