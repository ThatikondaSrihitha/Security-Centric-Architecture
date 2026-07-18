"""Security Dashboard page."""
from __future__ import annotations
import streamlit as st

from page_modules.shared_styles import inject_css, page_header, section_heading
from utils.session_manager import has_analysis, get as ss_get
from visualization.dashboard_charts import (
    stride_distribution, severity_distribution, component_risk_chart,
    risk_matrix, threats_by_component, pattern_usage_chart, risk_gauge,
    encrypted_flows_chart, security_controls_chart,
)


def show() -> None:
    inject_css()
    page_header("📊", "Security Dashboard", "Interactive overview of your architecture's security posture.")

    if not has_analysis():
        _no_analysis()
        return

    # Always read fresh from session state — never use cached variables
    result = st.session_state["analysis_result"]
    arch   = result.architecture
    rs     = result.risk_summary

    # Debug info — shows which analysis is loaded (helps confirm fresh data)
    analysis_ts = st.session_state.get("analysis_ts", "")

    # One-time success toast after completing analysis
    if st.session_state.pop("show_analysis_success", False):
        st.success(
            f"✅ Assessment complete for **{arch.name}** — "
            f"**{len(result.threats)} threats** found | "
            f"Risk Level: **{rs.get('overall_risk_level','N/A')}**"
        )

    # ── Active analysis banner ─────────────────────────────────────────────
    risk_level  = rs.get("overall_risk_level", "Low")
    risk_pct    = rs.get("overall_risk_pct", 0)
    colour_map  = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}
    banner_col  = colour_map.get(risk_level, "#74B9FF")
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f2d5c,#161b22);
            border:1px solid {banner_col}55; border-left:4px solid {banner_col};
            border-radius:10px; padding:12px 18px; margin-bottom:16px;
            display:flex; align-items:center; gap:16px;">
  <div style="font-size:1.8rem;">📊</div>
  <div>
    <div style="color:#9ca3af; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em;">
      Currently Analyzing
    </div>
    <div style="color:#e5e7eb; font-weight:700; font-size:1rem;">{arch.name}</div>
    <div style="color:{banner_col}; font-weight:700; font-size:0.85rem;">
      {risk_level} Risk — {risk_pct:.1f}% &nbsp;|&nbsp;
      <span style="color:#9ca3af; font-weight:400;">{len(result.threats)} threats detected</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Key metrics ────────────────────────────────────────────────────────
    section_heading("Architecture Overview")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Architecture",       arch.name[:20])
    m2.metric("Components",         len(arch.components))
    m3.metric("Data Flows",         len(arch.data_flows))
    m4.metric("Trust Boundaries",   len(arch.trust_boundaries))
    m5.metric("Patterns Recommended",len({m["pattern_name"] for m in result.pattern_mappings}))

    section_heading("Threat Summary")
    t1, t2, t3, t4, t5, t6 = st.columns(6)
    t1.metric("Total Threats",   rs.get("total_threats",  0))
    t2.metric("🔴 Critical",     rs.get("critical_count", 0))
    t3.metric("🟠 High",         rs.get("high_count",     0))
    t4.metric("🟡 Medium",       rs.get("medium_count",   0))
    t5.metric("🟢 Low",          rs.get("low_count",      0))
    t6.metric("Avg Risk Score",  f"{rs.get('avg_risk_score', 0):.1f}/25")

    # Overall risk gauge
    section_heading("Overall Risk Level")
    g_col, r_col = st.columns([1, 2])
    with g_col:
        fig = risk_gauge(risk_pct, risk_level)
        st.plotly_chart(fig, use_container_width=True)
        colour = colour_map.get(risk_level, "#74B9FF")
        st.markdown(f"""
<div style="text-align:center; background:#161b22; border:2px solid {colour}; border-radius:12px; padding:12px; margin-top:-10px;">
  <div style="font-size:2rem; font-weight:900; color:{colour};">{risk_pct:.1f}%</div>
  <div style="color:#9ca3af; font-size:0.85rem;">Overall Risk Score</div>
  <div style="color:{colour}; font-weight:700; font-size:1.1rem;">{risk_level} Risk</div>
  <div style="color:#6b7280; font-size:0.75rem; margin-top:4px;">Avg: {rs.get('avg_risk_score',0):.2f} / 25 × 100</div>
</div>
""", unsafe_allow_html=True)

    with r_col:
        st.plotly_chart(risk_matrix(result.threats), use_container_width=True)

    # ── Charts row 1 ───────────────────────────────────────────────────────
    section_heading("STRIDE & Severity Analysis")
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(stride_distribution(result.threats), use_container_width=True)
    with ch2:
        st.plotly_chart(severity_distribution(result.threats), use_container_width=True)

    # ── Charts row 2 ───────────────────────────────────────────────────────
    section_heading("Component & Pattern Analysis")
    ch3, ch4 = st.columns(2)
    with ch3:
        st.plotly_chart(component_risk_chart(rs), use_container_width=True)
    with ch4:
        st.plotly_chart(threats_by_component(result.threats), use_container_width=True)

    section_heading("Pattern Recommendations")
    st.plotly_chart(pattern_usage_chart(result.pattern_mappings), use_container_width=True)

    # ── Charts row 3 ───────────────────────────────────────────────────────
    section_heading("Security Controls Status")
    ch5, ch6 = st.columns(2)
    with ch5:
        st.plotly_chart(encrypted_flows_chart(arch), use_container_width=True)
    with ch6:
        st.plotly_chart(security_controls_chart(arch), use_container_width=True)

    # ── STRIDE breakdown table ─────────────────────────────────────────────
    section_heading("STRIDE Category Breakdown")
    stride_data = rs.get("stride_risk", {})
    if stride_data:
        import pandas as pd
        rows = []
        for cat, info in stride_data.items():
            rows.append({
                "STRIDE Category": cat,
                "Threat Count":    info["count"],
                "Max Risk Score":  info["max_score"],
                "Risk Level":      info["level"],
            })
        df = pd.DataFrame(rows).sort_values("Max Risk Score", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)


def _no_analysis() -> None:
    st.info("No analysis results found. Run an assessment first.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 Run E-Commerce Demo", type="primary"):
            st.session_state["current_page"]  = "New Architecture Assessment"
            st.session_state["trigger_demo"]  = True
            st.rerun()
    with c2:
        if st.button("📁 Upload Architecture"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.rerun()
