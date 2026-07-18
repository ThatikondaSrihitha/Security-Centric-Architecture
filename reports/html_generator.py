"""HTML report generator using Jinja2-style string templates."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict

from core.models import AnalysisResult


def generate_html(result: AnalysisResult) -> str:
    rs    = result.risk_summary
    arch  = result.architecture
    now   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    title = f"{arch.name} – Security Assessment Report"

    threats_rows = ""
    for t in result.threats:
        colour = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(t.severity,"#aaa")
        threats_rows += f"""
        <tr>
          <td>{t.id}</td>
          <td><span class="badge" style="background:{colour}">{t.stride_category}</span></td>
          <td>{t.title}</td>
          <td>{t.affected_component}</td>
          <td><span class="badge" style="background:{colour}">{t.severity}</span></td>
          <td>{t.risk_score}</td>
          <td style="font-size:0.82em;color:#aaa">{t.evidence}</td>
        </tr>"""

    rec_rows = ""
    for i, r in enumerate(result.recommendations, 1):
        colour = {"Critical":"#FF2D2D","High":"#FF8C00","Medium":"#FFD700","Low":"#00C853"}.get(r["priority"],"#aaa")
        rec_rows += f"""
        <tr>
          <td>{i}</td>
          <td><span class="badge" style="background:{colour}">{r['priority']}</span></td>
          <td><b>{r['title']}</b><br><small>{r['component']}</small></td>
          <td>{r['pattern']}</td>
          <td style="font-size:0.85em">{r['explanation'][:120]}…</td>
        </tr>"""

    stride_counts = {}
    for t in result.threats:
        stride_counts[t.stride_category] = stride_counts.get(t.stride_category, 0) + 1

    stride_rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>"
        for k, v in stride_counts.items()
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Segoe UI',Arial,sans-serif; background:#0d1117; color:#e5e7eb; line-height:1.6; }}
  .cover {{ background:linear-gradient(135deg,#0f3460 0%,#16213e 50%,#0d1117 100%);
             padding:60px 40px; text-align:center; }}
  .cover h1 {{ font-size:2.2em; color:#00D4FF; margin-bottom:10px; }}
  .cover h2 {{ font-size:1.5em; color:#e5e7eb; margin-bottom:20px; }}
  .cover p  {{ color:#9ca3af; font-size:1em; }}
  .section  {{ padding:30px 40px; border-bottom:1px solid #1f2937; }}
  .section h2 {{ font-size:1.4em; color:#00D4FF; margin-bottom:15px; border-left:4px solid #00D4FF; padding-left:12px; }}
  .section h3 {{ font-size:1.1em; color:#4ECDC4; margin:15px 0 10px; }}
  .metric-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:15px; margin-top:15px; }}
  .metric {{ background:#161b22; border:1px solid #30363d; border-radius:10px; padding:15px; text-align:center; }}
  .metric .val {{ font-size:2em; font-weight:700; color:#00D4FF; }}
  .metric .lbl {{ font-size:0.8em; color:#9ca3af; margin-top:4px; }}
  table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:0.9em; }}
  th    {{ background:#161b22; padding:10px; text-align:left; color:#9ca3af; font-weight:600; border-bottom:2px solid #30363d; }}
  td    {{ padding:9px 10px; border-bottom:1px solid #1f2937; vertical-align:top; }}
  tr:hover td {{ background:rgba(0,212,255,0.04); }}
  .badge {{ padding:3px 10px; border-radius:20px; font-size:0.78em; font-weight:700; color:#000; display:inline-block; }}
  .risk-box {{ background:#161b22; border:2px solid #00D4FF; border-radius:12px; padding:20px; margin:10px 0; text-align:center; }}
  .risk-box .big {{ font-size:3em; font-weight:900; }}
  footer {{ text-align:center; padding:20px; color:#4b5563; font-size:0.8em; }}
  @media print {{ body {{ background:#fff; color:#000; }} .cover {{ background:#0f3460; }} }}
</style>
</head>
<body>

<div class="cover">
  <div style="font-size:3em; margin-bottom:15px">🔐</div>
  <h1>Security Assessment Report</h1>
  <h2>{arch.name}</h2>
  <p>Analysis ID: {result.analysis_id} &nbsp;|&nbsp; Generated: {now}</p>
  <p>Framework: Security-Centric Architecture Assessment Framework v1.0.0</p>
</div>

<div class="section">
  <h2>Executive Summary</h2>
  <div class="metric-grid">
    <div class="metric"><div class="val">{len(arch.components)}</div><div class="lbl">Components</div></div>
    <div class="metric"><div class="val">{len(arch.data_flows)}</div><div class="lbl">Data Flows</div></div>
    <div class="metric"><div class="val">{len(result.threats)}</div><div class="lbl">Threats Detected</div></div>
    <div class="metric"><div class="val">{rs.get('critical_count',0)}</div><div class="lbl">Critical</div></div>
    <div class="metric"><div class="val">{rs.get('high_count',0)}</div><div class="lbl">High</div></div>
    <div class="metric"><div class="val">{rs.get('medium_count',0)}</div><div class="lbl">Medium</div></div>
    <div class="metric"><div class="val">{rs.get('low_count',0)}</div><div class="lbl">Low</div></div>
    <div class="metric"><div class="val">{rs.get('overall_risk_pct',0)}%</div><div class="lbl">Risk Score</div></div>
  </div>
  <div class="risk-box" style="margin-top:20px">
    <div class="big" style="color:{'#FF2D2D' if rs.get('overall_risk_level')=='Critical' else '#FF8C00' if rs.get('overall_risk_level')=='High' else '#FFD700' if rs.get('overall_risk_level')=='Medium' else '#00C853'}">{rs.get('overall_risk_pct',0)}%</div>
    <div style="font-size:1.4em; margin-top:5px; color:#e5e7eb">Overall Risk Level: <b>{rs.get('overall_risk_level','N/A')}</b></div>
    <div style="color:#9ca3af; margin-top:8px; font-size:0.9em">
      Formula: Risk Score = Likelihood × Impact (1–5 scale). Avg: {rs.get('avg_risk_score',0):.2f}/25 = {rs.get('overall_risk_pct',0)}%
    </div>
  </div>
</div>

<div class="section">
  <h2>Architecture Overview</h2>
  <p><b>Name:</b> {arch.name}</p>
  <p><b>Description:</b> {arch.description or "N/A"}</p>
  <p><b>Components:</b> {len(arch.components)} &nbsp;|&nbsp; <b>Data Flows:</b> {len(arch.data_flows)} &nbsp;|&nbsp; <b>Trust Boundaries:</b> {len(arch.trust_boundaries)}</p>
  <h3>Components</h3>
  <table>
    <tr><th>Name</th><th>Type</th><th>Zone</th><th>Internet-Facing</th><th>Sensitivity</th><th>Auth</th><th>Authz</th><th>Enc@Rest</th></tr>
    {"".join(f"<tr><td>{c.name}</td><td>{c.type}</td><td>{c.zone}</td><td>{'✅' if c.internet_facing else '❌'}</td><td>{c.data_sensitivity}</td><td>{'✅' if c.authentication else '❌'}</td><td>{'✅' if c.authorization else '❌'}</td><td>{'✅' if c.encryption_at_rest else '❌'}</td></tr>" for c in arch.components)}
  </table>
</div>

<div class="section">
  <h2>STRIDE Threat Analysis</h2>
  <h3>Summary by Category</h3>
  <table><tr><th>STRIDE Category</th><th>Threat Count</th></tr>{stride_rows}</table>
  <h3>Detailed Threat List</h3>
  <table>
    <tr><th>ID</th><th>Category</th><th>Title</th><th>Component</th><th>Severity</th><th>Risk</th><th>Evidence</th></tr>
    {threats_rows}
  </table>
</div>

<div class="section">
  <h2>Risk Assessment</h2>
  <p><b>Formula:</b> Risk Score = Likelihood (1–5) × Impact (1–5) → max 25</p>
  <p><b>Classification:</b> 1–4 Low | 5–9 Medium | 10–16 High | 17–25 Critical</p>
  <p><b>Average Risk Score:</b> {rs.get('avg_risk_score',0):.2f}</p>
  <p><b>Maximum Risk Score:</b> {rs.get('max_risk_score',0)}</p>
  <p><b>Overall Risk Percentage:</b> {rs.get('overall_risk_pct',0):.1f}%</p>
  <p><b>Overall Risk Level:</b> <b>{rs.get('overall_risk_level','N/A')}</b></p>
</div>

<div class="section">
  <h2>Prioritised Recommendations</h2>
  <table>
    <tr><th>#</th><th>Priority</th><th>Recommendation</th><th>Pattern</th><th>Explanation</th></tr>
    {rec_rows}
  </table>
</div>

<div class="section">
  <h2>Methodology</h2>
  <p>This report was generated using the Security-Centric Architecture Assessment Framework, which implements
  <b>Security by Design</b> principles. The framework applies <b>STRIDE threat modeling</b> rules to architecture
  diagrams before any code is written, enabling early identification and remediation of security issues.</p>
  <p><b>STRIDE Categories:</b> Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.</p>
  <p><b>Risk Formula:</b> Score = Likelihood × Impact (both 1–5). Classified as Low (1–4), Medium (5–9), High (10–16), Critical (17–25).</p>
</div>

<div class="section">
  <h2>Assumptions and Limitations</h2>
  <ul style="padding-left:20px; margin-top:10px">
    <li>Analysis is based solely on the provided architecture description.</li>
    <li>Actual risk may vary depending on implementation details not captured in the architecture.</li>
    <li>Threat detection is rule-based; novel attack vectors may not be covered.</li>
    <li>Recommended patterns should be validated by qualified security professionals.</li>
  </ul>
</div>

<footer>
  <p>Security-Centric Architecture Assessment Framework v1.0.0 &nbsp;|&nbsp; Generated {now}</p>
  <p>This report is for academic and development purposes.</p>
</footer>

</body>
</html>"""
