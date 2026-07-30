import streamlit as st
import plotly.express as px

from utils.db import get_sector_summary

st.title("🏭 Sector Analysis")

df = get_sector_summary()

st.subheader("Sector Summary")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(
        df,
        names="broad_sector",
        values="total_companies",
        hole=0.45,
        title="Companies by Sector"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
    )

with col2:
    fig2 = px.bar(
        df,
        x="broad_sector",
        y="avg_roe",
        color="avg_roe",
        title="Average ROE by Sector"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
    )

st.divider()

fig3 = px.bar(
    df,
    x="broad_sector",
    y="avg_roce",
    color="avg_roce",
    title="Average ROCE by Sector"
)

st.plotly_chart(
    fig3,
    use_container_width=True,
)