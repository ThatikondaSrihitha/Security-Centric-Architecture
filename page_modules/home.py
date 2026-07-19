"""Home page."""
from __future__ import annotations
import streamlit as st
from page_modules.shared_styles import inject_css


def show() -> None:
    inject_css()

    st.markdown("""
<div style="background:linear-gradient(135deg,#0a1628 0%,#0d1f3c 60%,#080c14 100%);
            border-radius:18px;padding:56px 48px 48px;text-align:center;
            margin-bottom:30px;border:1px solid rgba(0,212,255,0.1);
            box-shadow:0 20px 60px rgba(0,0,0,0.4);">
  <div style="display:inline-block;background:rgba(0,212,255,0.07);
              border:1px solid rgba(0,212,255,0.18);color:#00D4FF;
              font-size:0.68rem;font-weight:700;letter-spacing:0.14em;
              text-transform:uppercase;padding:4px 14px;border-radius:4px;
              margin-bottom:18px;">B.Tech Major Project &mdash; Cybersecurity</div>
  <h1 style="color:#e2e8f0;font-size:2.5rem;font-weight:800;
             margin:0 0 14px 0;letter-spacing:-0.03em;line-height:1.15;">
    Security-Centric Architecture<br>
    <span style="color:#00D4FF;">Assessment Framework</span>
  </h1>
  <p style="color:#64748b;font-size:1rem;margin:0 auto 32px;
            max-width:520px;line-height:1.7;font-weight:400;">
    Identify security threats in your software architecture
    <strong style="color:#94a3b8;font-weight:500;">before a single line of code is written.</strong>
  </p>
  <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;">
    <span style="background:rgba(0,212,255,0.07);color:#00D4FF;
                 border:1px solid rgba(0,212,255,0.18);
                 padding:4px 12px;border-radius:4px;font-size:0.75rem;
                 font-weight:600;letter-spacing:0.04em;">STRIDE Threat Modeling</span>
    <span style="background:rgba(74,222,128,0.07);color:#4ade80;
                 border:1px solid rgba(74,222,128,0.18);
                 padding:4px 12px;border-radius:4px;font-size:0.75rem;
                 font-weight:600;letter-spacing:0.04em;">Security by Design</span>
    <span style="background:rgba(251,191,36,0.07);color:#fbbf24;
                 border:1px solid rgba(251,191,36,0.18);
                 padding:4px 12px;border-radius:4px;font-size:0.75rem;
                 font-weight:600;letter-spacing:0.04em;">Risk Assessment</span>
    <span style="background:rgba(78,205,196,0.07);color:#4ECDC4;
                 border:1px solid rgba(78,205,196,0.18);
                 padding:4px 12px;border-radius:4px;font-size:0.75rem;
                 font-weight:600;letter-spacing:0.04em;">Pattern Mapping</span>
    <span style="background:rgba(192,132,252,0.07);color:#c084fc;
                 border:1px solid rgba(192,132,252,0.18);
                 padding:4px 12px;border-radius:4px;font-size:0.75rem;
                 font-weight:600;letter-spacing:0.04em;">Downloadable Reports</span>
  </div>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Run E-Commerce Demo", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
    with c2:
        if st.button("Start New Assessment", use_container_width=True):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.rerun()
    with c3:
        if st.button("AI Security Assistant", use_container_width=True):
            st.session_state["current_page"] = "AI Security Assistant"
            st.rerun()
    with c4:
        if st.button("View Pattern Library", use_container_width=True):
            st.session_state["current_page"] = "Architecture Patterns"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""<div style="color:#334155;font-size:0.68rem;font-weight:700;
    text-transform:uppercase;letter-spacing:0.12em;margin-bottom:14px;">
    How It Works</div>""", unsafe_allow_html=True)

    steps = [
        ("01", "Input",           "JSON, YAML, XML or PlantUML"),
        ("02", "Parse",           "Extract components and data flows"),
        ("03", "STRIDE + DREAD",  "Apply 20+ threat detection rules"),
        ("04", "Risk Scoring",    "Likelihood x Impact calculation"),
        ("05", "Attack Trees",    "Visualize attack paths"),
        ("06", "Patterns",        "Map to security design patterns"),
        ("07", "Recommendations", "Prioritized remediation steps"),
        ("08", "Report",          "Download HTML, PDF, JSON, CSV"),
    ]
    cols = st.columns(len(steps))
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
<div style="background:rgba(15,25,40,0.7);border:1px solid rgba(0,212,255,0.07);
            border-radius:10px;padding:16px 10px;text-align:center;height:110px;
            display:flex;flex-direction:column;align-items:center;justify-content:center;">
  <div style="color:rgba(0,212,255,0.35);font-size:0.6rem;font-weight:700;
              letter-spacing:0.1em;margin-bottom:5px;">{num}</div>
  <div style="color:#cbd5e1;font-weight:600;font-size:0.78rem;margin-bottom:4px;">{title}</div>
  <div style="color:#334155;font-size:0.66rem;line-height:1.4;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""<div style="color:#334155;font-size:0.68rem;font-weight:700;
    text-transform:uppercase;letter-spacing:0.12em;margin-bottom:14px;">
    Why Use This Framework</div>""", unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    benefits = [
        ("#00D4FF", "Security Before Coding",
         "Identify architectural flaws at design stage. Up to 100x cheaper to fix than post-deployment."),
        ("#4ade80", "Fully Automated",
         "No manual threat modeling. Upload your architecture and receive results in seconds."),
        ("#fbbf24", "Professional Reports",
         "Download PDF, HTML, JSON, and CSV reports suitable for academic and professional review."),
    ]
    for col, (colour, title, desc) in zip([b1, b2, b3], benefits):
        with col:
            st.markdown(f"""
<div style="background:rgba(15,25,40,0.5);border:1px solid rgba(255,255,255,0.04);
            border-top:2px solid {colour};border-radius:10px;
            padding:20px 18px 18px;height:140px;">
  <div style="color:{colour};font-weight:700;font-size:0.86rem;margin-bottom:7px;">{title}</div>
  <div style="color:#475569;font-size:0.78rem;line-height:1.55;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:rgba(10,20,40,0.5);border:1px solid rgba(0,212,255,0.07);
            border-radius:10px;padding:18px 24px;text-align:center;">
  <p style="color:#334155;font-size:0.84rem;margin:0;">
    Click <strong style="color:#00D4FF;font-weight:600;">Run E-Commerce Demo</strong>
    for an instant end-to-end demonstration with no file upload required.
  </p>
</div>
""", unsafe_allow_html=True)
