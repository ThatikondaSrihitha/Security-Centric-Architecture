"""
Architecture Visualization — Enhanced with multiple views, threat overlay,
zone layout, security heatmap, and component radar charts.
"""
from __future__ import annotations
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from page_modules.shared_styles import inject_css, page_header, section_heading
from visualization.architecture_graph import build_graph

_BG = "#0d1117"
_GRID = "#1f2937"
_TEXT = "#e5e7eb"


def show() -> None:
    inject_css()
    page_header("Architecture Visualization",
                "Interactive multi-view visualization of your architecture's structure and security posture.")

    if not st.session_state.get("analysis_result"):
        st.info("Run an architecture assessment first to see the visualization.")
        if st.button("Run E-Commerce Demo", use_container_width=True):
            st.session_state["current_page"] = "New Architecture Assessment"
            st.session_state["trigger_demo"] = True
            st.rerun()
        return

    result = st.session_state["analysis_result"]
    arch   = result.architecture
    rs     = result.risk_summary

    # ── Stats bar ─────────────────────────────────────────────────────────
    section_heading("Architecture Overview")
    s1, s2, s3, s4, s5, s6 = st.columns(6)
    s1.metric("Components",      len(arch.components))
    s2.metric("Data Flows",      len(arch.data_flows))
    s3.metric("Trust Boundaries",len(arch.trust_boundaries))
    s4.metric("Internet-Facing", sum(1 for c in arch.components if c.internet_facing))
    s5.metric("Total Threats",   len(result.threats))
    level = rs.get("overall_risk_level", "N/A")
    col   = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(level,"#74B9FF")
    s6.markdown(f"""
<div style="background:linear-gradient(135deg,#161b22,#1a2332); border:1px solid {col}44;
            border-radius:12px; padding:14px 16px; text-align:center;">
  <div style="color:#9ca3af; font-size:0.75rem; text-transform:uppercase;">Risk Level</div>
  <div style="color:{col}; font-size:1.5rem; font-weight:900;">{level}</div>
  <div style="color:{col}; font-size:0.8rem;">{rs.get('overall_risk_pct',0):.1f}%</div>
</div>
""", unsafe_allow_html=True)

    # ── View tabs ──────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Architecture Graph",
        "🔴 Threat Overlay",
        "🏠 Zone Layout",
        "📊 Security Heatmap",
        "📋 Data Tables",
    ])

    # ─────────────────────────────────────────────────────────────────────
    # TAB 1 — Architecture Graph (interactive with layout options)
    # ─────────────────────────────────────────────────────────────────────
    with tab1:
        section_heading("Interactive Architecture Graph")

        c1, c2 = st.columns([2, 1])
        with c1:
            layout_choice = st.radio(
                "Graph Layout",
                ["spring", "circular", "hierarchical"],
                horizontal=True,
                format_func=lambda x: {
                    "spring": "🔀 Force-Directed",
                    "circular": "⭕ Circular",
                    "hierarchical": "🏗️ Shell/Hierarchical",
                }[x],
            )
        with c2:
            st.markdown("""
<div style="background:#0f2d5c; border:1px solid #1e3a5f; border-radius:8px; padding:10px; font-size:0.82rem;">
is  <span style="color:#00C853">━━</span> Encrypted flow<br>
  <span style="color:#FF2D2D">╌╌</span> Unencrypted flow<br>
  ◆ Internet-facing component<br>
  ● Internal component<br>
  <span style="color:#FF2D2D">Border</span> = Missing controls
</div>
""", unsafe_allow_html=True)

        fig = build_graph(arch, layout=layout_choice)
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": True, "toImageButtonOptions": {
                            "format": "png", "filename": f"{arch.name}_architecture",
                            "height": 600, "width": 1200, "scale": 2,
                        }})

        st.markdown("""
<div style="background:#161b22; border:1px solid #30363d; border-radius:8px;
            padding:10px 14px; font-size:0.82rem; color:#9ca3af;">
  💡 <b style="color:#e5e7eb">Tip:</b> Hover over nodes and edges for details.
  Use the toolbar (top-right of graph) to zoom, pan, or download as PNG.
  Node size = data sensitivity. Border color = missing security controls.
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # TAB 2 — Threat Overlay
    # ─────────────────────────────────────────────────────────────────────
    with tab2:
        section_heading("Threat Overlay Graph")
        st.markdown("""
<div class="info-card">
  <h4>🔴 Threat Overlay Mode</h4>
  <p>Node color shows threat concentration: Red = many threats, Green = few/no threats.
  Node size scales with threat count. Shows which components need immediate attention.</p>
</div>
""", unsafe_allow_html=True)

        # Build threat count per component
        threat_map: dict = defaultdict(int)
        for t in result.threats:
            comp = t.affected_component
            # Handle "A → B" flow format
            if "→" in comp:
                for part in comp.split("→"):
                    threat_map[part.strip()] += 1
            else:
                threat_map[comp] += 1

        fig2 = build_graph(arch, layout="spring", show_threats=True,
                           threat_map=dict(threat_map))
        st.plotly_chart(fig2, use_container_width=True,
                        config={"displayModeBar": True})

        # Top threatened components
        section_heading("Most Threatened Components")
        if threat_map:
            sorted_threats = sorted(threat_map.items(), key=lambda x: x[1], reverse=True)
            bar_fig = go.Figure(go.Bar(
                y=[t[0][:30] for t in sorted_threats[:12]],
                x=[t[1] for t in sorted_threats[:12]],
                orientation="h",
                marker=dict(
                    color=[t[1] for t in sorted_threats[:12]],
                    colorscale=[[0, "#00C853"], [0.4, "#FFD700"],
                                [0.7, "#FF8C00"], [1.0, "#FF2D2D"]],
                    showscale=True,
                    colorbar=dict(title=dict(text="Threats", font=dict(color=_TEXT)), tickfont=dict(color=_TEXT)),
                ),
                text=[str(t[1]) for t in sorted_threats[:12]],
                textposition="outside",
                textfont=dict(color=_TEXT),
            ))
            bar_fig.update_layout(
                title="Threat Count per Component",
                paper_bgcolor=_BG, plot_bgcolor=_BG,
                font=dict(color=_TEXT),
                xaxis=dict(title="Threat Count", gridcolor=_GRID),
                yaxis=dict(autorange="reversed"),
                height=max(300, len(sorted_threats[:12]) * 35),
                margin=dict(l=10, r=60, t=40, b=30),
            )
            st.plotly_chart(bar_fig, use_container_width=True)

    # ─────────────────────────────────────────────────────────────────────
    # TAB 3 — Zone Layout
    # ─────────────────────────────────────────────────────────────────────
    with tab3:
        section_heading("Zone-Based Architecture Layout")
        st.markdown("""
<div class="info-card">
  <h4>🏠 Zone Layout</h4>
  <p>Components arranged by their security zone (External → DMZ → Internal → Data).
  Colored backgrounds show zone boundaries. This matches real network architecture diagrams.</p>
</div>
""", unsafe_allow_html=True)

        fig3 = build_graph(arch, layout="zone")
        st.plotly_chart(fig3, use_container_width=True,
                        config={"displayModeBar": True})

        # Zone summary
        section_heading("Zone Summary")
        zone_data: dict = defaultdict(list)
        for c in arch.components:
            zone_data[c.zone].append(c.name)

        zone_cols = st.columns(len(zone_data) if zone_data else 1)
        zone_colours = {
            "external": "#FF6B35", "dmz": "#FFD700",
            "internal": "#4ECDC4", "data": "#96CEB4",
        }
        for i, (zone, names) in enumerate(zone_data.items()):
            col = zone_colours.get(zone.lower(), "#74B9FF")
            with zone_cols[i % len(zone_cols)]:
                items_html = "".join(
                    f"<div style='color:#9ca3af; font-size:0.8rem; padding:2px 0;'>• {n}</div>"
                    for n in names
                )
                st.markdown(f"""
<div style="background:#161b22; border:1px solid {col}44; border-top:3px solid {col};
            border-radius:10px; padding:14px;">
  <div style="color:{col}; font-weight:700; font-size:0.9rem; margin-bottom:8px; text-transform:uppercase;">
    {zone} Zone
  </div>
  <div style="color:#9ca3af; font-size:0.75rem; margin-bottom:8px;">{len(names)} component(s)</div>
  {items_html}
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # TAB 4 — Security Heatmap
    # ─────────────────────────────────────────────────────────────────────
    with tab4:
        section_heading("Security Controls Heatmap")
        st.markdown("""
<div class="info-card">
  <h4>🌡️ What This Shows</h4>
  <p>Each row = a component. Each column = a security control.
  Green = enabled, Red = missing. Instantly see which components have the most gaps.</p>
</div>
""", unsafe_allow_html=True)

        controls = [
            "Authentication", "Authorization", "Encryption@Rest",
            "Logging", "Rate Limiting", "Input Validation",
        ]
        control_fns = [
            lambda c: c.authentication,
            lambda c: c.authorization,
            lambda c: c.encryption_at_rest,
            lambda c: c.logging_enabled,
            lambda c: c.rate_limiting,
            lambda c: c.input_validation,
        ]

        comp_names = [c.name[:25] for c in arch.components]
        matrix = []
        for c in arch.components:
            row = [int(fn(c)) for fn in control_fns]
            matrix.append(row)

        heatmap_fig = go.Figure(go.Heatmap(
            z=matrix,
            x=controls,
            y=comp_names,
            colorscale=[[0, "#FF2D2D"], [0.5, "#FFD700"], [1, "#00C853"]],
            showscale=True,
            colorbar=dict(
                title=dict(text="Enabled", font=dict(color=_TEXT)),
                tickvals=[0, 1],
                ticktext=["❌ Missing", "✅ Enabled"],
                tickfont=dict(color=_TEXT),
            ),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z}<extra></extra>",
            xgap=3, ygap=3,
        ))

        heatmap_fig.update_layout(
            title=dict(
                text="Security Controls Matrix — Green=Enabled, Red=Missing",
                font=dict(color="#00D4FF", size=13),
            ),
            paper_bgcolor=_BG, plot_bgcolor=_BG,
            font=dict(color=_TEXT, family="Inter, sans-serif"),
            xaxis=dict(side="top", tickfont=dict(size=10, color=_TEXT)),
            yaxis=dict(tickfont=dict(size=10, color=_TEXT), autorange="reversed"),
            height=max(350, len(arch.components) * 38),
            margin=dict(l=10, r=80, t=80, b=20),
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

        # Security score per component
        section_heading("Component Security Score")
        score_rows = []
        for c in arch.components:
            score = sum([
                c.authentication, c.authorization, c.encryption_at_rest,
                c.logging_enabled, c.rate_limiting, c.input_validation
            ])
            pct = round(score / 6 * 100)
            level_c = "Critical" if pct < 34 else "High" if pct < 50 else "Medium" if pct < 84 else "Low"
            score_rows.append({
                "Component": c.name,
                "Type": c.type,
                "Zone": c.zone,
                "Security Score": f"{score}/6",
                "Score %": f"{pct}%",
                "Risk Level": level_c,
                "Internet-Facing": "⚠️ Yes" if c.internet_facing else "No",
                "Sensitivity": c.data_sensitivity,
            })

        score_rows.sort(key=lambda x: int(x["Security Score"].split("/")[0]))
        st.dataframe(pd.DataFrame(score_rows), use_container_width=True, hide_index=True)

        # Radar chart for selected component
        section_heading("Component Security Radar")
        selected_comp = st.selectbox(
            "Select component to inspect",
            [c.name for c in arch.components]
        )
        comp_obj = next((c for c in arch.components if c.name == selected_comp), None)
        if comp_obj:
            radar_values = [
                int(comp_obj.authentication),
                int(comp_obj.authorization),
                int(comp_obj.encryption_at_rest),
                int(comp_obj.logging_enabled),
                int(comp_obj.rate_limiting),
                int(comp_obj.input_validation),
            ]
            score_pct = round(sum(radar_values) / 6 * 100)
            r_col = "#00C853" if score_pct >= 84 else "#FFD700" if score_pct >= 50 else "#FF2D2D"

            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(
                r=radar_values + [radar_values[0]],
                theta=controls + [controls[0]],
                fill="toself",
                fillcolor=f"rgba{tuple(int(r_col.lstrip('#')[i:i+2], 16) for i in (0,2,4)) + (0.2,)}",
                line=dict(color=r_col, width=2),
                name=selected_comp,
            ))
            radar_fig.add_trace(go.Scatterpolar(
                r=[1, 1, 1, 1, 1, 1, 1],
                theta=controls + [controls[0]],
                fill="toself",
                fillcolor="rgba(255,255,255,0.02)",
                line=dict(color="#30363d", width=1, dash="dot"),
                name="Full Coverage",
            ))
            radar_fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True, range=[0, 1],
                        tickvals=[0, 1], ticktext=["Off", "On"],
                        gridcolor="#30363d", color="#9ca3af",
                    ),
                    angularaxis=dict(gridcolor="#30363d", color="#9ca3af"),
                    bgcolor="#161b22",
                ),
                paper_bgcolor=_BG,
                font=dict(color=_TEXT),
                title=dict(
                    text=f"{selected_comp} — Security Score: {score_pct}%",
                    font=dict(color=r_col, size=13),
                ),
                showlegend=True,
                legend=dict(
                    bgcolor="rgba(22,27,34,0.9)", bordercolor="#30363d",
                    font=dict(color=_TEXT, size=10),
                ),
                height=380,
            )
            st.plotly_chart(radar_fig, use_container_width=True)

    # ─────────────────────────────────────────────────────────────────────
    # TAB 5 — Data Tables
    # ─────────────────────────────────────────────────────────────────────
    with tab5:
        section_heading("Component Details")
        comp_rows = []
        for c in arch.components:
            comp_rows.append({
                "Name":          c.name,
                "Type":          c.type,
                "Zone":          c.zone,
                "Internet":      "✅" if c.internet_facing    else "❌",
                "Sensitivity":   c.data_sensitivity,
                "Auth":          "✅" if c.authentication     else "❌",
                "Authz":         "✅" if c.authorization      else "❌",
                "Enc@Rest":      "✅" if c.encryption_at_rest else "❌",
                "Logging":       "✅" if c.logging_enabled    else "❌",
                "Rate Limit":    "✅" if c.rate_limiting      else "❌",
                "Input Val":     "✅" if c.input_validation   else "❌",
            })
        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)

        section_heading("Data Flow Details")
        flow_rows = []
        for df in arch.data_flows:
            flow_rows.append({
                "Source":        df.source,
                "→ Destination": df.destination,
                "Protocol":      df.protocol,
                "Data":          df.data[:45] + "…" if len(df.data) > 45 else df.data,
                "Encrypted":     "✅" if df.encrypted              else "❌",
                "Authenticated": "✅" if df.authenticated           else "❌",
                "Crosses Boundary": "⚠️" if df.crosses_trust_boundary else "✅",
                "Direction":     "↔ Both" if df.bidirectional       else "→ One-way",
            })
        st.dataframe(pd.DataFrame(flow_rows), use_container_width=True, hide_index=True)

        if arch.trust_boundaries:
            section_heading("Trust Boundaries")
            tb_rows = [
                {
                    "Name": tb.name,
                    "From Zone": tb.zone_from,
                    "To Zone": tb.zone_to,
                    "Description": tb.description,
                }
                for tb in arch.trust_boundaries
            ]
            st.dataframe(pd.DataFrame(tb_rows), use_container_width=True, hide_index=True)

        # Flow security summary
        section_heading("Data Flow Security Summary")
        total_flows = len(arch.data_flows)
        enc_flows   = sum(1 for df in arch.data_flows if df.encrypted)
        auth_flows  = sum(1 for df in arch.data_flows if df.authenticated)
        cross_flows = sum(1 for df in arch.data_flows if df.crosses_trust_boundary)

        fc1, fc2, fc3, fc4 = st.columns(4)
        fc1.metric("Total Flows",       total_flows)
        fc2.metric("Encrypted",         f"{enc_flows}/{total_flows}",
                   delta=f"{round(enc_flows/total_flows*100) if total_flows else 0}%")
        fc3.metric("Authenticated",     f"{auth_flows}/{total_flows}",
                   delta=f"{round(auth_flows/total_flows*100) if total_flows else 0}%")
        fc4.metric("Cross-Boundary",    cross_flows)
