"""STRIDE Threat Analysis page."""
from __future__ import annotations
from collections import Counter
import pandas as pd
import streamlit as st

from page_modules.shared_styles import inject_css, page_header, section_heading, severity_badge
from utils.session_manager import has_analysis, get as ss_get


_STRIDE_ICONS = {
    "Spoofing":             "🎭",
    "Tampering":            "🔧",
    "Repudiation":          "🙈",
    "InformationDisclosure":"👁️",
    "DenialOfService":      "🚫",
    "ElevationOfPrivilege": "🔑",
}

_STRIDE_DESC = {
    "Spoofing":              "Impersonating a user, device, or service identity",
    "Tampering":             "Unauthorised modification of data or code",
    "Repudiation":           "Denying having performed an action",
    "InformationDisclosure": "Unauthorised access to confidential data",
    "DenialOfService":       "Disrupting availability of the system",
    "ElevationOfPrivilege":  "Gaining more permissions than granted",
}


def show() -> None:
    inject_css()
    page_header("🎯", "STRIDE Threat Analysis", "Rule-based detection of security threats across all 6 STRIDE categories.")

    if not has_analysis():
        st.info("Run an architecture assessment first.")
        if st.button("🚀 Run E-Commerce Demo"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
        return

    result  = st.session_state["analysis_result"]
    threats = result.threats

    # ── Summary counters ──────────────────────────────────────────────────
    section_heading("Threat Summary")
    col_total, col_c, col_h, col_m, col_l = st.columns(5)
    counts = Counter(t.severity for t in threats)
    col_total.metric("Total Threats",   len(threats))
    col_c.metric("🔴 Critical", counts.get("Critical", 0))
    col_h.metric("🟠 High",     counts.get("High",     0))
    col_m.metric("🟡 Medium",   counts.get("Medium",   0))
    col_l.metric("🟢 Low",      counts.get("Low",      0))

    # ── STRIDE category cards ─────────────────────────────────────────────
    section_heading("STRIDE Category Overview")
    stride_counts = Counter(t.stride_category for t in threats)
    cats = list(_STRIDE_ICONS.keys())
    cols = st.columns(len(cats))
    for col, cat in zip(cols, cats):
        cnt = stride_counts.get(cat, 0)
        with col:
            st.markdown(f"""
<div style="background:#161b22; border:1px solid #30363d; border-radius:10px; padding:14px; text-align:center;">
  <div style="font-size:1.8rem">{_STRIDE_ICONS[cat]}</div>
  <div style="color:#00D4FF; font-weight:700; font-size:0.8rem; margin:4px 0;">{cat}</div>
  <div style="color:#e5e7eb; font-size:1.6rem; font-weight:900;">{cnt}</div>
  <div style="color:#6b7280; font-size:0.7rem;">{_STRIDE_DESC.get(cat,'')[:30]}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filters ───────────────────────────────────────────────────────────
    section_heading("Threat Details")
    f1, f2, f3 = st.columns(3)
    sel_cat = f1.selectbox("Filter by STRIDE", ["All"] + sorted(set(t.stride_category for t in threats)))
    sel_sev = f2.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"])
    search  = f3.text_input("Search threats", placeholder="component name or keyword…")

    filtered = threats
    if sel_cat != "All":
        filtered = [t for t in filtered if t.stride_category == sel_cat]
    if sel_sev != "All":
        filtered = [t for t in filtered if t.severity == sel_sev]
    if search:
        s = search.lower()
        filtered = [t for t in filtered if s in t.title.lower()
                    or s in t.affected_component.lower()
                    or s in t.description.lower()]

    st.markdown(f"**Showing {len(filtered)} of {len(threats)} threats**")

    # ── Threat cards ──────────────────────────────────────────────────────
    for t in filtered:
        sev_colour = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(t.severity,"#aaa")
        with st.expander(
            f"{_STRIDE_ICONS.get(t.stride_category,'⚠️')} [{t.severity}] {t.title} — {t.affected_component}",
            expanded=False,
        ):
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**STRIDE**<br>{t.stride_category}", unsafe_allow_html=True)
            c2.markdown(f"**Severity**<br>{severity_badge(t.severity)}", unsafe_allow_html=True)
            c3.markdown(f"**Risk Score**<br><span style='color:{sev_colour};font-size:1.3rem;font-weight:900'>{t.risk_score}/25</span>", unsafe_allow_html=True)
            c4.markdown(f"**Likelihood × Impact**<br>{t.likelihood} × {t.impact} = {t.risk_score}", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f"**🔎 Description:** {t.description}")
            st.markdown(f"**📍 Affected Component:** `{t.affected_component}`")

            tab_ev, tab_mit, tab_pat = st.tabs(["📋 Evidence", "💡 Mitigation", "🗺️ Patterns"])
            with tab_ev:
                st.markdown(f"""
<div style="background:#0f2d5c; border-left:4px solid {sev_colour}; padding:12px 16px; border-radius:6px; font-family:monospace; font-size:0.87rem;">
{t.evidence}
</div>
""", unsafe_allow_html=True)
                st.markdown(f"**Detection Rule:** {t.detection_reason}")
            with tab_mit:
                st.markdown(t.mitigation or "_No mitigation specified._")
                st.markdown(f"**Expected Improvement:** {t.potential_impact}")
            with tab_pat:
                if t.recommended_patterns:
                    for p in t.recommended_patterns:
                        st.markdown(f"• 🔑 **{p}**")
                else:
                    st.markdown("_No patterns mapped._")

    # ── Full threat table ─────────────────────────────────────────────────
    section_heading("All Threats Table")
    rows = []
    for t in threats:
        rows.append({
            "ID":        t.id,
            "STRIDE":    t.stride_category,
            "Title":     t.title,
            "Component": t.affected_component,
            "Severity":  t.severity,
            "Risk":      t.risk_score,
            "L×I":       f"{t.likelihood}×{t.impact}",
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
