import streamlit as st
import plotly.express as px

from utils.db import get_peer_comparison

st.title("👥 Peer Comparison")

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

df = get_peer_comparison(year)

peer_groups = sorted(df["peer_group_name"].dropna().unique())

selected_peer = st.selectbox(
    "Peer Group",
    peer_groups,
)

peer_df = df[df["peer_group_name"] == selected_peer]

st.subheader(f"{selected_peer} Companies")

st.dataframe(
    peer_df,
    use_container_width=True,
    hide_index=True,
)

fig = px.bar(
    peer_df,
    x="company_name",
    y="return_on_equity_pct",
    color="company_name",
    title="Return on Equity",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)