"""Security Pattern Library page."""
from __future__ import annotations
import streamlit as st

from page_modules.shared_styles import inject_css, page_header, section_heading
from patterns.security_patterns import get_all_patterns


def show() -> None:
    inject_css()
    page_header("Security Pattern Library", "24 curated security design patterns with implementation guidance.")

    all_patterns = get_all_patterns()

    # Stats
    section_heading("Library Overview")
    m1, m2, m3, m4 = st.columns(4)
    cats = {p["category"] for p in all_patterns}
    m1.metric("Total Patterns",    len(all_patterns))
    m2.metric("Categories",        len(cats))
    m3.metric("Critical Priority", sum(1 for p in all_patterns if p["priority"] == "Critical"))
    m4.metric("High Priority",     sum(1 for p in all_patterns if p["priority"] == "High"))

    # Filters
    section_heading("Browse & Filter Patterns")
    f1, f2, f3, f4 = st.columns(4)
    stride_options = ["All","Spoofing","Tampering","Repudiation","InformationDisclosure","DenialOfService","ElevationOfPrivilege"]
    sel_stride = f1.selectbox("STRIDE Category",  stride_options)
    sel_cat    = f2.selectbox("Pattern Category", ["All"] + sorted(cats))
    sel_pri    = f3.selectbox("Priority",         ["All", "Critical", "High", "Medium", "Low"])
    search     = f4.text_input("Search patterns", placeholder="keyword…")

    filtered = all_patterns
    if sel_stride != "All":
        filtered = [p for p in filtered if sel_stride in p.get("stride_categories", [])]
    if sel_cat != "All":
        filtered = [p for p in filtered if p["category"] == sel_cat]
    if sel_pri != "All":
        filtered = [p for p in filtered if p["priority"] == sel_pri]
    if search:
        s = search.lower()
        filtered = [p for p in filtered if s in p["name"].lower() or s in p["description"].lower()]

    st.markdown(f"**Showing {len(filtered)} of {len(all_patterns)} patterns**")
    st.markdown("<br>", unsafe_allow_html=True)

    # Pattern cards
    for p in filtered:
        pri_colour = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(p["priority"],"#74B9FF")
        with st.expander(f"🔑 **{p['name']}** — {p['category']} | Priority: {p['priority']}", expanded=False):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Pattern ID:** `{p['id']}`")
            c2.markdown(f"**Category:** {p['category']}")
            c3.markdown(f"**Priority:** <span style='color:{pri_colour};font-weight:700'>{p['priority']}</span>",
                        unsafe_allow_html=True)

            st.markdown(f"**Description:** {p['description']}")
            st.markdown(f"**Problem Addressed:** {p['problem']}")

            t1, t2, t3, t4 = st.tabs(["🎯 STRIDE Coverage", "🔧 Implementation", "✅ Benefits & Limits", "📝 Example"])
            with t1:
                for cat in p.get("stride_categories", []):
                    st.markdown(f"• {cat}")
                st.markdown(f"**Applicable components:** {', '.join(p.get('component_types',[]))}")
            with t2:
                st.markdown(p.get("implementation", "_Not specified._"))
            with t3:
                st.markdown(f"**✅ Benefits:** {p.get('benefits','')}")
                st.markdown(f"**⚠️ Limitations:** {p.get('limitations','')}")
            with t4:
                st.code(p.get("example", "No example provided."), language="text")

    # Category summary
    section_heading("Patterns by Category")
    cat_rows = []
    for cat in sorted(cats):
        ps = [p for p in all_patterns if p["category"] == cat]
        cat_rows.append({"Category": cat, "Pattern Count": len(ps),
                         "Patterns": ", ".join(p["name"] for p in ps[:3]) + ("…" if len(ps) > 3 else "")})
    import pandas as pd
    st.dataframe(pd.DataFrame(cat_rows), use_container_width=True, hide_index=True)
