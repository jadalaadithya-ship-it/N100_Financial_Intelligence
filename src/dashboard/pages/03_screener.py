import streamlit as st

from utils.db import get_all_ratios

st.title("📈 Stock Screener")

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

df = get_all_ratios(year)

st.sidebar.subheader("Filters")

min_roe = st.sidebar.slider(
    "Minimum ROE",
    -200.0,
    100.0,
    10.0,
)

max_de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    20.0,
    5.0,
)

filtered = df[
    (df["return_on_equity_pct"] >= min_roe)
    &
    (df["debt_to_equity"] <= max_de)
]

st.write(f"Companies Found: {len(filtered)}")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)