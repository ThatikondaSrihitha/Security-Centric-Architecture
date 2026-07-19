"""Shared CSS / theme - Premium Enterprise UI."""
import streamlit as st


def inject_css() -> None:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{font-family:'Inter','Segoe UI',system-ui,sans-serif!important;-webkit-font-smoothing:antialiased;}
.stApp{background:#080c14!important;color:#e2e8f0;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0b1929 0%,#060d18 100%)!important;border-right:1px solid rgba(0,212,255,0.1)!important;}
section[data-testid="stSidebar"] *{color:#cbd5e1!important;}
section[data-testid="stSidebar"] .stButton>button{background:transparent!important;border:1px solid rgba(0,212,255,0.06)!important;border-radius:7px!important;color:#64748b!important;font-size:0.82rem!important;font-weight:500!important;padding:8px 12px!important;transition:all 0.18s ease!important;margin-bottom:2px!important;text-align:left!important;}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(0,212,255,0.06)!important;border-color:rgba(0,212,255,0.25)!important;color:#e2e8f0!important;transform:translateX(2px)!important;box-shadow:none!important;}
.main .block-container{padding:1.5rem 2rem 3rem!important;max-width:1400px!important;}
div[data-testid="metric-container"]{background:linear-gradient(135deg,rgba(15,25,40,0.95) 0%,rgba(11,21,38,0.95) 100%)!important;border:1px solid rgba(0,212,255,0.1)!important;border-radius:12px!important;padding:16px 18px!important;box-shadow:0 4px 20px rgba(0,0,0,0.25)!important;transition:transform 0.2s ease,border-color 0.2s ease!important;}
div[data-testid="metric-container"]:hover{transform:translateY(-2px)!important;border-color:rgba(0,212,255,0.2)!important;}
div[data-testid="metric-container"] label{color:#475569!important;font-size:0.7rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:0.08em!important;}
div[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#00D4FF!important;font-weight:800!important;font-size:1.6rem!important;line-height:1.2!important;}
.stButton>button{background:rgba(15,35,65,0.8)!important;color:#94a3b8!important;border:1px solid rgba(0,212,255,0.12)!important;border-radius:8px!important;font-weight:500!important;font-size:0.84rem!important;padding:0.5rem 1.2rem!important;transition:all 0.2s ease!important;box-shadow:none!important;}
.stButton>button:hover{background:rgba(0,212,255,0.08)!important;color:#e2e8f0!important;border-color:rgba(0,212,255,0.3)!important;transform:translateY(-1px)!important;box-shadow:0 4px 12px rgba(0,0,0,0.3)!important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#0369a1,#0284c7)!important;color:#fff!important;border-color:#0284c7!important;font-weight:600!important;}
.stButton>button[kind="primary"]:hover{background:linear-gradient(135deg,#0284c7,#38bdf8)!important;box-shadow:0 4px 16px rgba(0,212,255,0.2)!important;transform:translateY(-1px)!important;color:#000!important;}
.stDownloadButton>button{background:rgba(4,47,46,0.6)!important;color:#4ade80!important;border:1px solid rgba(74,222,128,0.15)!important;border-radius:8px!important;font-weight:600!important;transition:all 0.2s ease!important;}
.stDownloadButton>button:hover{background:rgba(16,185,129,0.15)!important;color:#6ee7b7!important;border-color:rgba(110,231,183,0.3)!important;transform:translateY(-1px)!important;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:rgba(11,21,38,0.8)!important;border:1px solid rgba(0,212,255,0.12)!important;border-radius:8px!important;color:#e2e8f0!important;font-size:0.87rem!important;padding:9px 12px!important;transition:border-color 0.2s ease,box-shadow 0.2s ease!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:rgba(0,212,255,0.4)!important;box-shadow:0 0 0 3px rgba(0,212,255,0.08)!important;outline:none!important;}
.stTextInput>label,.stTextArea>label,.stSelectbox>label,.stMultiSelect>label,.stSlider>label{color:#475569!important;font-size:0.72rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:0.07em!important;}
.stSelectbox>div>div{background:rgba(11,21,38,0.8)!important;border:1px solid rgba(0,212,255,0.12)!important;border-radius:8px!important;color:#e2e8f0!important;}
.stTabs [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid rgba(0,212,255,0.1)!important;gap:0!important;}
.stTabs [data-baseweb="tab"]{color:#475569!important;font-weight:600!important;font-size:0.82rem!important;padding:10px 16px!important;transition:all 0.2s ease!important;letter-spacing:0.02em!important;border-bottom:2px solid transparent!important;}
.stTabs [data-baseweb="tab"]:hover{color:#94a3b8!important;}
.stTabs [aria-selected="true"]{color:#00D4FF!important;border-bottom:2px solid #00D4FF!important;}
.streamlit-expanderHeader{background:rgba(15,25,40,0.7)!important;border:1px solid rgba(0,212,255,0.08)!important;border-radius:8px!important;color:#94a3b8!important;font-weight:600!important;font-size:0.85rem!important;transition:all 0.2s ease!important;}
.streamlit-expanderHeader:hover{border-color:rgba(0,212,255,0.2)!important;color:#e2e8f0!important;}
.stDataFrame{border:1px solid rgba(0,212,255,0.08)!important;border-radius:10px!important;overflow:hidden!important;}
.stProgress>div>div>div>div{background:linear-gradient(90deg,#0369a1,#00D4FF)!important;border-radius:10px!important;}
.stAlert{border-radius:10px!important;border-left-width:3px!important;font-size:0.86rem!important;}
.stFileUploader>div{background:rgba(11,21,38,0.5)!important;border:2px dashed rgba(0,212,255,0.15)!important;border-radius:12px!important;}
.stFileUploader>div:hover{border-color:rgba(0,212,255,0.3)!important;}
.stCheckbox>label>span{color:#64748b!important;font-size:0.84rem!important;font-weight:400!important;text-transform:none!important;letter-spacing:0!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:#080c14;}
::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.15);border-radius:10px;}
::-webkit-scrollbar-thumb:hover{background:rgba(0,212,255,0.3);}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent!important;}
.stDeployButton{display:none!important;}
hr{border:none!important;border-top:1px solid rgba(255,255,255,0.05)!important;margin:14px 0!important;}
::selection{background:rgba(0,212,255,0.15);color:#e2e8f0;}
.info-card{background:rgba(11,21,38,0.7);border:1px solid rgba(0,212,255,0.08);border-radius:10px;padding:16px 18px;margin:6px 0;}
.info-card h4{color:#00D4FF;margin:0 0 6px 0;font-size:0.9rem;font-weight:600;}
.info-card p{color:#475569;margin:0;font-size:0.83rem;line-height:1.5;}
</style>
""", unsafe_allow_html=True)


def page_header(title_or_icon, title_or_sub="", subtitle=""):
    if subtitle:
        title = title_or_sub
        sub   = subtitle
    else:
        title = title_or_icon
        sub   = title_or_sub

    st.markdown(f"""
<div style="background:rgba(10,20,40,0.6);border:1px solid rgba(0,212,255,0.1);
            border-left:3px solid #00D4FF;border-radius:10px;
            padding:20px 28px;margin-bottom:22px;">
  <h1 style="color:#e2e8f0;font-size:1.5rem;font-weight:700;
             margin:0 0 4px 0;letter-spacing:-0.02em;">{title}</h1>
  <p style="color:#475569;margin:0;font-size:0.83rem;">{sub}</p>
</div>
""", unsafe_allow_html=True)


def section_heading(title):
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:8px;margin:22px 0 12px 0;">
  <div style="width:2px;height:14px;background:#00D4FF;border-radius:2px;flex-shrink:0;opacity:0.7;"></div>
  <span style="color:#475569;font-size:0.68rem;font-weight:700;
               text-transform:uppercase;letter-spacing:0.12em;">{title}</span>
</div>
""", unsafe_allow_html=True)


def severity_badge(severity):
    styles = {
        "Critical": "background:rgba(255,45,45,0.12);color:#f87171;border:1px solid rgba(255,45,45,0.25);",
        "High":     "background:rgba(255,140,0,0.12); color:#fb923c;border:1px solid rgba(255,140,0,0.25);",
        "Medium":   "background:rgba(255,215,0,0.12); color:#fbbf24;border:1px solid rgba(255,215,0,0.25);",
        "Low":      "background:rgba(0,200,83,0.12);  color:#4ade80;border:1px solid rgba(0,200,83,0.25);",
    }
    style = styles.get(severity, "background:rgba(100,116,139,0.12);color:#94a3b8;border:1px solid rgba(100,116,139,0.25);")
    return f'<span style="{style}padding:3px 10px;border-radius:5px;font-size:0.7rem;font-weight:700;letter-spacing:0.05em;">{severity.upper()}</span>'