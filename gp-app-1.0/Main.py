import streamlit as st

st.set_page_config(
    page_title="GP App"
)

st.write("# Wuling Monthly GP Report Generator")

st.sidebar.success("Select a feature above")

st.markdown(
    """
    Generate monthly financial report using "Gross Profit" report and Operational Expense report from "Laba Rugi" file.
    \n\n
    Feature Available:
    - GP Generator
    - Opex Summary Generator
    - Opex per Cabang Generator
    \n\n
    Created by: ***Devin Augustin***
"""
)

