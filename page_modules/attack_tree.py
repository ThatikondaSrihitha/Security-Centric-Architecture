"""
Attack Tree Visualization page.
Generates interactive attack trees from STRIDE analysis or manual input.
"""
from __future__ import annotations
from typing import Dict, List, Any
import streamlit as st
import plotly.graph_objects as go

from page_modules.shared_styles import inject_css, page_header, section_heading
from utils.session_manager import has_analysis, get as ss_get

# ── Pre-built attack trees ────────────────────────────────────────────────────

ATTACK_TREES: Dict[str, Dict] = {
    "Unauthorized Data Access": {
        "root": "Gain Unauthorized Access to Sensitive Data",
        "colour": "#FF2D2D",
        "children": [
            {
                "label": "Exploit Authentication Weakness",
                "type": "OR",
                "children": [
                    {"label": "Brute Force Password", "type": "LEAF", "probability": 0.6, "children": []},
                    {"label": "Credential Stuffing", "type": "LEAF", "probability": 0.5, "children": []},
                    {"label": "Phishing Attack", "type": "LEAF", "probability": 0.7, "children": []},
                    {"label": "Session Hijacking", "type": "LEAF", "probability": 0.4, "children": []},
                ],
            },
            {
                "label": "Exploit Authorization Flaw",
                "type": "OR",
                "children": [
                    {"label": "Broken Access Control", "type": "LEAF", "probability": 0.5, "children": []},
                    {"label": "IDOR Vulnerability", "type": "LEAF", "probability": 0.55, "children": []},
                    {"label": "Privilege Escalation", "type": "LEAF", "probability": 0.4, "children": []},
                ],
            },
            {
                "label": "Exploit Data Storage",
                "type": "OR",
                "children": [
                    {"label": "SQL Injection", "type": "LEAF", "probability": 0.65, "children": []},
                    {"label": "Unencrypted DB Access", "type": "LEAF", "probability": 0.45, "children": []},
                    {"label": "Backup File Exposure", "type": "LEAF", "probability": 0.3, "children": []},
                ],
            },
        ],
    },
    "API Service Disruption": {
        "root": "Disrupt API Service Availability",
        "colour": "#FF8C00",
        "children": [
            {
                "label": "Volumetric Attack",
                "type": "OR",
                "children": [
                    {"label": "HTTP Flood (DDoS)", "type": "LEAF", "probability": 0.7, "children": []},
                    {"label": "Amplification Attack", "type": "LEAF", "probability": 0.5, "children": []},
                    {"label": "Slowloris Attack", "type": "LEAF", "probability": 0.4, "children": []},
                ],
            },
            {
                "label": "Resource Exhaustion",
                "type": "AND",
                "children": [
                    {"label": "No Rate Limiting Present", "type": "LEAF", "probability": 0.6, "children": []},
                    {"label": "Large Request Payloads", "type": "LEAF", "probability": 0.5, "children": []},
                ],
            },
            {
                "label": "Logic Bomb / Crash",
                "type": "OR",
                "children": [
                    {"label": "Malformed Input Crash", "type": "LEAF", "probability": 0.4, "children": []},
                    {"label": "Memory Exhaustion", "type": "LEAF", "probability": 0.35, "children": []},
                ],
            },
        ],
    },
    "Identity Spoofing": {
        "root": "Impersonate Legitimate User/Service",
        "colour": "#AB47BC",
        "children": [
            {
                "label": "Steal Credentials",
                "type": "OR",
                "children": [
                    {"label": "Phishing Email", "type": "LEAF", "probability": 0.65, "children": []},
                    {"label": "Keylogger Malware", "type": "LEAF", "probability": 0.4, "children": []},
                    {"label": "Dark Web Purchase", "type": "LEAF", "probability": 0.35, "children": []},
                ],
            },
            {
                "label": "Forge Identity Tokens",
                "type": "OR",
                "children": [
                    {"label": "JWT Algorithm Confusion", "type": "LEAF", "probability": 0.3, "children": []},
                    {"label": "Weak Secret Key Exploit", "type": "LEAF", "probability": 0.4, "children": []},
                    {"label": "Token Replay Attack", "type": "LEAF", "probability": 0.45, "children": []},
                ],
            },
            {
                "label": "Man-in-the-Middle",
                "type": "AND",
                "children": [
                    {"label": "Network Interception Access", "type": "LEAF", "probability": 0.3, "children": []},
                    {"label": "No Certificate Pinning", "type": "LEAF", "probability": 0.5, "children": []},
                ],
            },
        ],
    },
    "Data Tampering": {
        "root": "Modify Data Without Authorization",
        "colour": "#FFA726",
        "children": [
            {
                "label": "Inject Malicious Data",
                "type": "OR",
                "children": [
                    {"label": "SQL Injection", "type": "LEAF", "probability": 0.6, "children": []},
                    {"label": "XSS Attack", "type": "LEAF", "probability": 0.55, "children": []},
                    {"label": "XML/JSON Injection", "type": "LEAF", "probability": 0.4, "children": []},
                ],
            },
            {
                "label": "Intercept and Modify Traffic",
                "type": "AND",
                "children": [
                    {"label": "Network Access", "type": "LEAF", "probability": 0.3, "children": []},
                    {"label": "Unencrypted Channel", "type": "LEAF", "probability": 0.5, "children": []},
                ],
            },
            {
                "label": "Abuse Legitimate Access",
                "type": "OR",
                "children": [
                    {"label": "Insider Threat", "type": "LEAF", "probability": 0.25, "children": []},
                    {"label": "Compromised Account", "type": "LEAF", "probability": 0.45, "children": []},
                ],
            },
        ],
    },
}


def _build_tree_figure(tree_name: str, tree_data: Dict) -> go.Figure:
    """Build a Plotly tree diagram from attack tree data."""
    nodes_x, nodes_y, node_text, node_hover, node_colours, node_sizes = [], [], [], [], [], []
    edge_x, edge_y = [], []
    annotations = []

    root_label = tree_data["root"]
    root_colour = tree_data["colour"]
    children = tree_data["children"]

    # Layout calculations
    def add_node(label, x, y, colour, size, node_type="", probability=None):
        nodes_x.append(x)
        nodes_y.append(y)
        node_text.append(label[:20] + "…" if len(label) > 20 else label)
        hover = f"<b>{label}</b>"
        if node_type:
            hover += f"<br>Type: {node_type}"
        if probability is not None:
            hover += f"<br>Probability: {probability:.0%}"
        node_hover.append(hover)
        node_colours.append(colour)
        node_sizes.append(size)

    def add_edge(x0, y0, x1, y1):
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Root node
    add_node(root_label, 0, 0, root_colour, 30)
    root_pos = (0, 0)

    # Level 1 children (attack vectors)
    n_l1 = len(children)
    l1_spacing = 3.0
    l1_start = -(n_l1 - 1) * l1_spacing / 2

    for i, child in enumerate(children):
        cx = l1_start + i * l1_spacing
        cy = -1.5
        node_type = child.get("type", "OR")
        node_col = "#00D4FF" if node_type == "AND" else "#4ECDC4"
        add_node(child["label"], cx, cy, node_col, 20, node_type)
        add_edge(root_pos[0], root_pos[1], cx, cy)

        # Level 2 (leaf nodes)
        grandchildren = child.get("children", [])
        n_l2 = len(grandchildren)
        l2_spacing = 0.9
        l2_start = cx - (n_l2 - 1) * l2_spacing / 2

        for j, gc in enumerate(grandchildren):
            gx = l2_start + j * l2_spacing
            gy = -3.0
            prob = gc.get("probability", 0.5)
            gc_col = "#FF6B6B" if prob >= 0.6 else "#FFD700" if prob >= 0.4 else "#00C853"
            add_node(gc["label"], gx, gy, gc_col, 14, "LEAF", prob)
            add_edge(cx, cy, gx, gy)

    fig = go.Figure()

    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(color="#30363d", width=1.5),
        hoverinfo="skip",
    ))

    # Nodes
    fig.add_trace(go.Scatter(
        x=nodes_x, y=nodes_y,
        mode="markers+text",
        marker=dict(
            size=node_sizes,
            color=node_colours,
            line=dict(width=2, color="#0d1117"),
            symbol="circle",
        ),
        text=node_text,
        textposition="bottom center",
        hovertext=node_hover,
        hoverinfo="text",
        textfont=dict(color="#e5e7eb", size=9),
    ))

    # Legend annotations
    legend_items = [
        (root_colour, "Root Goal"),
        ("#00D4FF", "AND Gate (all required)"),
        ("#4ECDC4", "OR Gate (any sufficient)"),
        ("#FF6B6B", "High Prob Attack"),
        ("#FFD700", "Medium Prob Attack"),
        ("#00C853", "Low Prob Attack"),
    ]
    for idx, (col, label) in enumerate(legend_items):
        fig.add_annotation(
            x=3.8, y=-idx * 0.35,
            text=f"● {label}",
            showarrow=False,
            font=dict(color=col, size=10),
            xanchor="left",
        )

    fig.update_layout(
        title=dict(text=f"Attack Tree: {tree_name}", font=dict(color="#00D4FF", size=16)),
        showlegend=False,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#e5e7eb"),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-4.5, 5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-3.8, 0.8]),
        height=480,
        margin=dict(l=20, r=120, t=60, b=20),
    )
    return fig


def show() -> None:
    inject_css()
    page_header("Attack Tree Visualization",
                "Visual decomposition of attack paths — understand how threats are realized.")

    tab1, tab2 = st.tabs(["📊 Pre-Built Attack Trees", "🔍 Analysis-Based Trees"])

    with tab1:
        section_heading("Select Attack Scenario")

        col1, col2 = st.columns([2, 1])
        with col1:
            tree_choice = st.selectbox(
                "Attack Scenario",
                list(ATTACK_TREES.keys()),
                help="Select an attack goal to visualize its decomposition"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            show_table = st.checkbox("Show node table", value=False)

        tree = ATTACK_TREES[tree_choice]

        # Info card
        st.markdown(f"""
<div style="background:#0f2d5c; border:1px solid rgba(0,212,255,0.3); border-radius:12px;
            padding:16px; margin-bottom:16px;">
  <b style="color:#00D4FF">Root Goal:</b>
  <span style="color:#e5e7eb; font-size:1.05rem; font-weight:600;"> {tree['root']}</span><br>
  <span style="color:#9ca3af; font-size:0.85rem; margin-top:6px; display:block;">
    Attack paths: {len(tree['children'])} main vectors |
    Leaf nodes: {sum(len(c['children']) for c in tree['children'])} specific attacks
  </span>
</div>
""", unsafe_allow_html=True)

        # Tree visualization
        fig = _build_tree_figure(tree_choice, tree)
        st.plotly_chart(fig, use_container_width=True)

        # Legend explanation
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
<div style="background:#161b22; border:1px solid #30363d; border-radius:10px; padding:14px;">
  <b style="color:#00D4FF">AND Gate (Blue)</b><br>
  <span style="color:#9ca3af; font-size:0.82rem;">ALL child conditions must be true for parent to succeed.</span>
</div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""
<div style="background:#161b22; border:1px solid #30363d; border-radius:10px; padding:14px;">
  <b style="color:#4ECDC4">OR Gate (Teal)</b><br>
  <span style="color:#9ca3af; font-size:0.82rem;">ANY child condition being true is sufficient for parent.</span>
</div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""
<div style="background:#161b22; border:1px solid #30363d; border-radius:10px; padding:14px;">
  <b style="color:#FF6B6B">Leaf Node (Red/Yellow/Green)</b><br>
  <span style="color:#9ca3af; font-size:0.82rem;">Color indicates attack probability: High/Medium/Low.</span>
</div>""", unsafe_allow_html=True)

        if show_table:
            st.markdown("<br>", unsafe_allow_html=True)
            section_heading("Attack Path Details")
            rows = []
            for vec in tree["children"]:
                for leaf in vec.get("children", []):
                    prob = leaf.get("probability", 0.5)
                    rows.append({
                        "Attack Vector": vec["label"],
                        "Specific Attack": leaf["label"],
                        "Gate Type": vec.get("type", "OR"),
                        "Probability": f"{prob:.0%}",
                        "Risk": "High" if prob >= 0.6 else "Medium" if prob >= 0.4 else "Low",
                    })
            import pandas as pd
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with tab2:
        section_heading("Generate from Your Analysis")

        if not has_analysis():
            st.info("Run an architecture assessment first to generate attack trees from your specific threats.")
            if st.button("Run E-Commerce Demo"):
                st.session_state["current_page"] = "New Architecture Assessment"
                st.session_state["trigger_demo"] = True
                st.rerun()
            return

        result = st.session_state["analysis_result"]

        # Group threats by stride category → build mini attack trees
        from collections import defaultdict
        by_stride = defaultdict(list)
        for t in result.threats:
            by_stride[t.stride_category].append(t)

        st.markdown(f"**Architecture:** `{result.architecture.name}` | **Threats:** {len(result.threats)}")

        stride_colours = {
            "Spoofing": "#FF6B6B", "Tampering": "#FFA726", "Repudiation": "#FFEE58",
            "InformationDisclosure": "#AB47BC", "DenialOfService": "#29B6F6",
            "ElevationOfPrivilege": "#EF5350",
        }

        selected_cat = st.selectbox(
            "Select STRIDE Category for Attack Tree",
            [cat for cat in stride_colours if cat in by_stride]
        )

        if selected_cat and selected_cat in by_stride:
            threats = by_stride[selected_cat]
            colour = stride_colours[selected_cat]

            # Build dynamic attack tree
            nodes_x, nodes_y = [0], [-0]
            node_text = [f"Achieve {selected_cat}"]
            node_colours = [colour]
            node_sizes = [30]
            node_hover = [f"<b>Root Goal:</b> Achieve {selected_cat}<br>on {result.architecture.name}"]
            edge_x, edge_y = [], []

            n = len(threats[:8])
            for i, t in enumerate(threats[:8]):
                angle_step = 2.5
                x = (i - (n - 1) / 2) * angle_step
                y = -1.8
                sev_col = {"Critical": "#FF2D2D", "High": "#FF8C00",
                           "Medium": "#FFD700", "Low": "#00C853"}.get(t.severity, "#aaa")
                nodes_x.append(x)
                nodes_y.append(y)
                label = t.title[:22] + "…" if len(t.title) > 22 else t.title
                node_text.append(label)
                node_colours.append(sev_col)
                node_sizes.append(18)
                node_hover.append(
                    f"<b>{t.title}</b><br>Component: {t.affected_component}<br>"
                    f"Severity: {t.severity}<br>Risk: {t.risk_score}/25"
                )
                edge_x.extend([0, x, None])
                edge_y.extend([0, y, None])

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=edge_x, y=edge_y, mode="lines",
                line=dict(color="#30363d", width=1.5), hoverinfo="skip",
            ))
            fig2.add_trace(go.Scatter(
                x=nodes_x, y=nodes_y,
                mode="markers+text",
                marker=dict(size=node_sizes, color=node_colours,
                            line=dict(width=2, color="#0d1117")),
                text=node_text,
                textposition="bottom center",
                hovertext=node_hover, hoverinfo="text",
                textfont=dict(color="#e5e7eb", size=9),
            ))
            fig2.update_layout(
                title=dict(
                    text=f"Attack Tree: {selected_cat} on {result.architecture.name[:30]}",
                    font=dict(color="#00D4FF", size=14)
                ),
                showlegend=False,
                paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
                font=dict(color="#e5e7eb"),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=420,
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Threat list for this category
            import pandas as pd
            rows = [{"Title": t.title, "Component": t.affected_component,
                     "Severity": t.severity, "Risk Score": t.risk_score,
                     "Mitigation": t.mitigation[:60] + "…" if len(t.mitigation) > 60 else t.mitigation}
                    for t in threats]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
