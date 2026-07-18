"""
PDF report generator using ReportLab.
"""
from __future__ import annotations
import io
from datetime import datetime, timezone
from typing import Any, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from core.models import AnalysisResult

_DARK   = colors.HexColor("#0d1117")
_CYAN   = colors.HexColor("#00D4FF")
_GREEN  = colors.HexColor("#00C853")
_RED    = colors.HexColor("#FF2D2D")
_ORANGE = colors.HexColor("#FF8C00")
_YELLOW = colors.HexColor("#FFD700")
_GREY   = colors.HexColor("#9ca3af")
_NAVY   = colors.HexColor("#0f3460")
_WHITE  = colors.white
_LIGHT  = colors.HexColor("#e5e7eb")
_BORDER = colors.HexColor("#30363d")

_SEV_COLOUR = {
    "Critical": _RED,
    "High":     _ORANGE,
    "Medium":   _YELLOW,
    "Low":      _GREEN,
}


def generate_pdf(result: AnalysisResult) -> bytes:
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm,
        title=f"{result.architecture.name} Security Report",
    )

    styles = getSampleStyleSheet()
    body   = ParagraphStyle("body",   parent=styles["Normal"],  textColor=_LIGHT, fontSize=9,  leading=14)
    h1     = ParagraphStyle("h1",     parent=styles["Title"],   textColor=_CYAN,  fontSize=22, spaceAfter=8)
    h2     = ParagraphStyle("h2",     parent=styles["Heading2"],textColor=_CYAN,  fontSize=14, spaceBefore=12, spaceAfter=6)
    h3     = ParagraphStyle("h3",     parent=styles["Heading3"],textColor=colors.HexColor("#4ECDC4"), fontSize=11, spaceBefore=8, spaceAfter=4)
    centre = ParagraphStyle("centre", parent=body, alignment=TA_CENTER)
    small  = ParagraphStyle("small",  parent=body, fontSize=8, textColor=_GREY)

    arch   = result.architecture
    rs     = result.risk_summary
    now    = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    story: List[Any] = []

    # ── Cover ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("🔐 Security Assessment Report", h1))
    story.append(Paragraph(arch.name, ParagraphStyle("sub", parent=h1, fontSize=16, textColor=_LIGHT)))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(f"Analysis ID: {result.analysis_id}", centre))
    story.append(Paragraph(f"Generated: {now}", centre))
    story.append(Paragraph("Security-Centric Architecture Assessment Framework v1.0.0", centre))
    story.append(PageBreak())

    # ── Executive Summary ──────────────────────────────────────────────────
    story.append(Paragraph("Executive Summary", h2))
    story.append(HRFlowable(width="100%", thickness=1, color=_CYAN))
    story.append(Spacer(1, 4*mm))

    metrics = [
        ["Metric", "Value"],
        ["Total Components",        str(len(arch.components))],
        ["Total Data Flows",        str(len(arch.data_flows))],
        ["Trust Boundaries",        str(len(arch.trust_boundaries))],
        ["Threats Detected",        str(len(result.threats))],
        ["Critical Threats",        str(rs.get("critical_count", 0))],
        ["High Threats",            str(rs.get("high_count", 0))],
        ["Medium Threats",          str(rs.get("medium_count", 0))],
        ["Low Threats",             str(rs.get("low_count", 0))],
        ["Average Risk Score",      f"{rs.get('avg_risk_score', 0):.2f} / 25"],
        ["Overall Risk Percentage", f"{rs.get('overall_risk_pct', 0):.1f}%"],
        ["Overall Risk Level",      rs.get("overall_risk_level", "N/A")],
    ]
    t = Table(metrics, colWidths=[90*mm, 80*mm])
    t.setStyle(_table_style())
    story.append(t)
    story.append(Spacer(1, 6*mm))

    # ── Architecture overview ──────────────────────────────────────────────
    story.append(Paragraph("Architecture Overview", h2))
    story.append(HRFlowable(width="100%", thickness=1, color=_CYAN))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(f"<b>Name:</b> {arch.name}", body))
    story.append(Paragraph(f"<b>Description:</b> {arch.description or 'N/A'}", body))
    story.append(Spacer(1, 3*mm))

    comp_data = [["Name", "Type", "Zone", "Internet", "Sensitivity", "Auth", "Authz", "Enc@Rest"]]
    for c in arch.components:
        comp_data.append([
            c.name[:22], c.type, c.zone,
            "Yes" if c.internet_facing else "No",
            c.data_sensitivity,
            "✓" if c.authentication     else "✗",
            "✓" if c.authorization      else "✗",
            "✓" if c.encryption_at_rest else "✗",
        ])
    ct = Table(comp_data, colWidths=[40*mm,22*mm,22*mm,18*mm,22*mm,12*mm,12*mm,18*mm])
    ct.setStyle(_table_style(header_bg=_NAVY))
    story.append(Paragraph("Components", h3))
    story.append(ct)
    story.append(PageBreak())

    # ── STRIDE Threats ─────────────────────────────────────────────────────
    story.append(Paragraph("STRIDE Threat Analysis", h2))
    story.append(HRFlowable(width="100%", thickness=1, color=_CYAN))
    story.append(Spacer(1, 3*mm))

    threat_data = [["ID", "Category", "Title", "Component", "Sev", "Risk"]]
    for t in result.threats:
        threat_data.append([
            Paragraph(t.id[:10], small),
            Paragraph(t.stride_category, small),
            Paragraph(t.title[:40], small),
            Paragraph(t.affected_component[:25], small),
            Paragraph(t.severity, small),
            Paragraph(str(t.risk_score), small),
        ])
    tt = Table(threat_data, colWidths=[20*mm, 32*mm, 55*mm, 38*mm, 16*mm, 12*mm])
    tt.setStyle(_table_style())
    story.append(tt)
    story.append(PageBreak())

    # ── Recommendations ────────────────────────────────────────────────────
    story.append(Paragraph("Prioritised Recommendations", h2))
    story.append(HRFlowable(width="100%", thickness=1, color=_CYAN))
    story.append(Spacer(1, 3*mm))

    for i, r in enumerate(result.recommendations[:20], 1):
        col = _SEV_COLOUR.get(r["priority"], _GREY)
        story.append(Paragraph(f"{i}. [{r['priority']}] {r['title']}", h3))
        story.append(Paragraph(f"<b>Component:</b> {r['component']}", body))
        story.append(Paragraph(f"<b>Pattern:</b> {r['pattern']}", body))
        story.append(Paragraph(r["explanation"][:200], body))
        story.append(Spacer(1, 3*mm))

    story.append(PageBreak())

    # ── Methodology ────────────────────────────────────────────────────────
    story.append(Paragraph("Methodology", h2))
    story.append(HRFlowable(width="100%", thickness=1, color=_CYAN))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "This assessment uses rule-based STRIDE threat modeling applied to architecture diagrams "
        "before any code is written (Security by Design). "
        "Risk Score = Likelihood × Impact (1–5 scale). "
        "Scores: 1–4 Low, 5–9 Medium, 10–16 High, 17–25 Critical.",
        body,
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "STRIDE: Spoofing (identity theft) | Tampering (data modification) | "
        "Repudiation (denying actions) | Information Disclosure (data leakage) | "
        "Denial of Service (availability loss) | Elevation of Privilege (unauthorised access).",
        body,
    ))
    story.append(Spacer(1, 5*mm))

    # ── Footer ─────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=_BORDER))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        f"Security-Centric Architecture Assessment Framework v1.0.0  |  Generated {now}",
        small,
    ))

    doc.build(story)
    return buffer.getvalue()


def _table_style(header_bg=_DARK) -> TableStyle:
    return TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR",    (0, 0), (-1, 0), _CYAN),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 8),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
        ("FONTSIZE",     (0, 1), (-1, -1), 8),
        ("TEXTCOLOR",    (0, 1), (-1, -1), _LIGHT),
        ("BACKGROUND",   (0, 1), (-1, -1), colors.HexColor("#161b22")),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.HexColor("#161b22"), colors.HexColor("#0d1117")]),
        ("GRID",         (0, 0), (-1, -1), 0.4, _BORDER),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ])
