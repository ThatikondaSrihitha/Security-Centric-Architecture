"""
Enhanced Architecture Graph — multiple layout options, threat overlay, zone coloring.
"""
from __future__ import annotations
from typing import Dict, List
import networkx as nx
import plotly.graph_objects as go
from core.models import Architecture

_TYPE_COLOURS = {
    "user":     "#00D4FF",
    "actor":    "#00D4FF",
    "external": "#FF6B35",
    "service":  "#4ECDC4",
    "api":      "#45B7D1",
    "database": "#96CEB4",
    "storage":  "#96CEB4",
    "queue":    "#FFEAA7",
    "default":  "#74B9FF",
}

_SENSITIVITY_SIZE = {
    "low": 22, "medium": 30, "high": 40, "critical": 52,
}

_ZONE_BG = {
    "external": "rgba(255,107,53,0.06)",
    "dmz":      "rgba(255,215,0,0.06)",
    "internal": "rgba(78,205,196,0.06)",
    "data":     "rgba(150,206,180,0.08)",
}


def build_graph(arch: Architecture, layout: str = "spring",
                show_threats: bool = False,
                threat_map: Dict[str, int] = None) -> go.Figure:
    """
    Build interactive architecture graph.
    layout: 'spring' | 'circular' | 'hierarchical' | 'zone'
    """
    G = nx.DiGraph()
    for c in arch.components:
        G.add_node(c.name, **c.to_dict())
    for df in arch.data_flows:
        if df.source and df.destination:
            G.add_edge(df.source, df.destination,
                       protocol=df.protocol,
                       encrypted=df.encrypted,
                       crosses=df.crosses_trust_boundary,
                       authenticated=df.authenticated)

    if len(G.nodes) == 0:
        return _empty_fig("No components found in architecture.")

    pos = _get_layout(G, arch, layout)
    comp_map = {c.name: c for c in arch.components}

    traces = []

    # Zone background shapes
    shapes = _zone_shapes(arch, pos, comp_map) if layout == "zone" else []

    # Edge traces
    traces += _edge_traces(G, pos, arch)

    # Node trace
    node_x, node_y = [], []
    node_text, node_hover = [], []
    node_colours, node_sizes, node_symbols = [], [], []
    node_border_colours, node_border_widths = [], []

    for node in G.nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        c = comp_map.get(node)
        label = node[:18] + "…" if len(node) > 18 else node
        node_text.append(label)

        if c:
            base_colour = _TYPE_COLOURS.get(c.type.lower(), _TYPE_COLOURS["default"])
            size = _SENSITIVITY_SIZE.get(c.data_sensitivity.lower(), 26)
            sym = "diamond" if c.internet_facing else "circle"

            # Threat overlay — colour by threat count
            if show_threats and threat_map:
                tc = threat_map.get(node, 0)
                if tc >= 8:
                    base_colour = "#FF2D2D"
                elif tc >= 5:
                    base_colour = "#FF8C00"
                elif tc >= 2:
                    base_colour = "#FFD700"
                else:
                    base_colour = "#00C853"
                size = max(26, min(55, 22 + tc * 3))

            # Border: red if missing critical controls
            missing = sum([
                not c.authentication, not c.authorization,
                not c.encryption_at_rest, not c.logging_enabled
            ])
            border_col = "#FF2D2D" if missing >= 3 else "#FF8C00" if missing >= 2 else "#30363d"
            border_w = 3 if missing >= 2 else 1.5

            sec_score = sum([
                c.authentication, c.authorization, c.encryption_at_rest,
                c.logging_enabled, c.rate_limiting, c.input_validation
            ])

            hover = (
                f"<b>🔲 {c.name}</b><br>"
                f"─────────────────<br>"
                f"<b>Type:</b> {c.type} &nbsp;|&nbsp; <b>Zone:</b> {c.zone}<br>"
                f"<b>Sensitivity:</b> {c.data_sensitivity}<br>"
                f"<b>Internet-Facing:</b> {'⚠️ Yes' if c.internet_facing else '✅ No'}<br>"
                f"─────────────────<br>"
                f"<b>Security Controls ({sec_score}/6)</b><br>"
                f"{'✅' if c.authentication else '❌'} Authentication &nbsp;"
                f"{'✅' if c.authorization else '❌'} Authorization<br>"
                f"{'✅' if c.encryption_at_rest else '❌'} Encryption@Rest &nbsp;"
                f"{'✅' if c.logging_enabled else '❌'} Logging<br>"
                f"{'✅' if c.rate_limiting else '❌'} Rate Limiting &nbsp;"
                f"{'✅' if c.input_validation else '❌'} Input Validation"
            )
            if show_threats and threat_map:
                tc = threat_map.get(node, 0)
                hover += f"<br>─────────────────<br><b>⚠️ Threats: {tc}</b>"
        else:
            base_colour = _TYPE_COLOURS["default"]
            size = 26
            sym = "circle"
            hover = f"<b>{node}</b>"
            border_col = "#30363d"
            border_w = 1.5

        node_colours.append(base_colour)
        node_sizes.append(size)
        node_symbols.append(sym)
        node_hover.append(hover)
        node_border_colours.append(border_col)
        node_border_widths.append(border_w)

    traces.append(go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hovertext=node_hover,
        hoverinfo="text",
        marker=dict(
            size=node_sizes,
            color=node_colours,
            symbol=node_symbols,
            line=dict(width=node_border_widths, color=node_border_colours),
            opacity=0.95,
        ),
        textfont=dict(color="#e5e7eb", size=10, family="Inter, sans-serif"),
        name="Components",
    ))

    # Legend traces (invisible, for legend display)
    for label, colour, sym in [
        ("User/External", "#00D4FF", "circle"),
        ("Service/API", "#4ECDC4", "circle"),
        ("Database", "#96CEB4", "circle"),
        ("Internet-Facing", "#74B9FF", "diamond"),
        ("Encrypted Flow", "#00FF00", "circle"),
        ("Unencrypted Flow", "#FF4444", "circle"),
    ]:
        traces.append(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=colour, symbol=sym),
            name=label, showlegend=True,
        ))

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            showlegend=True,
            legend=dict(
                bgcolor="rgba(22,27,34,0.9)",
                bordercolor="#30363d",
                borderwidth=1,
                font=dict(color="#9ca3af", size=10),
                x=1.01, y=1,
            ),
            hovermode="closest",
            margin=dict(b=30, l=10, r=120, t=50),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0a0e1a",
            font=dict(color="white", family="Inter, sans-serif"),
            title=dict(
                text=f"{'🔴 Threat Overlay: ' if show_threats else '🗺️ '}{arch.name}",
                font=dict(size=15, color="#00D4FF"),
                x=0.01,
            ),
            shapes=shapes,
            height=560,
        ),
    )
    return fig


def _get_layout(G: nx.DiGraph, arch: Architecture, layout: str) -> dict:
    if layout == "circular":
        try:
            return nx.circular_layout(G, scale=2)
        except Exception:
            pass
    elif layout == "hierarchical":
        try:
            return nx.shell_layout(G, scale=2)
        except Exception:
            pass
    elif layout == "zone":
        return _zone_layout(arch)
    # Default spring
    try:
        return nx.spring_layout(G, seed=42, k=2.2, iterations=60)
    except Exception:
        return {n: (i * 0.4, 0) for i, n in enumerate(G.nodes)}


def _zone_layout(arch: Architecture) -> dict:
    """Arrange components by zone vertically."""
    zone_order = ["external", "dmz", "internal", "data"]
    zone_map: Dict[str, List] = {z: [] for z in zone_order}
    other = []
    for c in arch.components:
        z = c.zone.lower()
        if z in zone_map:
            zone_map[z].append(c.name)
        else:
            other.append(c.name)

    pos = {}
    y_positions = {"external": 3.0, "dmz": 1.5, "internal": 0.0, "data": -1.5}
    for zone, names in zone_map.items():
        n = len(names)
        for i, name in enumerate(names):
            x = (i - (n - 1) / 2) * 1.8
            y = y_positions.get(zone, 0)
            pos[name] = (x, y)
    for i, name in enumerate(other):
        pos[name] = (i * 1.5, -3.0)
    return pos


def _zone_shapes(arch: Architecture, pos: dict, comp_map: dict) -> list:
    """Draw background rectangles per zone."""
    from collections import defaultdict
    zone_positions = defaultdict(list)
    for name, (x, y) in pos.items():
        c = comp_map.get(name)
        zone = c.zone.lower() if c else "other"
        zone_positions[zone].append((x, y))

    shapes = []
    for zone, pts in zone_positions.items():
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        bg = _ZONE_BG.get(zone, "rgba(100,100,100,0.04)")
        shapes.append(dict(
            type="rect",
            x0=min(xs) - 0.9, x1=max(xs) + 0.9,
            y0=min(ys) - 0.6, y1=max(ys) + 0.6,
            fillcolor=bg,
            line=dict(color=bg.replace("0.06", "0.3").replace("0.08", "0.3"), width=1, dash="dot"),
            layer="below",
        ))
    return shapes


def _edge_traces(G: nx.DiGraph, pos: dict, arch: Architecture) -> list:
    traces = []
    df_map = {(df.source, df.destination): df for df in arch.data_flows}

    for src, dst, data in G.edges(data=True):
        if src not in pos or dst not in pos:
            continue
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        df = df_map.get((src, dst))

        encrypted = data.get("encrypted", True)
        crosses   = data.get("crosses", False)
        auth      = data.get("authenticated", True)

        colour = "#00C853" if encrypted else "#FF2D2D"
        width  = 2.5 if crosses else 1.5
        dash   = "solid" if encrypted else "dash"

        if not encrypted and not auth:
            colour = "#FF2D2D"
            width  = 3.0

        hover = (
            f"<b>{src} → {dst}</b><br>"
            f"Protocol: <b>{data.get('protocol', '?')}</b><br>"
            f"{'✅' if encrypted else '❌'} Encrypted &nbsp;|&nbsp; "
            f"{'✅' if auth else '❌'} Authenticated<br>"
            f"{'⚠️ Crosses Trust Boundary' if crosses else 'Same Zone'}"
        )

        traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode="lines",
            line=dict(width=width, color=colour, dash=dash),
            hoverinfo="text", hovertext=hover,
            opacity=0.85, showlegend=False,
        ))

        # Protocol label at midpoint
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        traces.append(go.Scatter(
            x=[mx], y=[my],
            mode="text",
            text=[f"  {data.get('protocol', '')}"],
            textfont=dict(size=8, color="#6b7280"),
            hoverinfo="skip", showlegend=False,
        ))

    return traces


def _empty_fig(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, x=0.5, y=0.5, showarrow=False,
                       font=dict(size=14, color="#9ca3af"))
    fig.update_layout(paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
                      font=dict(color="white"))
    return fig
