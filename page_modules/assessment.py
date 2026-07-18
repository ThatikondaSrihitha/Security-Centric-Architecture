"""New Architecture Assessment page – upload, sample selection, and manual entry."""
from __future__ import annotations
import json
import time
from pathlib import Path

import streamlit as st

from config import ALLOWED_EXTENSIONS
from core.analyzer import ArchitectureAnalyzer
from core.models import Architecture, Component, DataFlow, TrustBoundary
from core.validators import validate_architecture
from database.db import init_db, save_analysis
from page_modules.shared_styles import inject_css, page_header, section_heading
from parsers.json_parser import JSONParser
from parsers.yaml_parser import YAMLParser
from parsers.xml_parser import XMLParser
from parsers.plantuml_parser import PlantUMLParser
from utils.helpers import validate_upload, sanitise_filename
from utils.session_manager import set as ss_set


_SAMPLES = {
    "E-Commerce System":        "data/sample_ecommerce.json",
    "Online Banking System":    "data/sample_banking.yaml",
    "Hospital Management System":"data/sample_hospital.xml",
    "Microservices Application":"data/sample_microservices.puml",
    "IoT Monitoring System":    "data/sample_iot.json",
}

_PARSER_MAP = {
    ".json": JSONParser,
    ".yaml": YAMLParser,
    ".yml":  YAMLParser,
    ".xml":  XMLParser,
    ".puml": PlantUMLParser,
    ".txt":  PlantUMLParser,
}


def show() -> None:
    inject_css()
    init_db()

    page_header(
        "🔍",
        "New Architecture Assessment",
        "Upload an architecture file, choose a built-in sample, or define your architecture manually.",
    )

    # Check if demo was triggered from Home
    if st.session_state.get("trigger_demo"):
        st.session_state["trigger_demo"] = False
        _run_sample("E-Commerce System")
        return

    tab1, tab2, tab3 = st.tabs(["📁 Upload File", "📋 Sample Architectures", "✏️ Manual Entry"])

    with tab1:
        _upload_tab()
    with tab2:
        _sample_tab()
    with tab3:
        _manual_tab()


# ── Upload tab ────────────────────────────────────────────────────────────────

def _upload_tab() -> None:
    section_heading("Upload Architecture File")
    st.markdown("""
<div class="info-card">
  <h4>📂 Supported Formats</h4>
  <p>JSON, YAML (.yaml/.yml), XML, PlantUML (.puml/.txt)</p>
</div>
""", unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Choose an architecture file",
        type=["json", "yaml", "yml", "xml", "puml", "txt"],
        help="Maximum 10 MB",
    )
    if uploaded:
        ok, err = validate_upload(uploaded.name, uploaded.size)
        if not ok:
            st.error(err)
            return

        # ── Read content immediately and cache in session state ───────────
        # Streamlit re-renders on button click which resets uploaded.read()
        # to empty — reading here before the button guarantees content
        file_key = f"uploaded_content_{uploaded.name}_{uploaded.size}"
        if file_key not in st.session_state:
            raw_bytes = uploaded.read()
            st.session_state[file_key] = raw_bytes
        else:
            raw_bytes = st.session_state[file_key]

        content = raw_bytes.decode("utf-8", errors="replace")

        if not content.strip():
            st.error("File appears to be empty. Please upload a valid architecture file.")
            return

        suffix = Path(sanitise_filename(uploaded.name)).suffix.lower()
        parser_cls = _PARSER_MAP.get(suffix)
        if not parser_cls:
            st.error(f"No parser for '{suffix}'. Supported: {', '.join(_PARSER_MAP.keys())}")
            return

        # Show file preview
        st.markdown(f"""
<div style="background:#0f2d5c; border:1px solid #1e3a5f; border-radius:8px;
            padding:10px 14px; margin:8px 0; font-size:0.85rem;">
  <span style="color:#9ca3af;">📄 File loaded: </span>
  <span style="color:#00D4FF; font-weight:600;">{uploaded.name}</span>
  <span style="color:#9ca3af;"> — {len(content):,} characters | Format: </span>
  <span style="color:#4ECDC4; font-weight:600;">{suffix.upper()}</span>
</div>
""", unsafe_allow_html=True)

        if st.button("🔍 Run Security Assessment", type="primary", use_container_width=True):
            with st.spinner("Parsing architecture…"):
                try:
                    parser = parser_cls()
                    arch   = parser.parse(content)
                    arch.metadata["source_file"] = sanitise_filename(uploaded.name)
                except Exception as e:
                    st.error(f"Parse error: {e}")
                    import traceback
                    with st.expander("Technical details"):
                        st.code(traceback.format_exc())
                    return

            valid, errs = validate_architecture(arch)
            if not valid:
                for e in errs:
                    st.warning(e)
                if not arch.components:
                    return

            # Clear cached file content after successful parse
            st.session_state.pop(file_key, None)
            _run_analysis(arch)


# ── Sample tab ────────────────────────────────────────────────────────────────

def _sample_tab() -> None:
    section_heading("Built-In Sample Architectures")
    choice = st.selectbox("Select a sample architecture", list(_SAMPLES.keys()))
    _show_sample_info(choice)

    if st.button(f"▶️ Run Assessment on {choice}", type="primary"):
        _run_sample(choice)


def _show_sample_info(name: str) -> None:
    info = {
        "E-Commerce System":         "13 components, 13 data flows, 4 trust boundaries. Deliberately includes missing controls for a realistic threat profile.",
        "Online Banking System":     "7 components focusing on PCI-DSS relevant controls and regulatory compliance requirements.",
        "Hospital Management System":"7 components with HIPAA-relevant patient data handling and access control issues.",
        "Microservices Application": "PlantUML-based microservices with 11 components and internal message queue flows.",
        "IoT Monitoring System":     "7 components modelling field devices, edge gateway, and cloud processing with MQTT communication.",
    }
    st.markdown(f"""
<div class="info-card">
  <h4>ℹ️ {name}</h4>
  <p>{info.get(name, '')}</p>
</div>
""", unsafe_allow_html=True)


def _run_sample(name: str) -> None:
    path = Path(_SAMPLES[name])
    if not path.exists():
        st.error(f"Sample file not found: {path}")
        return
    content = path.read_text(encoding="utf-8")
    suffix  = path.suffix.lower()
    parser_cls = _PARSER_MAP.get(suffix, JSONParser)
    try:
        arch = parser_cls().parse(content)
        arch.metadata["source_file"] = path.name
    except Exception as e:
        st.error(f"Failed to load sample: {e}")
        return
    _run_analysis(arch)


# ── Manual tab ────────────────────────────────────────────────────────────────

def _manual_tab() -> None:
    section_heading("Manual Architecture Entry")

    if "manual_arch" not in st.session_state:
        st.session_state["manual_arch"] = {
            "name": "", "description": "",
            "components": [], "data_flows": [],
        }

    ma = st.session_state["manual_arch"]

    c1, c2 = st.columns(2)
    with c1:
        ma["name"]        = st.text_input("Architecture Name *", value=ma["name"])
    with c2:
        ma["description"] = st.text_input("Description", value=ma["description"])

    # Components
    section_heading("Components")
    with st.expander("➕ Add Component", expanded=True):
        cc1, cc2, cc3 = st.columns(3)
        comp_name = cc1.text_input("Component Name *", key="new_comp_name")
        comp_type = cc2.selectbox("Type", ["service","database","api","user","external","queue","storage"], key="new_comp_type")
        comp_desc = cc3.text_input("Description", key="new_comp_desc")

        cc4, cc5, cc6 = st.columns(3)
        comp_sens    = cc4.selectbox("Data Sensitivity", ["low","medium","high","critical"], key="new_comp_sens")
        comp_zone    = cc5.text_input("Zone", value="internal", key="new_comp_zone")
        comp_inet    = cc6.checkbox("Internet-Facing", key="new_comp_inet")

        cc7, cc8, cc9, cc10 = st.columns(4)
        comp_auth  = cc7.checkbox("Authentication",   value=True, key="new_comp_auth")
        comp_authz = cc8.checkbox("Authorization",    value=True, key="new_comp_authz")
        comp_enc   = cc9.checkbox("Encryption@Rest",  key="new_comp_enc")
        comp_log   = cc10.checkbox("Logging",         value=True, key="new_comp_log")

        cc11, cc12 = st.columns(2)
        comp_rate  = cc11.checkbox("Rate Limiting",   key="new_comp_rate")
        comp_iv    = cc12.checkbox("Input Validation",value=True, key="new_comp_iv")

        if st.button("Add Component", key="add_comp_btn"):
            if comp_name.strip():
                ma["components"].append({
                    "name": comp_name.strip(), "type": comp_type,
                    "description": comp_desc, "zone": comp_zone,
                    "internet_facing": comp_inet, "data_sensitivity": comp_sens,
                    "authentication": comp_auth, "authorization": comp_authz,
                    "encryption_at_rest": comp_enc, "logging_enabled": comp_log,
                    "rate_limiting": comp_rate, "input_validation": comp_iv,
                })
                st.success(f"Component '{comp_name}' added.")
            else:
                st.warning("Component Name is required.")

    if ma["components"]:
        st.write(f"**{len(ma['components'])} component(s) defined:**")
        for i, c in enumerate(ma["components"]):
            col_a, col_b = st.columns([4, 1])
            col_a.markdown(f"• **{c['name']}** ({c['type']}, {c['zone']}, sensitivity={c['data_sensitivity']})")
            if col_b.button("❌", key=f"del_comp_{i}"):
                ma["components"].pop(i)
                st.rerun()

    # Data flows
    section_heading("Data Flows")
    comp_names = [c["name"] for c in ma["components"]]
    if len(comp_names) >= 2:
        with st.expander("➕ Add Data Flow", expanded=True):
            df1, df2, df3 = st.columns(3)
            df_src  = df1.selectbox("Source *", comp_names, key="new_df_src")
            df_dst  = df2.selectbox("Destination *", [n for n in comp_names if n != df_src], key="new_df_dst")
            df_proto= df3.selectbox("Protocol", ["HTTPS","HTTP","SQL","gRPC","AMQP","MQTT","WSS","SMTP"], key="new_df_proto")

            df4, df5, df6, df7 = st.columns(4)
            df_data  = st.text_input("Data transferred", key="new_df_data")
            df_enc   = df4.checkbox("Encrypted",          value=True,  key="new_df_enc")
            df_auth  = df5.checkbox("Authenticated",       value=True,  key="new_df_auth")
            df_cross = df6.checkbox("Crosses Trust Boundary",           key="new_df_cross")
            df_bidir = df7.checkbox("Bidirectional",                     key="new_df_bidir")

            if st.button("Add Data Flow", key="add_df_btn"):
                ma["data_flows"].append({
                    "source": df_src, "destination": df_dst,
                    "protocol": df_proto, "data": df_data,
                    "encrypted": df_enc, "authenticated": df_auth,
                    "crosses_trust_boundary": df_cross, "bidirectional": df_bidir,
                })
                st.success(f"Flow {df_src}→{df_dst} added.")
    else:
        st.info("Add at least 2 components to define data flows.")

    if ma["data_flows"]:
        st.write(f"**{len(ma['data_flows'])} flow(s) defined:**")
        for i, df in enumerate(ma["data_flows"]):
            col_a, col_b = st.columns([4, 1])
            col_a.markdown(f"• **{df['source']}** → **{df['destination']}** ({df['protocol']}, enc={df['encrypted']})")
            if col_b.button("❌", key=f"del_df_{i}"):
                ma["data_flows"].pop(i)
                st.rerun()

    # Run
    if st.button("🔍 Run Security Assessment", type="primary", key="run_manual_btn"):
        if not ma["name"].strip():
            st.error("Architecture Name is required.")
            return
        if not ma["components"]:
            st.error("At least one component is required.")
            return
        arch = Architecture(
            name        = ma["name"],
            description = ma.get("description", ""),
        )
        for raw in ma["components"]:
            arch.components.append(Component(**{k: v for k, v in raw.items()}))
        for raw in ma["data_flows"]:
            arch.data_flows.append(DataFlow(**{k: v for k, v in raw.items()}))
        arch.metadata["source_file"] = "manual_entry"
        _run_analysis(arch)


# ── Analysis runner ───────────────────────────────────────────────────────────

def _run_analysis(arch: Architecture) -> None:
    steps = [
        "Validating architecture input",
        "Parsing architecture",
        "Extracting components and data flows",
        "Detecting trust boundaries",
        "Running STRIDE threat analysis",
        "Calculating threat risks",
        "Mapping security patterns",
        "Generating recommendations",
        "Creating visualizations",
        "Saving analysis",
    ]

    # ── Clear previous analysis from session BEFORE running new one ──────
    for key in ["analysis_result", "current_architecture", "current_analysis_id"]:
        if key in st.session_state:
            del st.session_state[key]

    progress = st.progress(0)
    status   = st.empty()

    for i, step in enumerate(steps):
        status.markdown(f"⚙️ **{step}…**")
        progress.progress((i + 1) / len(steps))
        time.sleep(0.18)

    try:
        analyzer = ArchitectureAnalyzer()
        result   = analyzer.analyze(arch)
    except Exception as e:
        st.error(f"Analysis failed: {e}")
        progress.empty()
        status.empty()
        return

    try:
        save_analysis(result)
    except Exception as e:
        st.warning(f"Could not save analysis to history: {e}")

    # ── Write directly to session_state to guarantee fresh values ────────
    import time as _time
    st.session_state["analysis_result"]      = result
    st.session_state["current_architecture"] = arch
    st.session_state["current_analysis_id"]  = result.analysis_id
    st.session_state["demo_loaded"]          = True
    st.session_state["analysis_ts"]          = _time.time()  # force re-render

    progress.progress(1.0)
    status.markdown("✅ **Analysis complete! Redirecting to Dashboard…**")
    time.sleep(0.8)
    progress.empty()
    status.empty()

    # Navigate directly to dashboard
    st.session_state["show_analysis_success"] = True
    st.session_state["current_page"] = "Security Dashboard"
    st.rerun()
