"""Analysis History page."""
from __future__ import annotations
import json
import pandas as pd
import streamlit as st

from database.db import init_db, list_analyses, load_analysis, delete_analysis
from page_modules.shared_styles import inject_css, page_header, section_heading
from utils.session_manager import set as ss_set


def show() -> None:
    inject_css()
    init_db()
    page_header("Analysis History", "View, reload, compare, and manage previous security assessments.")

    analyses = list_analyses()

    if not analyses:
        st.info("No analyses saved yet. Run an assessment to populate history.")
        if st.button("Run E-Commerce Demo"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
        return

    # Summary stats
    section_heading("History Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Analyses",    len(analyses))
    m2.metric("Latest Analysis",   analyses[0]["arch_name"] if analyses else "—")
    m3.metric("Total Threats Found", sum(a["threats"] for a in analyses))

    # Comparison table
    section_heading("All Analyses")
    rows = []
    for a in analyses:
        rows.append({
            "ID":          a["id"],
            "Architecture":a["arch_name"],
            "Date":        a["timestamp"][:16].replace("T"," "),
            "Components":  a["components"],
            "Flows":       a["data_flows"],
            "Threats":     a["threats"],
            "Risk %":      f"{a['risk_score']:.1f}%",
            "Risk Level":  a["risk_level"],
            "Source File": a["filename"] or "—",
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Per-analysis actions
    section_heading("Actions")
    for a in analyses:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        risk_colour = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(a["risk_level"],"#74B9FF")
        col1.markdown(
            f"**{a['arch_name']}** — {a['timestamp'][:10]} "
            f"| {a['threats']} threats "
            f"| <span style='color:{risk_colour}'>{a['risk_level']}</span> risk",
            unsafe_allow_html=True,
        )

        if col2.button("Load", key=f"load_{a['id']}"):
            _reload_analysis(a["id"])

        if col3.button("JSON", key=f"dl_{a['id']}"):
            data = load_analysis(a["id"])
            if data:
                json_str = json.dumps(data, indent=2)
                st.download_button(
                    "Download JSON",
                    data=json_str.encode("utf-8"),
                    file_name=f"{a['arch_name'].replace(' ','_')}_{a['id']}.json",
                    mime="application/json",
                    key=f"dl_btn_{a['id']}",
                )

        if col4.button("Delete", key=f"del_{a['id']}"):
            st.session_state[f"confirm_del_{a['id']}"] = True

        # Confirmation dialog
        if st.session_state.get(f"confirm_del_{a['id']}"):
            st.warning(f"⚠️ Delete analysis for **{a['arch_name']}**? This cannot be undone.")
            yes_col, no_col = st.columns(2)
            if yes_col.button("Yes, Delete", key=f"yes_del_{a['id']}"):
                delete_analysis(a["id"])
                st.session_state[f"confirm_del_{a['id']}"] = False
                st.success("Deleted.")
                st.rerun()
            if no_col.button("Cancel", key=f"no_del_{a['id']}"):
                st.session_state[f"confirm_del_{a['id']}"] = False
                st.rerun()

    st.markdown("---")
    if st.button("Clear All History", type="secondary"):
        st.session_state["confirm_clear_all"] = True

    if st.session_state.get("confirm_clear_all"):
        st.warning("⚠️ This will permanently delete ALL analysis history.")
        c1, c2 = st.columns(2)
        if c1.button("Yes, clear all"):
            for a in analyses:
                delete_analysis(a["id"])
            st.session_state["confirm_clear_all"] = False
            st.success("All history cleared.")
            st.rerun()
        if c2.button("Cancel"):
            st.session_state["confirm_clear_all"] = False
            st.rerun()


def _reload_analysis(analysis_id: str) -> None:
    """Reload a stored analysis into session state."""
    from core.models import Architecture, Component, DataFlow, TrustBoundary, Threat, AnalysisResult

    data = load_analysis(analysis_id)
    if not data:
        st.error("Could not load analysis.")
        return

    try:
        arch_d = data["architecture"]
        arch   = Architecture(
            id          = arch_d.get("id",""),
            name        = arch_d.get("name",""),
            description = arch_d.get("description",""),
            created_at  = arch_d.get("created_at",""),
            metadata    = arch_d.get("metadata",{}),
        )
        for c in arch_d.get("components",[]):
            arch.components.append(Component(**{k:v for k,v in c.items() if k != "metadata"}))
        for df in arch_d.get("data_flows",[]):
            arch.data_flows.append(DataFlow(**{k:v for k,v in df.items() if k != "metadata"}))
        for tb in arch_d.get("trust_boundaries",[]):
            arch.trust_boundaries.append(TrustBoundary(**tb))

        threats = [Threat(**t) for t in data.get("threats", [])]
        result  = AnalysisResult(
            architecture     = arch,
            threats          = threats,
            risk_summary     = data.get("risk_summary", {}),
            pattern_mappings = data.get("pattern_mappings", []),
            recommendations  = data.get("recommendations", []),
            analysis_id      = data.get("analysis_id",""),
            timestamp        = data.get("timestamp",""),
        )
        ss_set("analysis_result",      result)
        ss_set("current_architecture", arch)
        ss_set("current_analysis_id",  result.analysis_id)
        ss_set("current_page",         "Security Dashboard")
        st.success(f"Analysis for '{arch.name}' loaded. Navigating to Dashboard…")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to restore analysis: {e}")
