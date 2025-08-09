import streamlit as st
from streamlit_option_menu import option_menu
import os

# Page config
st.set_page_config(
    page_title="Wuling GP App",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 36px; font-weight: bold; color: #FF4B4B; }
    .sub-title { font-size: 18px; color: #555; margin-bottom: 20px; }
    .uploaded-file { font-size: 14px; color: #2e7d32; margin-top: -10px; }
    .stDownloadButton > button {
        background-color: #FF4B4B; 
        color: white; 
        font-size: 16px; 
        padding: 10px 20px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "📂 Navigation",
        ["🏠 Home", "📈 GP Generator", "📊 Opex Summary", "🏢 Opex Cabang"],
        icons=["house", "bar-chart", "table", "building"],
        menu_icon="menu-app",
        default_index=0
    )

# Home page
if selected == "🏠 Home":
    st.markdown("<div class='main-title'>Wuling Monthly GP Report Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Generate Gross Profit and Opex reports from your monthly financial files with a modern interface.</div>", unsafe_allow_html=True)
    st.info("Select a feature from the left menu to get started.")

# GP Generator
elif selected == "📈 GP Generator":
    from gp_1_Gross_Profit import process_gp

    st.header("📈 Gross Profit Report Generator")
    st.write("Upload your 'Gross Profit Penjualan' and 'Penjualan Unit' files to generate the GP report.")

    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("📄 Gross Profit Penjualan", type=["xlsx"])
        if file1:
            st.markdown(f"<div class='uploaded-file'>✅ {file1.name} ({round(len(file1.getbuffer())/1024, 1)} KB)</div>", unsafe_allow_html=True)
    with col2:
        file2 = st.file_uploader("📄 Report Penjualan Unit", type=["xlsx"])
        if file2:
            st.markdown(f"<div class='uploaded-file'>✅ {file2.name} ({round(len(file2.getbuffer())/1024, 1)} KB)</div>", unsafe_allow_html=True)

    if file1 and file2:
        with st.spinner("Processing GP report..."):
            output_file = process_gp(file1, file2)
        st.success("✅ GP File generated!")
        with open(output_file, "rb") as f:
            st.download_button("⬇ Download GP Report", f, file_name="gp.xlsx")

# Opex Summary
elif selected == "📊 Opex Summary":
    from gp_2_Opex_Summary import opex_summary

    st.header("📊 Opex Summary Generator")
    file = st.file_uploader("📄 Upload Laba Rugi - Konsolidasi", type=["xlsx"])
    if file:
        st.markdown(f"<div class='uploaded-file'>✅ {file.name} ({round(len(file.getbuffer())/1024, 1)} KB)</div>", unsafe_allow_html=True)
        with st.spinner("Processing Opex Summary..."):
            output_file = opex_summary(file)
        st.success("✅ Opex Summary generated!")
        with open(output_file, "rb") as f:
            st.download_button("⬇ Download Opex Summary", f, file_name="opex-summary.xlsx")

# Opex Cabang
elif selected == "🏢 Opex Cabang":
    from gp_3_Opex_Cabang import opex_cabang

    st.header("🏢 Opex per Cabang Generator")
    file = st.file_uploader("📄 Upload Laba Rugi - per Cabang", type=["xlsx"])
    if file:
        st.markdown(f"<div class='uploaded-file'>✅ {file.name} ({round(len(file.getbuffer())/1024, 1)} KB)</div>", unsafe_allow_html=True)
        with st.spinner("Processing Opex Cabang..."):
            output_file = opex_cabang(file)
        st.success("✅ Opex Cabang generated!")
        with open(output_file, "rb") as f:
            st.download_button("⬇ Download Opex Cabang", f, file_name="opex-cabang.xlsx")
