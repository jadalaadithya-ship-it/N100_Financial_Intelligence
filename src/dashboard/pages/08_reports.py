import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_all_ratios,
    get_sector_summary,
    get_capital_data,
)

st.title("📄 Reports")

year = st.selectbox(
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

capital_year = int(year.split()[-1])

# -----------------------
# Screener Report
# -----------------------
st.subheader("📈 Screener Report")

ratios = get_all_ratios(year)

st.dataframe(ratios, use_container_width=True)

st.download_button(
    label="⬇ Download Screener CSV",
    data=ratios.to_csv(index=False),
    file_name=f"screener_{year}.csv",
    mime="text/csv",
)

st.divider()

# -----------------------
# Sector Report
# -----------------------
st.subheader("🏭 Sector Summary")

sector = get_sector_summary()

st.dataframe(sector, use_container_width=True)

st.download_button(
    label="⬇ Download Sector CSV",
    data=sector.to_csv(index=False),
    file_name="sector_summary.csv",
    mime="text/csv",
)

st.divider()

# -----------------------
# Capital Report
# -----------------------
st.subheader("💰 Capital Report")

capital = get_capital_data(capital_year)

st.dataframe(capital, use_container_width=True)

st.download_button(
    label="⬇ Download Capital CSV",
    data=capital.to_csv(index=False),
    file_name=f"capital_{capital_year}.csv",
    mime="text/csv",
)

st.divider()

# -----------------------
# Company List
# -----------------------
st.subheader("🏢 Companies")

companies = get_companies()

st.dataframe(companies, use_container_width=True)

st.download_button(
    label="⬇ Download Company List",
    data=companies.to_csv(index=False),
    file_name="companies.csv",
    mime="text/csv",
)