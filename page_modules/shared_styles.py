"""Shared CSS / theme - Premium Enterprise UI."""
import streamlit as st


def inject_css() -> None:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset & Base ──────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ── App Background ────────────────────────────────── */
.stApp {
    background: #080c14 !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,212,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(15,52,96,0.15) 0%, transparent 50%) !important;
    color: #e2e8f0;
}

/* ── Sidebar ───────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1929 0%, #060d18 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.1) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(0,212,255,0.08) !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 2px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,212,255,0.08) !important;
    border-color: rgba(0,212,255,0.3) !important;
    color: #00D4FF !important;
    transform: translateX(3px) !important;
    box-shadow: none !important;
}

/* ── Main Content ──────────────────────────────────── */
.main .block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1400px !important;
}

/* ── Metric Cards ──────────────────────────────────── */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(15,25,40,0.95) 0%, rgba(11,21,38,0.95) 100%) !important;
    border: 1px solid rgba(0,212,255,0.12) !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.4), transparent);
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(0,212,255,0.25) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4), 0 0 20px rgba(0,212,255,0.08) !important;
}
div[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #00D4FF !important;
    font-weight: 800 !important;
    font-size: 1.75rem !important;
    line-height: 1.2 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* ── Buttons ───────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #0f3460 0%, #1a4a7a 100%) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.22s ease !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
}
.stButton > button::after {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    transition: left 0.4s ease;
}
.stButton > button:hover::after { left: 100%; }
.stButton > button:hover {
    background: linear-gradient(135deg, #00D4FF 0%, #0099bb 100%) !important;
    color: #000 !important;
    border-color: #00D4FF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,212,255,0.3), 0 2px 8px rgba(0,0,0,0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00b8d9 0%, #00D4FF 100%) !important;
    color: #000 !important;
    border-color: #00D4FF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(0,212,255,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #00D4FF 0%, #33ddff 100%) !important;
    box-shadow: 0 6px 25px rgba(0,212,255,0.4) !important;
    transform: translateY(-2px) !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, #064e3b 0%, #065f46 100%) !important;
    color: #6ee7b7 !important;
    border: 1px solid rgba(110,231,183,0.2) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.22s ease !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
    color: #000 !important;
    border-color: #10b981 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(16,185,129,0.3) !important;
}

/* ── Input Fields ──────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(11,21,38,0.8) !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(0,212,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
    outline: none !important;
}
.stTextInput > label, .stTextArea > label,
.stSelectbox > label, .stMultiSelect > label,
.stSlider > label, .stCheckbox > label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 4px !important;
}

/* ── Selectbox & Dropdowns ─────────────────────────── */
.stSelectbox > div > div {
    background: rgba(11,21,38,0.8) !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stSelectbox > div > div:focus-within {
    border-color: rgba(0,212,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
}

/* ── Tabs ──────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(11,21,38,0.6) !important;
    border-radius: 12px 12px 0 0 !important;
    border-bottom: 2px solid rgba(0,212,255,0.15) !important;
    padding: 0 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    padding: 10px 18px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #94a3b8 !important;
    background: rgba(0,212,255,0.05) !important;
}
.stTabs [aria-selected="true"] {
    color: #00D4FF !important;
    background: rgba(0,212,255,0.08) !important;
    border-bottom: 2px solid #00D4FF !important;
}

/* ── Expanders ─────────────────────────────────────── */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, rgba(15,25,40,0.9), rgba(11,21,38,0.9)) !important;
    border: 1px solid rgba(0,212,255,0.1) !important;
    border-radius: 10px !important;
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 14px 18px !important;
    transition: all 0.2s ease !important;
}
.streamlit-expanderHeader:hover {
    border-color: rgba(0,212,255,0.25) !important;
    color: #e2e8f0 !important;
    background: rgba(0,212,255,0.05) !important;
}
.streamlit-expanderContent {
    background: rgba(11,21,38,0.4) !important;
    border: 1px solid rgba(0,212,255,0.08) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 16px !important;
}

/* ── Tables / DataFrames ───────────────────────────── */
.stDataFrame {
    border: 1px solid rgba(0,212,255,0.1) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
.stDataFrame thead th {
    background: rgba(11,21,38,0.95) !important;
    color: #64748b !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    padding: 12px 14px !important;
    border-bottom: 2px solid rgba(0,212,255,0.15) !important;
}
.stDataFrame tbody tr {
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    transition: background 0.15s ease !important;
}
.stDataFrame tbody tr:hover {
    background: rgba(0,212,255,0.04) !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background: rgba(0,0,0,0.15) !important;
}
.stDataFrame tbody td {
    color: #cbd5e1 !important;
    font-size: 0.84rem !important;
    padding: 10px 14px !important;
}

/* ── Progress Bar ──────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #0099bb, #00D4FF, #33ddff) !important;
    border-radius: 10px !important;
}
.stProgress > div > div > div {
    background: rgba(11,21,38,0.8) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(0,212,255,0.1) !important;
}

/* ── Alerts ────────────────────────────────────────── */
.stAlert {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    font-size: 0.87rem !important;
}
div[data-testid="stNotification"] {
    border-radius: 12px !important;
}

/* ── File Uploader ─────────────────────────────────── */
.stFileUploader > div {
    background: rgba(11,21,38,0.6) !important;
    border: 2px dashed rgba(0,212,255,0.2) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s ease, background 0.2s ease !important;
}
.stFileUploader > div:hover {
    border-color: rgba(0,212,255,0.4) !important;
    background: rgba(0,212,255,0.03) !important;
}

/* ── Checkboxes ────────────────────────────────────── */
.stCheckbox > label > span {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Radio Buttons ─────────────────────────────────── */
.stRadio > div {
    gap: 8px !important;
}
.stRadio > div > label {
    background: rgba(11,21,38,0.6) !important;
    border: 1px solid rgba(0,212,255,0.12) !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
    color: #94a3b8 !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stRadio > div > label:hover {
    border-color: rgba(0,212,255,0.3) !important;
    color: #e2e8f0 !important;
    background: rgba(0,212,255,0.06) !important;
}

/* ── Sliders ───────────────────────────────────────── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #00D4FF, #0099bb) !important;
}
.stSlider > div > div > div > div > div {
    background: #00D4FF !important;
    border: 2px solid #000 !important;
    box-shadow: 0 0 8px rgba(0,212,255,0.4) !important;
}

/* ── Plotly Charts ─────────────────────────────────── */
.js-plotly-plot {
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ── Scrollbar ─────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb {
    background: rgba(0,212,255,0.2);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0,212,255,0.4); }

/* ── Hide Streamlit chrome ─────────────────────────── */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent !important; }
.stDeployButton { display: none !important; }

/* ── Dividers ──────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid rgba(0,212,255,0.08) !important;
    margin: 16px 0 !important;
}

/* ── Code blocks ───────────────────────────────────── */
.stCode, code {
    background: rgba(11,21,38,0.9) !important;
    border: 1px solid rgba(0,212,255,0.1) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
}

/* ── Selection ─────────────────────────────────────── */
::selection {
    background: rgba(0,212,255,0.2);
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


# ── Page Header ───────────────────────────────────────────────────────────────
def page_header(icon: str, title: str, subtitle: str) -> None:
    st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(10,25,50,0.95) 0%, rgba(8,20,40,0.95) 100%);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 18px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
">
  <div style="
      position: absolute; top: -40px; right: -40px;
      width: 160px; height: 160px;
      background: radial-gradient(circle, rgba(0,212,255,0.08) 0%, transparent 70%);
      pointer-events: none;
  "></div>
  <div style="display:flex; align-items:center; gap:14px; position:relative;">
    <div style="
        font-size:2rem;
        background: rgba(0,212,255,0.1);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 12px;
        width: 52px; height: 52px;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    ">{icon}</div>
    <div>
      <h1 style="
          color: #00D4FF;
          font-size: 1.75rem;
          font-weight: 800;
          margin: 0 0 4px 0;
          letter-spacing: -0.02em;
          line-height: 1.2;
      ">{title}</h1>
      <p style="color: #64748b; margin: 0; font-size: 0.88rem; font-weight: 400;">{subtitle}</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Section Heading ───────────────────────────────────────────────────────────
def section_heading(title: str) -> None:
    st.markdown(f"""
<div style="
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 14px 0;
">
  <div style="
      width: 3px; height: 18px;
      background: linear-gradient(180deg, #00D4FF, rgba(0,212,255,0.3));
      border-radius: 2px;
      flex-shrink: 0;
  "></div>
  <span style="
      color: #94a3b8;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
  ">{title}</span>
</div>
""", unsafe_allow_html=True)


# ── Severity Badge ────────────────────────────────────────────────────────────
def severity_badge(severity: str) -> str:
    styles = {
        "Critical": "background:rgba(255,45,45,0.15); color:#ff6b6b; border:1px solid rgba(255,45,45,0.3);",
        "High":     "background:rgba(255,140,0,0.15);  color:#ffa94d; border:1px solid rgba(255,140,0,0.3);",
        "Medium":   "background:rgba(255,215,0,0.15);  color:#ffd43b; border:1px solid rgba(255,215,0,0.3);",
        "Low":      "background:rgba(0,200,83,0.15);   color:#69db7c; border:1px solid rgba(0,200,83,0.3);",
    }
    style = styles.get(severity, "background:rgba(100,116,139,0.15); color:#94a3b8; border:1px solid rgba(100,116,139,0.3);")
    return f'<span style="{style} padding:3px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; letter-spacing:0.05em;">{severity}</span>'
