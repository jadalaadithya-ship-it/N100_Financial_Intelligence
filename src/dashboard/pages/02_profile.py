import streamlit as st

from utils.db import (
    get_companies,
    get_company,
)

st.title("🏢 Company Profile")

companies = get_companies()

company_name = st.selectbox(
    "Select Company",
    companies["company_name"],
)

company_id = companies.loc[
    companies["company_name"] == company_name,
    "id"
].iloc[0]

company = get_company(company_id).iloc[0]

col1, col2 = st.columns([1, 3])

with col1:
    st.image(company["company_logo"], width=150)

with col2:
    st.header(company["company_name"])
    st.write(company["about_company"])

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.metric("Face Value", company["face_value"])
    st.metric("Book Value", company["book_value"])
    st.metric("ROCE", f"{company['roce_percentage']} %")

with c2:
    st.metric("ROE", f"{company['roe_percentage']} %")
    st.write("🌐 Website")
    st.write(company["website"])

st.divider()

st.subheader("Exchange Links")

st.markdown(f"**NSE Profile:** {company['nse_profile']}")
st.markdown(f"**BSE Profile:** {company['bse_profile']}")