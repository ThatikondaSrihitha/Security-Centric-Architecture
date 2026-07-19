"""Risk Assessment page."""
from __future__ import annotations
import pandas as pd
import streamlit as st

from page_modules.shared_styles import inject_css, page_header, section_heading
from utils.session_manager import has_analysis, get as ss_get
from visualization.dashboard_charts import risk_gauge, risk_matrix, component_risk_chart, severity_distribution


def show() -> None:
    inject_css()
    page_header("Risk Assessment", "Detailed risk scores, classification, and component-level risk analysis.")

    if not has_analysis():
        st.info("Run an architecture assessment first.")
        if st.button("Run E-Commerce Demo"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
        return

    result = st.session_state["analysis_result"]
    rs     = result.risk_summary
    arch   = result.architecture

    # ── Risk formula explanation ───────────────────────────────────────────
    section_heading("Risk Calculation Formula")
    st.markdown("""
<div style="background:#0f2d5c; border:1px solid #1e3a5f; border-radius:12px; padding:20px; margin-bottom:16px;">
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; text-align:center;">
    <div>
      <div style="color:#00D4FF; font-size:0.85rem; font-weight:700; text-transform:uppercase;">Formula</div>
      <div style="color:#e5e7eb; font-size:1.3rem; font-weight:900; margin-top:6px;">Risk = Likelihood × Impact</div>
      <div style="color:#9ca3af; font-size:0.8rem;">Both scored 1–5 (max = 25)</div>
    </div>
    <div>
      <div style="color:#00D4FF; font-size:0.85rem; font-weight:700; text-transform:uppercase;">Classification</div>
      <div style="margin-top:6px; font-size:0.85rem; line-height:1.8;">
        <span style="color:#00C853">■ Low: 1–4</span><br>
        <span style="color:#FFD700">■ Medium: 5–9</span><br>
        <span style="color:#FF8C00">■ High: 10–16</span><br>
        <span style="color:#FF2D2D">■ Critical: 17–25</span>
      </div>
    </div>
    <div>
      <div style="color:#00D4FF; font-size:0.85rem; font-weight:700; text-transform:uppercase;">Normalisation</div>
      <div style="color:#e5e7eb; font-size:1.3rem; font-weight:900; margin-top:6px;">Avg Score / 25 × 100</div>
      <div style="color:#9ca3af; font-size:0.8rem;">Produces 0–100% risk percentage</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Overall risk ──────────────────────────────────────────────────────
    section_heading("Overall Risk Summary")
    g1, g2 = st.columns([1, 2])
    with g1:
        st.plotly_chart(risk_gauge(rs.get("overall_risk_pct",0), rs.get("overall_risk_level","Low")), use_container_width=True)
    with g2:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Threats",   rs.get("total_threats",  0))
        m2.metric("Avg Risk Score",  f"{rs.get('avg_risk_score',0):.2f}")
        m3.metric("Max Risk Score",  rs.get("max_risk_score",  0))
        m4.metric("Risk Percentage", f"{rs.get('overall_risk_pct',0):.1f}%")
        m5, m6, m7, m8 = st.columns(4)
        m5.metric("Critical", rs.get("critical_count", 0))
        m6.metric("High",     rs.get("high_count",     0))
        m7.metric("Medium",   rs.get("medium_count",   0))
        m8.metric("Low",      rs.get("low_count",      0))

    # ── Charts ────────────────────────────────────────────────────────────
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(severity_distribution(result.threats), use_container_width=True)
    with ch2:
        st.plotly_chart(risk_matrix(result.threats), use_container_width=True)

    st.plotly_chart(component_risk_chart(rs), use_container_width=True)

    # ── Component risk table ───────────────────────────────────────────────
    section_heading("Component Risk Details")
    comp_risk = rs.get("component_risk", {})
    if comp_risk:
        rows = []
        for name, info in sorted(comp_risk.items(), key=lambda x: x[1]["score"], reverse=True):
            rows.append({
                "Component":   name,
                "Max Risk Score": info["score"],
                "Threat Count":   info["count"],
                "Risk Level":     info["level"],
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ── STRIDE risk table ──────────────────────────────────────────────────
    section_heading("STRIDE Category Risk")
    stride_risk = rs.get("stride_risk", {})
    if stride_risk:
        rows2 = []
        for cat, info in sorted(stride_risk.items(), key=lambda x: x[1]["max_score"], reverse=True):
            rows2.append({
                "STRIDE Category": cat,
                "Threat Count":    info["count"],
                "Max Risk Score":  info["max_score"],
                "Risk Level":      info["level"],
            })
        df2 = pd.DataFrame(rows2)
        st.dataframe(df2, use_container_width=True, hide_index=True)

    # ── Individual threat scores ───────────────────────────────────────────
    section_heading("All Threat Risk Scores")
    rows3 = []
    for t in sorted(result.threats, key=lambda x: x.risk_score, reverse=True):
        rows3.append({
            "Threat":     t.title,
            "Component":  t.affected_component,
            "STRIDE":     t.stride_category,
            "Likelihood": t.likelihood,
            "Impact":     t.impact,
            "Risk Score": t.risk_score,
            "Severity":   t.severity,
        })
    df3 = pd.DataFrame(rows3)
    st.dataframe(df3, use_container_width=True, hide_index=True)
