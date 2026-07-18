"""About page."""
import streamlit as st
from config import (
    APP_NAME, APP_TAGLINE, APP_VERSION, APP_DOMAIN, APP_CONCEPT, APP_METHOD,
    STUDENT_NAME, ROLL_NUMBER, DEPARTMENT, COLLEGE, GUIDE_NAME, ACADEMIC_YEAR
)
from page_modules.shared_styles import inject_css, page_header, section_heading


def show() -> None:
    inject_css()
    page_header("ℹ️", "About This Project", "Project details, academic information, and framework overview.")

    # Project info card
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f3460,#16213e); border:1px solid #1e3a5f; border-radius:16px; padding:30px; text-align:center; margin-bottom:24px;">
  <div style="font-size:3rem; margin-bottom:12px;">🔐</div>
  <h2 style="color:#00D4FF; margin:0 0 8px 0; font-size:1.6rem;">{APP_NAME}</h2>
  <p style="color:#9ca3af; font-style:italic; margin:0 0 16px 0;">{APP_TAGLINE}</p>
  <div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">
    <span style="background:#00D4FF; color:#000; padding:4px 14px; border-radius:20px; font-size:0.8rem; font-weight:700;">v{APP_VERSION}</span>
    <span style="background:#0f3460; color:#00D4FF; border:1px solid #00D4FF; padding:4px 14px; border-radius:20px; font-size:0.8rem;">B.Tech Major Project</span>
    <span style="background:#0f3460; color:#4ECDC4; border:1px solid #4ECDC4; padding:4px 14px; border-radius:20px; font-size:0.8rem;">{APP_DOMAIN}</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # Details columns
    c1, c2 = st.columns(2)

    with c1:
        section_heading("Project Details")
        details = [
            ("Project Title",     APP_NAME),
            ("Tagline",           APP_TAGLINE),
            ("Version",           APP_VERSION),
            ("Project Type",      "B.Tech Major Project"),
            ("Domain",            APP_DOMAIN),
            ("Core Concept",      APP_CONCEPT),
            ("Primary Method",    APP_METHOD),
        ]
        for label, value in details:
            st.markdown(f"**{label}:** {value}")

    with c2:
        section_heading("Academic Information")
        academic = [
            ("Student Name",  STUDENT_NAME),
            ("Roll Number",   ROLL_NUMBER),
            ("Department",    DEPARTMENT),
            ("College",       COLLEGE),
            ("Project Guide", GUIDE_NAME),
            ("Academic Year", ACADEMIC_YEAR),
        ]
        for label, value in academic:
            st.markdown(f"**{label}:** {value}")

    section_heading("Project Objectives")
    objectives = [
        "Implement Security by Design for software architecture assessment.",
        "Automate STRIDE threat modeling without requiring code or deployment.",
        "Provide transparent, explainable risk scoring (Likelihood × Impact).",
        "Map threats to curated security design patterns.",
        "Generate professional security assessment reports.",
        "Visualise architecture as an interactive network graph.",
        "Provide an educational security pattern library.",
        "Demonstrate that security issues are cheaper to fix at the design stage.",
    ]
    for i, obj in enumerate(objectives, 1):
        st.markdown(f"{i}. {obj}")

    section_heading("Technology Stack")
    tech = {
        "Language":         "Python 3.11+",
        "Web Framework":    "Streamlit 1.35+",
        "Charts":           "Plotly 5.x",
        "Graph Library":    "NetworkX 3.x",
        "Data Processing":  "Pandas 2.x",
        "YAML Parsing":     "PyYAML 6.x",
        "PDF Generation":   "ReportLab 4.x",
        "Database":         "SQLite3 (built-in)",
        "Testing":          "pytest 7.x",
        "Deployment":       "Streamlit Community Cloud",
    }
    tech_rows = [{"Component": k, "Technology": v} for k, v in tech.items()]
    import pandas as pd
    st.dataframe(pd.DataFrame(tech_rows), use_container_width=True, hide_index=True)

    section_heading("Key Features")
    features = [
        ("📥 Multi-Format Input",         "JSON, YAML, XML, PlantUML architecture files"),
        ("🎯 STRIDE Threat Modeling",      "Automated rule-based detection across 6 categories"),
        ("📊 Risk Assessment",            "Likelihood × Impact scoring with percentage normalisation"),
        ("🗝️ Security Pattern Library",  "24 curated patterns with implementation guidance"),
        ("💡 Smart Recommendations",      "Architecture-specific, prioritised remediation steps"),
        ("🗺️ Interactive Visualization",  "NetworkX + Plotly architecture graph"),
        ("📊 9-Chart Dashboard",          "Real-time charts from analysis results"),
        ("📄 4-Format Reports",           "HTML, PDF, JSON, CSV downloadable reports"),
        ("🕐 Analysis History",           "SQLite persistent storage for previous analyses"),
        ("🚀 One-Click Demo",             "E-Commerce demo requires no file upload"),
    ]
    for icon_title, desc in features:
        st.markdown(f"• **{icon_title}**: {desc}")

    st.markdown("---")
    st.markdown("""
<div style="text-align:center; color:#6b7280; font-size:0.85rem;">
  <p>Security-Centric Architecture Assessment Framework v{} | Academic Project</p>
  <p>Built with Python + Streamlit | Security by Design | STRIDE Threat Modeling</p>
</div>
""".format(APP_VERSION), unsafe_allow_html=True)
