"""
Security-Centric Architecture Assessment Framework
Main Streamlit application entry point.

Run with:  streamlit run app.py
"""
from __future__ import annotations
from pathlib import Path

import streamlit as st

# ── Bootstrap ─────────────────────────────────────────────────────────────────
from utils.logger import setup_logging
setup_logging()

from database.db import init_db
from utils.session_manager import init_session
from config import APP_VERSION, GENERATED_REPORTS_DIR

for d in [GENERATED_REPORTS_DIR, "database", "logs"]:
    Path(d).mkdir(parents=True, exist_ok=True)

init_db()

# ── Streamlit page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title            = "Security Architecture Framework",
    page_icon             = "🔐",
    layout                = "wide",
    initial_sidebar_state = "expanded",
)

init_session()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 100%);
    border-radius: 10px;
    padding: 20px 16px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,212,255,0.12);
    text-align: center;
">
  <div style="
      width: 36px; height: 36px;
      background: rgba(0,212,255,0.1);
      border: 1px solid rgba(0,212,255,0.25);
      border-radius: 8px;
      margin: 0 auto 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.1rem; font-weight: 900; color: #00D4FF;
  ">S</div>
  <div style="color:#e2e8f0; font-weight:700; font-size:0.88rem; line-height:1.4;">
    Security Architecture<br>Framework
  </div>
  <div style="color:#475569; font-size:0.7rem; margin-top:5px; letter-spacing:0.05em;">v{APP_VERSION}</div>
</div>
""", unsafe_allow_html=True)

    pages = [
        ("Home",                        "Home"),
        ("Login / Profile",             "Login"),
        ("New Architecture Assessment", "New Architecture Assessment"),
        ("Security Dashboard",          "Security Dashboard"),
        ("Architecture Visualization",  "Architecture Visualization"),
        ("STRIDE Threat Analysis",      "STRIDE Threat Analysis"),
        ("Risk Assessment",             "Risk Assessment"),
        ("Security Pattern Library",    "Security Pattern Library"),
        ("Architecture Patterns",       "Architecture Patterns"),
        ("Recommendations",             "Recommendations"),
        ("Attack Tree Analysis",        "Attack Tree Analysis"),
        ("DREAD & OWASP Mapping",       "DREAD & OWASP Mapping"),
        ("AI Security Assistant",       "AI Security Assistant"),
        ("Reports",                     "Reports"),
        ("Analysis History",            "Analysis History"),
    ]

    st.markdown("### Navigation")
    for label, key in pages:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state["current_page"] = key
            st.rerun()

    st.markdown("---")
    if st.button("Run E-Commerce Demo", type="primary", use_container_width=True):
        st.session_state["current_page"] = "New Architecture Assessment"
        st.session_state["trigger_demo"] = True
        st.rerun()

    # Current analysis indicator
    if st.session_state.get("analysis_result") is not None:
        result = st.session_state["analysis_result"]
        rs     = result.risk_summary
        level  = rs.get("overall_risk_level", "N/A")
        colour = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(level,"#74B9FF")
        st.markdown(f"""
<div style="background:#161b22; border:1px solid #30363d; border-radius:8px;
            padding:10px; margin-top:10px; font-size:0.8rem;">
  <div style="color:#9ca3af; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.05em;">
    Current Analysis
  </div>
  <div style="color:#e5e7eb; font-weight:600; margin:3px 0;">{result.architecture.name[:22]}</div>
  <div>
    <span style="color:#9ca3af">Threats: </span>
    <span style="color:#e5e7eb">{len(result.threats)}</span>
    &nbsp;|&nbsp;
    <span style="color:{colour}; font-weight:700">{level} Risk</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Page router ───────────────────────────────────────────────────────────────
current_page = st.session_state.get("current_page", "Home")

page_map = {
    "Home":                        "page_modules.home",
    "Login":                       "page_modules.login",
    "Security Dashboard":          "page_modules.dashboard",
    "New Architecture Assessment": "page_modules.assessment",
    "Architecture Visualization":  "page_modules.visualization",
    "STRIDE Threat Analysis":      "page_modules.threats",
    "Risk Assessment":             "page_modules.risks",
    "Security Pattern Library":    "page_modules.patterns",
    "Architecture Patterns":       "page_modules.arch_patterns",
    "Recommendations":             "page_modules.recommendations",
    "Attack Tree Analysis":        "page_modules.attack_tree",
    "DREAD & OWASP Mapping":       "page_modules.dread_owasp",
    "AI Security Assistant":       "page_modules.ai_assistant",
    "Secure Coding Examples":      "page_modules.secure_coding",
    "Research Hub":                "page_modules.research_hub",
    "Reports":                     "page_modules.reports",
    "Analysis History":            "page_modules.history",
}

import importlib, logging, traceback

module_path = page_map.get(current_page, "page_modules.home")
try:
    module = importlib.import_module(module_path)
    module.show()
except Exception as exc:
    logging.error("Page '%s' failed: %s\n%s", current_page, exc, traceback.format_exc())
    st.error(f"⚠️ Page could not be loaded: {exc}")
    with st.expander("Technical details"):
        st.code(traceback.format_exc())
