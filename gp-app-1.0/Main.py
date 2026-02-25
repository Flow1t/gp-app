import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

import streamlit as st
import base64
from PIL import Image
from io import BytesIO

# ─── Page Config ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def load_logo(path: str):
    if not os.path.exists(path):
        return None, None, None
    img = Image.open(path)
    with open(path, "rb") as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode()
    return img, raw, b64

LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
logo_img, logo_bytes, logo_b64 = load_logo(LOGO_PATH)

st.set_page_config(
    page_title="Wuling GP App",
    page_icon=logo_img or "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inject CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #0a0d14;
    color: #c8d0e0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #080b11 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    width: 240px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

.sidebar-header {
    padding: 28px 20px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 8px;
}
.sidebar-logo {
    width: 48px;
    height: 48px;
    object-fit: contain;
    margin-bottom: 10px;
}
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: #ffffff;
    text-transform: uppercase;
}
.sidebar-tagline {
    font-size: 10px;
    color: #4a5568;
    letter-spacing: 0.08em;
    margin-top: 2px;
}

/* ── Nav items (radio buttons) ── */
div[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}
div[data-testid="stSidebar"] .stRadio label {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 20px;
    margin: 0 !important;
    border-radius: 0;
    cursor: pointer;
    font-size: 13px;
    font-weight: 400;
    color: #6b7a99;
    transition: all 0.15s ease;
    border-left: 2px solid transparent;
}
div[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.04);
    color: #c8d0e0;
    border-left-color: rgba(88,130,255,0.4);
}
div[data-testid="stSidebar"] .stRadio [aria-checked="true"] + div label {
    background: rgba(88,130,255,0.08);
    color: #5882ff;
    border-left-color: #5882ff;
    font-weight: 500;
}
/* Hide radio circles */
div[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ── Main content area ── */
.block-container {
    max-width: 860px;
    padding: 40px 48px 60px !important;
}

/* ── Page headers ── */
.page-eyebrow {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.2em;
    color: #5882ff;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 6px;
}
.page-desc {
    font-size: 14px;
    color: #4a5568;
    margin-bottom: 36px;
    line-height: 1.6;
}

/* ── Upload cards ── */
.upload-section {
    background: #0e1320;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s ease;
}
.upload-section:hover {
    border-color: rgba(88,130,255,0.25);
}
.upload-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: #5882ff;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploader"] > div {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    padding: 16px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: rgba(88,130,255,0.4) !important;
    background: rgba(88,130,255,0.04) !important;
}
[data-testid="stFileUploader"] label {
    color: #6b7a99 !important;
    font-size: 13px !important;
}
[data-testid="stFileUploader"] small {
    color: #3d4a63 !important;
    font-size: 11px !important;
}

/* ── Buttons ── */
.stButton > button, .stDownloadButton > button {
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    background: #5882ff !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 11px 24px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(88,130,255,0.25) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #6b92ff !important;
    box-shadow: 0 6px 28px rgba(88,130,255,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Success / Info alerts ── */
.stAlert {
    background: rgba(88,130,255,0.08) !important;
    border: 1px solid rgba(88,130,255,0.2) !important;
    border-radius: 10px !important;
    color: #c8d0e0 !important;
}
[data-testid="stNotification"] {
    background: rgba(34,197,94,0.08) !important;
    border: 1px solid rgba(34,197,94,0.2) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #5882ff !important; }

/* ── Home cards ── */
.home-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin-top: 8px;
}
.home-card {
    background: #0e1320;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 22px 24px;
    transition: all 0.2s ease;
    cursor: default;
}
.home-card:hover {
    border-color: rgba(88,130,255,0.3);
    background: #111828;
    transform: translateY(-2px);
}
.home-card-icon {
    font-size: 22px;
    margin-bottom: 10px;
}
.home-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 5px;
}
.home-card-desc {
    font-size: 12px;
    color: #4a5568;
    line-height: 1.5;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── Hide Streamlit chrome ── */
#footer { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

.file-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    color: #4ade80;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_html = ""
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="sidebar-logo"/>'

    st.markdown(f"""
    <div class="sidebar-header">
        {logo_html}
        <div class="sidebar-brand">Wuling GP App</div>
        <div class="sidebar-tagline">Report Generator</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home": "home",
        "📈  GP Generator": "gp",
        "📊  Opex Summary": "opex_summary",
        "🏢  Opex Cabang": "opex_cabang",
        "🧾  Opex Monthly": "opex_monthly",
    }

    selected_label = st.radio(
        label="nav",
        options=list(pages.keys()),
        label_visibility="collapsed",
    )
    selected = pages[selected_label]

# ─── Helper ─────────────────────────────────────────────────────────────────────
def page_header(eyebrow: str, title: str, desc: str = ""):
    st.markdown(f"""
    <div class="page-eyebrow">{eyebrow}</div>
    <div class="page-title">{title}</div>
    <div class="page-desc">{desc}</div>
    """, unsafe_allow_html=True)

def file_badge(name: str, size_kb: float):
    st.markdown(
        f'<div class="file-badge">✓ {name} &nbsp;·&nbsp; {size_kb:.1f} KB</div>',
        unsafe_allow_html=True,
    )

# ─── Pages ──────────────────────────────────────────────────────────────────────

if selected == "home":
    page_header("Dashboard", "Monthly Report Generator",
                "Select a report type from the sidebar to get started.")

    st.markdown("""
    <div class="home-grid">
        <div class="home-card">
            <div class="home-card-icon">📈</div>
            <div class="home-card-title">GP Generator</div>
            <div class="home-card-desc">Generate monthly Gross Profit reports from Penjualan files.</div>
        </div>
        <div class="home-card">
            <div class="home-card-icon">📊</div>
            <div class="home-card-title">Opex Summary</div>
            <div class="home-card-desc">Summarize consolidated Laba Rugi into a structured Opex report.</div>
        </div>
        <div class="home-card">
            <div class="home-card-icon">🏢</div>
            <div class="home-card-title">Opex Cabang</div>
            <div class="home-card-desc">Break down operational expenses by each branch office.</div>
        </div>
        <div class="home-card">
            <div class="home-card-icon">🧾</div>
            <div class="home-card-title">Opex Monthly</div>
            <div class="home-card-desc">Combine all branch Opex data into monthly sheets.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:12px;color:#3d4a63;">All source files are downloadable from Meta.</p>',
        unsafe_allow_html=True
    )

elif selected == "gp":
    from gp_1_Gross_Profit import process_gp

    page_header(
        "GP Generator",
        "Gross Profit Report",
        "Upload the two monthly Penjualan files to generate the consolidated GP report."
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<div class="upload-section"><div class="upload-label">File 1</div>', unsafe_allow_html=True)
        file1 = st.file_uploader("Gross Profit Penjualan", type=["xlsx"], key="gp_f1", label_visibility="collapsed")
        if file1:
            file_badge(file1.name, len(file1.getbuffer()) / 1024)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="upload-section"><div class="upload-label">File 2</div>', unsafe_allow_html=True)
        file2 = st.file_uploader("Report Penjualan Unit", type=["xlsx"], key="gp_f2", label_visibility="collapsed")
        if file2:
            file_badge(file2.name, len(file2.getbuffer()) / 1024)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if file1 and file2:
        if st.button("Generate GP Report", key="btn_gp"):
            with st.spinner("Processing..."):
                output_file = process_gp(file1, file2)
            st.success("Report generated successfully.")
            with open(output_file, "rb") as f:
                st.download_button(
                    "⬇  Download GP Report",
                    data=f,
                    file_name="gp.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
    else:
        st.markdown(
            '<p style="font-size:12px;color:#3d4a63;">Upload both files to enable report generation.</p>',
            unsafe_allow_html=True
        )

elif selected == "opex_summary":
    from gp_2_Opex_Summary import opex_summary

    page_header(
        "Opex Summary",
        "Consolidated Opex Summary",
        "Upload the Laba Rugi Konsolidasi file to generate the Opex Summary report."
    )

    st.markdown('<div class="upload-section"><div class="upload-label">Source File</div>', unsafe_allow_html=True)
    file = st.file_uploader("Laba Rugi – Konsolidasi", type=["xlsx"], key="os_f", label_visibility="collapsed")
    if file:
        file_badge(file.name, len(file.getbuffer()) / 1024)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if file:
        if st.button("Generate Opex Summary", key="btn_os"):
            with st.spinner("Processing..."):
                output_file = opex_summary(file)
            st.success("Opex Summary generated successfully.")
            with open(output_file, "rb") as f:
                st.download_button(
                    "⬇  Download Opex Summary",
                    data=f,
                    file_name="opex-summary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

elif selected == "opex_cabang":
    from gp_3_Opex_Cabang import opex_cabang

    page_header(
        "Opex Cabang",
        "Per-Branch Opex Report",
        "Upload the combined Laba Rugi per-Cabang file (all branches as separate sheets)."
    )

    st.markdown('<div class="upload-section"><div class="upload-label">Source File</div>', unsafe_allow_html=True)
    file = st.file_uploader("Laba Rugi – per Cabang", type=["xlsx"], key="oc_f", label_visibility="collapsed")
    if file:
        file_badge(file.name, len(file.getbuffer()) / 1024)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if file:
        if st.button("Generate Opex Cabang", key="btn_oc"):
            with st.spinner("Processing all branches..."):
                output_file = opex_cabang(file)
            st.success("Opex Cabang report generated.")
            with open(output_file, "rb") as f:
                st.download_button(
                    "⬇  Download Opex Cabang",
                    data=f,
                    file_name="opex-cabang.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

elif selected == "opex_monthly":
    from gp_4_Opex_Cabang_Monthly import opex_cabang_monthly

    page_header(
        "Opex Monthly",
        "Monthly Opex Combiner",
        "Combines all branch Opex data into one file organized by month."
    )

    st.markdown('<div class="upload-section"><div class="upload-label">Source File</div>', unsafe_allow_html=True)
    file = st.file_uploader("Opex Cabang Combined File", type=["xlsx"], key="om_f", label_visibility="collapsed")
    if file:
        file_badge(file.name, len(file.getbuffer()) / 1024)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if file:
        if st.button("Generate Monthly Report", key="btn_om"):
            with st.spinner("Combining all months..."):
                output_io = opex_cabang_monthly(file)
            st.success("Monthly report generated.")
            st.download_button(
                "⬇  Download Opex Monthly",
                data=output_io,
                file_name="Opex_Wuling_All_Cabang_Monthly.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
