"""
All Plotly dashboard charts.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from typing import Any, Dict, List

import plotly.graph_objects as go
import plotly.express as px

from core.models import AnalysisResult, Threat

_BG   = "#0d1117"
_GRID = "#1f2937"
_TEXT = "#e5e7eb"

_STRIDE_COLOURS = {
    "Spoofing":             "#FF6B6B",
    "Tampering":            "#FFA726",
    "Repudiation":          "#FFEE58",
    "InformationDisclosure":"#AB47BC",
    "DenialOfService":      "#29B6F6",
    "ElevationOfPrivilege": "#EF5350",
}

_SEV_COLOURS = {
    "Critical": "#FF2D2D",
    "High":     "#FF8C00",
    "Medium":   "#FFD700",
    "Low":      "#00C853",
}


def _base_layout(**kwargs) -> dict:
    base = dict(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=dict(color=_TEXT, family="Inter, sans-serif"),
        margin=dict(l=30, r=20, t=50, b=30),
    )
    base.update(kwargs)
    return base


# ── 1. STRIDE distribution (donut) ───────────────────────────────────────────
def stride_distribution(threats: List[Threat]) -> go.Figure:
    counts = Counter(t.stride_category for t in threats)
    labels = list(counts.keys())
    values = list(counts.values())
    colours = [_STRIDE_COLOURS.get(l, "#74B9FF") for l in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.5,
        marker=dict(colors=colours, line=dict(color=_BG, width=2)),
        textinfo="label+percent",
        hovertemplate="%{label}<br>Count: %{value}<extra></extra>",
    ))
    fig.update_layout(
        title="STRIDE Threat Distribution",
        **_base_layout(),
        showlegend=True,
        legend=dict(orientation="v", font=dict(size=10)),
    )
    return fig


# ── 2. Severity distribution (bar) ───────────────────────────────────────────
def severity_distribution(threats: List[Threat]) -> go.Figure:
    counts = Counter(t.severity for t in threats)
    cats   = ["Critical", "High", "Medium", "Low"]
    vals   = [counts.get(c, 0) for c in cats]
    colours= [_SEV_COLOURS[c] for c in cats]
    fig = go.Figure(go.Bar(
        x=cats, y=vals,
        marker_color=colours,
        text=vals, textposition="outside",
        hovertemplate="%{x}: %{y} threats<extra></extra>",
    ))
    fig.update_layout(
        title="Threat Severity Distribution",
        xaxis_title="Severity",
        yaxis_title="Count",
        **_base_layout(),
    )
    return fig


# ── 3. Component risk ranking ─────────────────────────────────────────────────
def component_risk_chart(risk_summary: Dict) -> go.Figure:
    comp_risk = risk_summary.get("component_risk", {})
    if not comp_risk:
        return _empty_fig("No component risk data")
    items = sorted(comp_risk.items(), key=lambda x: x[1]["score"], reverse=True)[:12]
    names  = [i[0][:25] for i in items]
    scores = [i[1]["score"] for i in items]
    levels = [i[1]["level"] for i in items]
    colours = [_SEV_COLOURS.get(l, "#74B9FF") for l in levels]
    fig = go.Figure(go.Bar(
        y=names, x=scores,
        orientation="h",
        marker_color=colours,
        text=[f"{s} ({l})" for s, l in zip(scores, levels)],
        textposition="outside",
        hovertemplate="%{y}<br>Risk Score: %{x}<extra></extra>",
    ))
    fig.update_layout(
        title="Component Risk Ranking",
        xaxis_title="Max Risk Score",
        yaxis=dict(autorange="reversed"),
        **_base_layout(height=max(350, len(names) * 35)),
    )
    return fig


# ── 4. Likelihood vs Impact risk matrix ──────────────────────────────────────
def risk_matrix(threats: List[Threat]) -> go.Figure:
    x_vals, y_vals, labels, colours, hover = [], [], [], [], []
    for t in threats:
        x_vals.append(t.likelihood)
        y_vals.append(t.impact)
        labels.append(t.title[:20])
        colours.append(_SEV_COLOURS.get(t.severity, "#74B9FF"))
        hover.append(
            f"<b>{t.title}</b><br>Likelihood: {t.likelihood}<br>"
            f"Impact: {t.impact}<br>Risk: {t.risk_score}<br>Severity: {t.severity}"
        )
    fig = go.Figure()
    # Background zones
    for (x0, x1, y0, y1, zone_colour) in [
        (0.5, 2.5, 0.5, 2.5, "rgba(0,200,83,0.08)"),
        (0.5, 2.5, 2.5, 5.5, "rgba(255,215,0,0.08)"),
        (2.5, 5.5, 0.5, 2.5, "rgba(255,215,0,0.08)"),
        (2.5, 5.5, 2.5, 5.5, "rgba(255,45,45,0.12)"),
    ]:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                      fillcolor=zone_colour, line_width=0)

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode="markers",
        marker=dict(size=14, color=colours, opacity=0.85,
                    line=dict(width=1.5, color="white")),
        hovertext=hover,
        hoverinfo="text",
    ))
    fig.update_layout(
        title="Likelihood × Impact Risk Matrix",
        xaxis=dict(title="Likelihood (1–5)", range=[0.5, 5.5],
                   tickvals=[1,2,3,4,5], gridcolor=_GRID),
        yaxis=dict(title="Impact (1–5)", range=[0.5, 5.5],
                   tickvals=[1,2,3,4,5], gridcolor=_GRID),
        **_base_layout(),
    )
    return fig


# ── 5. Threats by component ───────────────────────────────────────────────────
def threats_by_component(threats: List[Threat]) -> go.Figure:
    counts = Counter(t.affected_component for t in threats)
    items  = counts.most_common(12)
    names  = [i[0][:25] for i in items]
    vals   = [i[1] for i in items]
    fig = go.Figure(go.Bar(
        y=names, x=vals, orientation="h",
        marker_color="#00D4FF",
        text=vals, textposition="outside",
    ))
    fig.update_layout(
        title="Threats per Component",
        xaxis_title="Threat Count",
        yaxis=dict(autorange="reversed"),
        **_base_layout(height=max(300, len(names) * 32)),
    )
    return fig


# ── 6. Security pattern usage ─────────────────────────────────────────────────
def pattern_usage_chart(pattern_mappings: List[Dict]) -> go.Figure:
    counts = Counter(m["pattern_name"] for m in pattern_mappings)
    items  = counts.most_common(12)
    names  = [i[0] for i in items]
    vals   = [i[1] for i in items]
    fig = go.Figure(go.Bar(
        x=names, y=vals,
        marker_color="#4ECDC4",
        text=vals, textposition="outside",
    ))
    fig.update_layout(
        title="Recommended Security Patterns",
        xaxis_title="Pattern",
        yaxis_title="Times Recommended",
        xaxis_tickangle=-30,
        **_base_layout(height=380),
    )
    return fig


# ── 7. Risk gauge ─────────────────────────────────────────────────────────────
def risk_gauge(risk_pct: float, risk_level: str) -> go.Figure:
    colour = _SEV_COLOURS.get(risk_level, "#74B9FF")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_pct,
        number={"suffix": "%", "font": {"size": 30, "color": colour}},
        title={"text": f"Overall Risk: {risk_level}"},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": _TEXT},
            "bar":  {"color": colour, "thickness": 0.3},
            "steps": [
                {"range": [0, 16],  "color": "rgba(0,200,83,0.2)"},
                {"range": [16, 36], "color": "rgba(255,215,0,0.2)"},
                {"range": [36, 64], "color": "rgba(255,140,0,0.2)"},
                {"range": [64, 100],"color": "rgba(255,45,45,0.2)"},
            ],
            "threshold": {
                "line": {"color": colour, "width": 4},
                "thickness": 0.8,
                "value": risk_pct,
            },
            "bgcolor": _BG,
        },
    ))
    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font={"color": _TEXT},
        margin=dict(l=20, r=20, t=60, b=20),
        height=280,
    )
    return fig


# ── 8. Encrypted vs unencrypted flows ────────────────────────────────────────
def encrypted_flows_chart(arch) -> go.Figure:
    enc = sum(1 for df in arch.data_flows if df.encrypted)
    unenc = len(arch.data_flows) - enc
    fig = go.Figure(go.Pie(
        labels=["Encrypted", "Unencrypted"],
        values=[enc, unenc],
        hole=0.55,
        marker=dict(
            colors=["#00C853", "#FF2D2D"],
            line=dict(color=_BG, width=2),
        ),
        textinfo="label+percent",
    ))
    fig.update_layout(title="Encrypted vs Unencrypted Data Flows", **_base_layout())
    return fig


# ── 9. Security controls enabled vs missing ─────────────────────────────────
def security_controls_chart(arch) -> go.Figure:
    controls = {
        "Authentication":  (0, 0),
        "Authorization":   (0, 0),
        "Encryption@Rest": (0, 0),
        "Logging":         (0, 0),
        "Rate Limiting":   (0, 0),
        "Input Validation":(0, 0),
    }
    enabled_map  = {
        "Authentication":   lambda c: c.authentication,
        "Authorization":    lambda c: c.authorization,
        "Encryption@Rest":  lambda c: c.encryption_at_rest,
        "Logging":          lambda c: c.logging_enabled,
        "Rate Limiting":    lambda c: c.rate_limiting,
        "Input Validation": lambda c: c.input_validation,
    }
    result = {}
    for name, fn in enabled_map.items():
        enabled  = sum(1 for c in arch.components if fn(c))
        missing  = len(arch.components) - enabled
        result[name] = (enabled, missing)

    cats    = list(result.keys())
    enabled = [result[c][0] for c in cats]
    missing = [result[c][1] for c in cats]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Enabled", x=cats, y=enabled, marker_color="#00C853"))
    fig.add_trace(go.Bar(name="Missing", x=cats, y=missing, marker_color="#FF2D2D"))
    fig.update_layout(
        title="Security Controls: Enabled vs Missing",
        barmode="group",
        yaxis_title="Component Count",
        **_base_layout(),
    )
    return fig


def _empty_fig(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, x=0.5, y=0.5, showarrow=False,
                       font=dict(size=14, color=_TEXT))
    fig.update_layout(**_base_layout())
    return fig
