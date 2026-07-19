"""Reports generation and download page."""
from __future__ import annotations
from datetime import datetime
import streamlit as st

from page_modules.shared_styles import inject_css, page_header, section_heading
from utils.session_manager import has_analysis, get as ss_get
from reports.report_generator import (
    get_html_report, get_pdf_report, get_json_report,
    get_csv_threats, get_csv_recommendations, build_filename,
)


def show() -> None:
    inject_css()
    page_header("Report Generation", "Download professional security assessment reports in multiple formats.")

    if not has_analysis():
        st.info("Run an architecture assessment first to generate reports.")
        if st.button("Run E-Commerce Demo"):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
        return

    result    = st.session_state["analysis_result"]
    arch_name = result.architecture.name
    rs        = result.risk_summary

    # Summary
    section_heading("Report Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Architecture",  arch_name[:20])
    m2.metric("Threats Found", len(result.threats))
    m3.metric("Risk Level",    rs.get("overall_risk_level","N/A"))
    m4.metric("Recommendations", len(result.recommendations))

    st.markdown("<br>", unsafe_allow_html=True)

    # Report cards
    section_heading("Available Report Formats")

    r1, r2 = st.columns(2)

    with r1:
        st.markdown("""
<div class="info-card">
  <h4>📄 HTML Report</h4>
  <p>Full interactive report with professional styling. Best for viewing in a browser and printing.</p>
</div>
""", unsafe_allow_html=True)
        try:
            html_bytes = get_html_report(result).encode("utf-8")
            fn_html    = build_filename(arch_name, "html")
            st.download_button(
                "Download HTML Report",
                data=html_bytes,
                file_name=fn_html,
                mime="text/html",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"HTML report failed: {e}")

    with r2:
        st.markdown("""
<div class="info-card">
  <h4>📑 PDF Report</h4>
  <p>Clean paginated PDF with cover page, metrics, threats, and recommendations table.</p>
</div>
""", unsafe_allow_html=True)
        try:
            pdf_bytes = get_pdf_report(result)
            fn_pdf    = build_filename(arch_name, "pdf")
            st.download_button(
                "Download PDF Report",
                data=pdf_bytes,
                file_name=fn_pdf,
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"PDF report failed: {e}")

    r3, r4 = st.columns(2)

    with r3:
        st.markdown("""
<div class="info-card">
  <h4>📦 JSON Export</h4>
  <p>Complete structured results including all threats, risk scores, patterns, and recommendations. Machine-readable.</p>
</div>
""", unsafe_allow_html=True)
        try:
            json_str = get_json_report(result)
            fn_json  = build_filename(arch_name, "json")
            st.download_button(
                "Download JSON Export",
                data=json_str.encode("utf-8"),
                file_name=fn_json,
                mime="application/json",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"JSON export failed: {e}")

    with r4:
        st.markdown("""
<div class="info-card">
  <h4>📊 CSV Exports</h4>
  <p>Spreadsheet-compatible threat and recommendation tables for further analysis.</p>
</div>
""", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        try:
            csv_threats = get_csv_threats(result)
            fn_csv_t    = build_filename(arch_name + "_threats", "csv")
            col_a.download_button(
                "Threats CSV",
                data=csv_threats.encode("utf-8"),
                file_name=fn_csv_t,
                mime="text/csv",
                use_container_width=True,
            )
        except Exception as e:
            col_a.error(f"CSV failed: {e}")
        try:
            csv_recs = get_csv_recommendations(result)
            fn_csv_r = build_filename(arch_name + "_recommendations", "csv")
            col_b.download_button(
                "Recommendations CSV",
                data=csv_recs.encode("utf-8"),
                file_name=fn_csv_r,
                mime="text/csv",
                use_container_width=True,
            )
        except Exception as e:
            col_b.error(f"CSV failed: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Report contents preview
    section_heading("Report Contents")
    with st.expander("View Report Sections", expanded=True):
        sections = [
            ("1", "Cover Page", "Analysis ID, date, architecture name"),
            ("2", "Executive Summary", "Key metrics, risk level, threat counts"),
            ("3", "Architecture Overview", "Component table, data flow summary, trust boundaries"),
            ("4", "STRIDE Threat Analysis", "All detected threats with evidence"),
            ("5", "Risk Assessment", "Risk scores, severity distribution, formula explanation"),
            ("6", "Security Pattern Recommendations", "Threat-to-pattern mappings"),
            ("7", "Prioritised Remediation Plan", "Ordered recommendations with implementation guidance"),
            ("8", "Methodology", "STRIDE explanation, risk formula, security by design"),
            ("9", "Assumptions & Limitations", "Scope and constraints"),
            ("10","Conclusion", "Overall security posture summary"),
        ]
        for num, title, desc in sections:
            st.markdown(f"**{num}. {title}** — {desc}")

    # Preview HTML inline
    section_heading("HTML Report Preview")
    with st.expander("HTML Report Preview", expanded=False):
        try:
            html_content = get_html_report(result)
            st.components.v1.html(html_content, height=600, scrolling=True)
        except Exception as e:
            st.error(f"Preview failed: {e}")
