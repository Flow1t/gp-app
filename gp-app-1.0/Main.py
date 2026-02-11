import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_SERVER_ENABLECORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLEWEBSOCKETCOMPRESSION"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
import streamlit as st
from streamlit_option_menu import option_menu
import base64
from PIL import Image
import io

# load logo file from assets
BASE_DIR = os.path.dirname(__file__)
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
logo_img = None
logo_bytes = None
if os.path.exists(LOGO_PATH):
    logo_img = Image.open(LOGO_PATH)
    with open(LOGO_PATH, "rb") as f:
        logo_bytes = f.read()

# set page config - use logo image if available (must be called before other st.*)
if logo_img:
    st.set_page_config(
        page_title="Wuling GP App",
        page_icon=logo_img,
        layout="wide"
    )
else:
    st.set_page_config(
        page_title="Wuling GP App",
        page_icon="📊",
        layout="wide"
    )

# also inject a favicon link (works around some browsers) using base64
if logo_bytes:
    from io import BytesIO
    import base64

    # original bytes (fallback)
    b64_orig = base64.b64encode(logo_bytes).decode()

    # create a 48x48 PNG for favicon
    buf = BytesIO()
    img = Image.open(BytesIO(logo_bytes)).convert("RGBA")
    favicon_img = img.resize((48, 48), Image.LANCZOS)
    favicon_img.save(buf, format="PNG")
    b64_48 = base64.b64encode(buf.getvalue()).decode()

    favicon_html = (
        f'<link rel="icon" type="image/png" sizes="48x48" href="data:image/png;base64,{b64_48}" />'
        f'<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,{b64_orig}" />'
    )
    st.markdown(favicon_html, unsafe_allow_html=True)

# Custom CSS
# Custom CSS – clean, modern theme
st.markdown("""
<style>
    /* Overall background */
    .stApp {
        background: #020617; /* very dark navy */
        color: #e5e7eb;      /* light gray text */
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #111827;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f9fafb;
    }

    /* Main container tweaks */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Titles */
    .main-title { 
        font-size: 34px; 
        font-weight: 700; 
        color: #f9fafb; 
        letter-spacing: 0.02em;
    }
    .sub-title { 
        font-size: 16px; 
        color: #9ca3af; 
        margin-bottom: 1.5rem; 
    }

    /* Uploaded file label */
    .uploaded-file { 
        font-size: 13px; 
        color: #bbf7d0; 
        margin-top: -8px; 
    }

    /* Download buttons (white pill buttons) */
    .stDownloadButton > button {
        background: #ffffff; 
        color: #020617; 
        font-size: 15px; 
        padding: 0.6rem 1.4rem;
        border-radius: 999px;
        border: none;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.7);
        font-weight: 600;
    }
    .stDownloadButton > button:hover {
        background: #e5e7eb; 
        color: #020617;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.9);
    }

    /* Info / success boxes */
    .stAlert {
        border-radius: 10px;
        border: 1px solid #1f2937;
        background: #020617;
        color: #e5e7eb;
    }

    /* Headers */
    h1, h2, h3 {
        color: #f9fafb;
    }

    /* File uploader label */
    .stFileUploader label {
        color: #e5e7eb;
        font-weight: 500;
    }

    /* Radio / select labels etc. */
    label {
        color: #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    # Logo + title in sidebar
    if logo_img is not None:
        st.image(logo_img, use_column_width=True)
    st.markdown("<div class='sidebar-title'>Wuling GP App</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Navigation menu
    selected = option_menu(
        None,  # no big title inside the menu itself
        ["🏠 Home", "📈 GP Generator", "📊 Opex Summary", "🏢 Opex Cabang", "🧾 Opex Cabang Monthly"],
        icons=["house", "bar-chart", "table", "building", "file-earmark-excel"],
        menu_icon="menu-app",
        default_index=0,
    )

# Home page
if selected == "🏠 Home":
    st.markdown(
        "<div class='main-title'>Wuling Monthly GP Report Generator</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-title'>Generate Gross Profit and Opex reports from your monthly financial files with a clean, modern interface.</div>",
        unsafe_allow_html=True,
    )
    st.info("Use the navigation on the left to select which report you want to generate.")

# GP Generator
elif selected == "📈 GP Generator":
    from gp_1_Gross_Profit import process_gp

    st.header("📈 Gross Profit Report Generator")
    st.caption("Upload the monthly Gross Profit and Penjualan Unit files to generate the GP report.")

    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("📄 Gross Profit Penjualan", type=["xlsx"])
        if file1:
            st.markdown(
                f"<div class='uploaded-file'>✅ {file1.name} "
                f"({round(len(file1.getbuffer())/1024, 1)} KB)</div>",
                unsafe_allow_html=True,
            )
    with col2:
        file2 = st.file_uploader("📄 Report Penjualan Unit", type=["xlsx"])
        if file2:
            st.markdown(
                f"<div class='uploaded-file'>✅ {file2.name} "
                f"({round(len(file2.getbuffer())/1024, 1)} KB)</div>",
                unsafe_allow_html=True,
            )

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

#Opex Cabang Monthly
elif selected == "🧾 Opex Cabang Monthly":
    from gp_4_Opex_Cabang_Monthly import opex_cabang_monthly

    st.header("🧾 Opex Cabang Monthly")
    file = st.file_uploader("📄 Upload Opex Cabang file", type=["xlsx"])

    if file:
        st.markdown(
            f"<div class='uploaded-file'>✅ {file.name} ({round(len(file.getbuffer())/1024, 1)} KB)</div>",
            unsafe_allow_html=True
        )

        with st.spinner("Processing Opex Cabang Monthly..."):
            output_io = opex_cabang_monthly(file)  # <— returns BytesIO, not path

        st.success("✅ Combined file generated!")

        st.download_button(
            "⬇ Download Combined Excel File",
            data=output_io,
            file_name="Opex_Wuling_All_Cabang_Monthly.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

