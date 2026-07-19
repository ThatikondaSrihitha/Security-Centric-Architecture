"""Recommendations page."""
from __future__ import annotations
from collections import defaultdict
import pandas as pd
import streamlit as st

from page_modules.shared_styles import inject_css, page_header, section_heading, severity_badge
from utils.session_manager import has_analysis, get as ss_get


def show() -> None:
    inject_css()
    page_header("Security Recommendations", "Prioritised, architecture-specific remediation recommendations.")

    if not has_analysis():
        st.info("Run an architecture assessment first.")
        if st.button("Run E-Commerce Demo"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
        return

    result  = st.session_state["analysis_result"]
    recs    = result.recommendations
    mappings = result.pattern_mappings

    # Stats
    section_heading("Recommendation Overview")
    from collections import Counter
    counts  = Counter(r["priority"] for r in recs)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Recommendations", len(recs))
    m2.metric("Immediate Actions",  counts.get("Critical", 0))
    m3.metric("High Priority",      counts.get("High",     0))
    m4.metric("Medium Priority",    counts.get("Medium",   0))
    m5.metric("Best Practice",      counts.get("Low",      0))

    # Filter
    f1, f2 = st.columns(2)
    sel_pri  = f1.selectbox("Filter by Priority", ["All","Critical","High","Medium","Low"])
    search   = f2.text_input("Search recommendations", placeholder="component or keyword…")

    filtered = recs
    if sel_pri != "All":
        filtered = [r for r in filtered if r["priority"] == sel_pri]
    if search:
        s = search.lower()
        filtered = [r for r in filtered if s in r["title"].lower() or s in r["component"].lower()]

    st.markdown(f"**Showing {len(filtered)} of {len(recs)} recommendations**")

    # Group by priority group
    groups = defaultdict(list)
    for r in filtered:
        groups[r["group"]].append(r)

    group_order = ["Immediate Actions", "High-Priority Improvements", "Medium-Priority Improvements", "Best-Practice Enhancements"]
    group_icons = {"Immediate Actions":"🚨","High-Priority Improvements":"🔥","Medium-Priority Improvements":"⚠️","Best-Practice Enhancements":"✅"}
    group_colours = {"Immediate Actions":"#FF2D2D","High-Priority Improvements":"#FF8C00","Medium-Priority Improvements":"#FFD700","Best-Practice Enhancements":"#00C853"}

    for group_name in group_order:
        group_recs = groups.get(group_name, [])
        if not group_recs:
            continue

        colour = group_colours[group_name]
        st.markdown(f"""
<div style="border-left:4px solid {colour}; padding:8px 16px; margin:20px 0 8px 0; background:rgba(255,255,255,0.03); border-radius:0 8px 8px 0;">
  <span style="color:{colour}; font-weight:700; font-size:1rem;">{group_icons[group_name]} {group_name}</span>
  <span style="color:#9ca3af; font-size:0.85rem; margin-left:12px;">{len(group_recs)} recommendation(s)</span>
</div>
""", unsafe_allow_html=True)

        for i, r in enumerate(group_recs):
            sev_colour = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(r["priority"],"#aaa")
            with st.expander(f"{'🚨' if r['priority']=='Critical' else '⚠️'} {r['title']}", expanded=(r["priority"]=="Critical")):
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f"**Priority**<br>{severity_badge(r['priority'])}", unsafe_allow_html=True)
                c2.markdown(f"**Component**<br>`{r['component']}`", unsafe_allow_html=True)
                c3.markdown(f"**Pattern**<br>{r['pattern']}", unsafe_allow_html=True)
                c4.markdown(f"**Difficulty**<br>{r['difficulty']}", unsafe_allow_html=True)

                st.markdown("---")
                st.markdown(f"**🔎 Explanation:** {r['explanation']}")

                t1, t2, t3 = st.tabs(["🔧 Implementation", "📈 Expected Improvement", "🔗 Related Threat"])
                with t1:
                    st.markdown(r.get("implementation", "_Not specified._"))
                with t2:
                    st.success(r.get("improvement", "Improves overall security posture."))
                with t3:
                    st.markdown(f"**Threat ID:** `{r['threat_id']}`")
                    st.markdown(f"**Threat Title:** {r['threat_title']}")

    # Pattern mapping table
    section_heading("Threat → Pattern Mapping Table")
    if mappings:
        map_rows = []
        for m in mappings[:50]:  # cap for display
            map_rows.append({
                "Threat":          m["threat_title"][:40],
                "STRIDE":          m["stride_category"],
                "Affected Element":m["affected_element"][:30],
                "Pattern":         m["pattern_name"],
                "Category":        m["pattern_category"],
                "Priority":        m["priority"],
            })
        st.dataframe(pd.DataFrame(map_rows), use_container_width=True, hide_index=True)

    # Full recommendations table
    section_heading("All Recommendations Summary")
    table_rows = []
    for r in recs:
        table_rows.append({
            "ID":         r["id"],
            "Priority":   r["priority"],
            "Title":      r["title"][:50],
            "Component":  r["component"][:30],
            "Pattern":    r["pattern"],
            "Group":      r["group"],
            "Difficulty": r["difficulty"],
            "Status":     r["status"],
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
