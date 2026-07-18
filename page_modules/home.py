"""Home / landing page — clean, modern, minimal."""
from __future__ import annotations
import streamlit as st
from page_modules.shared_styles import inject_css


def show() -> None:
    inject_css()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
<div style="
    background: linear-gradient(135deg, #0f3460 0%, #0d1b2a 60%, #0a0e1a 100%);
    border-radius: 24px;
    padding: 64px 40px 52px;
    text-align: center;
    margin-bottom: 36px;
    border: 1px solid #1e3a5f;
    box-shadow: 0 24px 80px rgba(0,212,255,0.12);
    position: relative;
    overflow: hidden;
">
  <div style="font-size:3.6rem; margin-bottom:18px; line-height:1;">🔐</div>
  <h1 style="
      color:#00D4FF;
      font-size:2.6rem;
      font-weight:900;
      margin:0 0 14px 0;
      letter-spacing:-0.03em;
      line-height:1.15;
  ">
      Security-Centric Architecture<br>Assessment Framework
  </h1>
  <p style="
      color:#9ca3af;
      font-size:1.1rem;
      margin:0 auto 32px;
      max-width:560px;
      line-height:1.7;
  ">
      Identify security threats in your software architecture
      <strong style="color:#e5e7eb;">before a single line of code is written.</strong>
  </p>

  <div style="display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-bottom:32px;">
    <span style="background:rgba(0,212,255,0.15); color:#00D4FF; border:1px solid #00D4FF;
                 padding:5px 16px; border-radius:20px; font-size:0.8rem; font-weight:600;">
      STRIDE Threat Modeling
    </span>
    <span style="background:rgba(0,200,83,0.15); color:#00C853; border:1px solid #00C853;
                 padding:5px 16px; border-radius:20px; font-size:0.8rem; font-weight:600;">
      Security by Design
    </span>
    <span style="background:rgba(255,215,0,0.15); color:#FFD700; border:1px solid #FFD700;
                 padding:5px 16px; border-radius:20px; font-size:0.8rem; font-weight:600;">
      DREAD + OWASP
    </span>
    <span style="background:rgba(255,140,0,0.15); color:#FF8C00; border:1px solid #FF8C00;
                 padding:5px 16px; border-radius:20px; font-size:0.8rem; font-weight:600;">
      AI Assistant
    </span>
    <span style="background:rgba(78,205,196,0.15); color:#4ECDC4; border:1px solid #4ECDC4;
                 padding:5px 16px; border-radius:20px; font-size:0.8rem; font-weight:600;">
      12 Architecture Patterns
    </span>
    <span style="background:rgba(171,71,188,0.15); color:#AB47BC; border:1px solid #AB47BC;
                 padding:5px 16px; border-radius:20px; font-size:0.8rem; font-weight:600;">
      Attack Tree Viz
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── CTA Buttons ───────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    with c1:
        if st.button("▶️  Run E-Commerce Demo", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
    with c2:
        if st.button("🚀  Start Assessment", use_container_width=True):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.rerun()
    with c3:
        if st.button("🤖  AI Assistant", use_container_width=True):
            st.session_state["current_page"] = "AI Security Assistant"
            st.rerun()
    with c4:
        if st.button("🏛️  Pattern Library", use_container_width=True):
            st.session_state["current_page"] = "Architecture Patterns"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Workflow Steps ────────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
  <span style="color:#00D4FF; font-weight:700; font-size:0.85rem;
               text-transform:uppercase; letter-spacing:0.1em;">
    How It Works
  </span>
</div>
""", unsafe_allow_html=True)

    steps = [
        ("📥", "Input",           "Upload JSON, YAML, XML, or PlantUML"),
        ("⚙️", "Parse",           "Extract components & data flows"),
        ("🎯", "STRIDE+DREAD",   "20+ rules + DREAD scoring"),
        ("📊", "Risk + OWASP",   "L×I scoring + OWASP mapping"),
        ("🌳", "Attack Trees",   "Visualize attack paths"),
        ("🗝️", "Patterns",        "12 architecture + 24 security"),
        ("💡", "Recommendations", "Prioritized fix list"),
        ("📄", "Report",          "Download HTML / PDF / CSV"),
    ]

    cols = st.columns(len(steps))
    for i, (col, (icon, title, desc)) in enumerate(zip(cols, steps)):
        connector = "→" if i < len(steps) - 1 else ""
        with col:
            st.markdown(f"""
<div style="
    background: linear-gradient(160deg, #161b22, #0f2d5c);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 20px 12px;
    text-align: center;
    height: 130px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
">
  <div style="font-size:1.7rem; margin-bottom:8px;">{icon}</div>
  <div style="color:#00D4FF; font-weight:700; font-size:0.82rem; margin-bottom:4px;">{title}</div>
  <div style="color:#6b7280; font-size:0.72rem; line-height:1.4;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 3 Key Benefits ────────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
  <span style="color:#00D4FF; font-weight:700; font-size:0.85rem;
               text-transform:uppercase; letter-spacing:0.1em;">
    Why Use This Framework
  </span>
</div>
""", unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    benefits = [
        ("🛡️", "#00D4FF", "Before Code",
         "Finds architectural flaws at the design stage — 10–100× cheaper to fix than post-deployment."),
        ("⚡", "#00C853", "Fully Automated",
         "No manual threat modeling. Upload your architecture and get results in seconds."),
        ("📋", "#FFD700", "Professional Reports",
         "Download PDF, HTML, JSON, and CSV reports ready for academic or client presentation."),
    ]
    for col, (icon, colour, title, desc) in zip([b1, b2, b3], benefits):
        with col:
            st.markdown(f"""
<div style="
    background: #161b22;
    border: 1px solid #30363d;
    border-top: 3px solid {colour};
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    height: 160px;
">
  <div style="font-size:2rem; margin-bottom:10px;">{icon}</div>
  <div style="color:{colour}; font-weight:700; font-size:0.95rem; margin-bottom:8px;">{title}</div>
  <div style="color:#9ca3af; font-size:0.82rem; line-height:1.5;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bottom CTA ────────────────────────────────────────────────────────────
    st.markdown("""
<div style="
    background: linear-gradient(135deg, #0f3460, #0d1b2a);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 32px;
    text-align: center;
">
  <p style="color:#9ca3af; font-size:0.95rem; margin:0;">
    Click <strong style="color:#00D4FF;">▶️ Run E-Commerce Demo</strong> in the sidebar
    for an instant end-to-end demonstration — no file upload needed.
  </p>
</div>
""", unsafe_allow_html=True)
