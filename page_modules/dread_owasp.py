"""
DREAD Scoring + OWASP Top 10 Mapping page.
Works standalone or enriches existing STRIDE analysis.
"""
from __future__ import annotations
from typing import Dict, List, Any
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from page_modules.shared_styles import inject_css, page_header, section_heading
from utils.session_manager import has_analysis, get as ss_get

# ── DREAD Calculator ──────────────────────────────────────────────────────────

def _dread_score(d: int, r: int, e: int, a: int, disc: int) -> float:
    return round((d + r + e + a + disc) / 5, 2)

def _dread_level(score: float) -> tuple[str, str]:
    if score >= 7:
        return "Critical", "#FF2D2D"
    if score >= 5:
        return "High", "#FF8C00"
    if score >= 3:
        return "Medium", "#FFD700"
    return "Low", "#00C853"

# ── OWASP Top 10 (2021) ───────────────────────────────────────────────────────

OWASP_TOP_10 = [
    {
        "rank": "A01",
        "name": "Broken Access Control",
        "severity": "Critical",
        "colour": "#FF2D2D",
        "description": "Restrictions on what authenticated users are allowed to do are not properly enforced.",
        "examples": ["Accessing other users' data by modifying URL", "Viewing/editing someone else's account",
                     "Missing function-level access control"],
        "mitigations": ["Deny by default", "Log access control failures", "Rate limit API access",
                        "Invalidate JWT tokens on server side"],
        "cwe": "CWE-284",
    },
    {
        "rank": "A02",
        "name": "Cryptographic Failures",
        "severity": "Critical",
        "colour": "#FF2D2D",
        "description": "Failures related to cryptography that lead to exposure of sensitive data.",
        "examples": ["Passwords stored in plaintext", "Weak MD5/SHA1 hashing", "HTTP instead of HTTPS",
                     "Hardcoded encryption keys"],
        "mitigations": ["Encrypt data at rest and in transit", "Use strong algorithms (AES-256, bcrypt)",
                        "Don't cache sensitive data", "Enforce TLS 1.2+"],
        "cwe": "CWE-327",
    },
    {
        "rank": "A03",
        "name": "Injection",
        "severity": "Critical",
        "colour": "#FF2D2D",
        "description": "Hostile data is sent to an interpreter as part of a command or query.",
        "examples": ["SQL injection", "NoSQL injection", "OS command injection", "LDAP injection"],
        "mitigations": ["Use parameterized queries", "Server-side input validation", "Escape special characters",
                        "Use LIMIT to prevent mass data disclosure"],
        "cwe": "CWE-89",
    },
    {
        "rank": "A04",
        "name": "Insecure Design",
        "severity": "High",
        "colour": "#FF8C00",
        "description": "Missing or ineffective control design — security is not built into the design.",
        "examples": ["No rate limiting on credential recovery", "Missing threat modeling",
                     "No security requirements defined"],
        "mitigations": ["Use threat modeling", "Apply secure design patterns", "Write security stories",
                        "Use reference architectures"],
        "cwe": "CWE-657",
    },
    {
        "rank": "A05",
        "name": "Security Misconfiguration",
        "severity": "High",
        "colour": "#FF8C00",
        "description": "Insecure default configurations, incomplete configurations, open cloud storage.",
        "examples": ["Default admin credentials", "Unnecessary features enabled", "Verbose error messages",
                     "Missing security headers"],
        "mitigations": ["Minimal platform", "Remove unused features", "Review and update configs",
                        "Automated configuration auditing"],
        "cwe": "CWE-16",
    },
    {
        "rank": "A06",
        "name": "Vulnerable and Outdated Components",
        "severity": "High",
        "colour": "#FF8C00",
        "description": "Components with known vulnerabilities are used without testing for compatibility.",
        "examples": ["Outdated libraries with CVEs", "Unsupported OS", "Unpatched dependencies"],
        "mitigations": ["Monitor CVE databases", "Use SCA tools (Snyk, OWASP Dependency-Check)",
                        "Subscribe to security advisories", "Automated patch management"],
        "cwe": "CWE-1026",
    },
    {
        "rank": "A07",
        "name": "Identification and Authentication Failures",
        "severity": "High",
        "colour": "#FF8C00",
        "description": "Weaknesses in authentication and session management allow attackers to compromise passwords.",
        "examples": ["Weak passwords permitted", "No MFA", "Weak session tokens",
                     "Session IDs in URL"],
        "mitigations": ["Implement MFA", "Strong password policies", "Secure session management",
                        "Rate limit login attempts"],
        "cwe": "CWE-287",
    },
    {
        "rank": "A08",
        "name": "Software and Data Integrity Failures",
        "severity": "Medium",
        "colour": "#FFD700",
        "description": "Code and infrastructure that does not protect against integrity violations.",
        "examples": ["Unsigned software updates", "Insecure deserialization", "Auto-update without integrity check"],
        "mitigations": ["Use digital signatures", "Verify integrity of libraries", "Review serialized data",
                        "CI/CD pipeline integrity"],
        "cwe": "CWE-494",
    },
    {
        "rank": "A09",
        "name": "Security Logging and Monitoring Failures",
        "severity": "Medium",
        "colour": "#FFD700",
        "description": "Insufficient logging and monitoring allows attackers to persist undetected.",
        "examples": ["Login failures not logged", "No alerting on suspicious activity",
                     "Logs stored only locally"],
        "mitigations": ["Log authentication events", "Centralize logs (SIEM)", "Monitor and alert",
                        "Tamper-resistant audit trails"],
        "cwe": "CWE-778",
    },
    {
        "rank": "A10",
        "name": "Server-Side Request Forgery (SSRF)",
        "severity": "Medium",
        "colour": "#FFD700",
        "description": "SSRF flaws occur when a web application fetches a remote resource from user-supplied URLs.",
        "examples": ["Fetching internal metadata URLs", "Accessing internal services via SSRF",
                     "Cloud metadata endpoint abuse"],
        "mitigations": ["Deny by default", "URL allowlisting", "Disable HTTP redirections",
                        "Network segmentation"],
        "cwe": "CWE-918",
    },
]

# ── STRIDE → OWASP mapping ────────────────────────────────────────────────────

STRIDE_OWASP_MAP = {
    "Spoofing":              ["A07", "A01"],
    "Tampering":             ["A03", "A08", "A02"],
    "Repudiation":           ["A09"],
    "InformationDisclosure": ["A02", "A01", "A05"],
    "DenialOfService":       ["A05", "A10"],
    "ElevationOfPrivilege":  ["A01", "A04", "A07"],
}


def show() -> None:
    inject_css()
    page_header("DREAD Scoring & OWASP Top 10", "Quantitative risk scoring and OWASP vulnerability mapping.")

    tab1, tab2, tab3 = st.tabs(["📊 DREAD Risk Calculator", "🛡️ OWASP Top 10", "🔗 STRIDE → OWASP Mapping"])

    # ── Tab 1: DREAD Calculator ────────────────────────────────────────────
    with tab1:
        section_heading("DREAD Risk Scoring Calculator")
        st.markdown("""
<div style="background:#0f2d5c; border:1px solid #1e3a5f; border-radius:12px; padding:16px; margin-bottom:20px;">
  <b style="color:#00D4FF">Formula:</b> <span style="color:#e5e7eb">DREAD Score = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5</span><br>
  <span style="color:#9ca3af; font-size:0.85rem">Each factor rated 0–10. Score 0–3 = Low, 4–6 = Medium, 7–9 = High, 10 = Critical</span>
</div>
""", unsafe_allow_html=True)

        # Threat name input
        threat_name = st.text_input("Threat / Vulnerability Name", placeholder="e.g., SQL Injection in Login Form")

        c1, c2 = st.columns(2)
        with c1:
            d_score = st.slider("💥 Damage Potential", 0, 10, 5,
                                help="How bad is the damage if successfully exploited?")
            r_score = st.slider("🔁 Reproducibility", 0, 10, 5,
                                help="How easy is it to reproduce the attack?")
            e_score = st.slider("⚡ Exploitability", 0, 10, 5,
                                help="How easy is it to launch the attack?")
        with c2:
            a_score = st.slider("👥 Affected Users", 0, 10, 5,
                                help="How many users are affected?")
            disc_score = st.slider("🔍 Discoverability", 0, 10, 5,
                                   help="How easy is it to discover this vulnerability?")

        if st.button("Calculate DREAD Score", type="primary", use_container_width=True):
            final_score = _dread_score(d_score, r_score, e_score, a_score, disc_score)
            level, colour = _dread_level(final_score)

            st.markdown(f"""
<div style="background:#161b22; border:2px solid {colour}; border-radius:16px; padding:24px; text-align:center; margin:16px 0;">
  <div style="font-size:3.5rem; font-weight:900; color:{colour};">{final_score}</div>
  <div style="color:#e5e7eb; font-size:1.2rem; font-weight:700; margin:8px 0;">{level} Risk</div>
  <div style="color:#9ca3af; font-size:0.85rem;">Threat: <b style="color:#e5e7eb">{threat_name or 'Unnamed Threat'}</b></div>
</div>
""", unsafe_allow_html=True)

            # Radar chart
            fig = go.Figure(go.Scatterpolar(
                r=[d_score, r_score, e_score, a_score, disc_score, d_score],
                theta=["Damage", "Reproducibility", "Exploitability", "Affected Users", "Discoverability", "Damage"],
                fill="toself",
                fillcolor=f"rgba{tuple(int(colour.lstrip('#')[i:i+2], 16) for i in (0,2,4)) + (0.2,)}",
                line=dict(color=colour, width=2),
                name="DREAD Score",
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 10], gridcolor="#30363d", color="#9ca3af"),
                    angularaxis=dict(gridcolor="#30363d", color="#9ca3af"),
                    bgcolor="#161b22",
                ),
                paper_bgcolor="#0d1117",
                plot_bgcolor="#0d1117",
                font=dict(color="#e5e7eb"),
                title=dict(text=f"DREAD Analysis: {threat_name or 'Threat'}", font=dict(color="#00D4FF")),
                height=350,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Factor breakdown
            factors = {
                "Damage Potential": (d_score, "How bad if exploited"),
                "Reproducibility": (r_score, "Ease of repetition"),
                "Exploitability": (e_score, "Ease of exploitation"),
                "Affected Users": (a_score, "User impact breadth"),
                "Discoverability": (disc_score, "Ease of discovery"),
            }
            rows = [{"Factor": k, "Score": v[0], "Description": v[1],
                     "Level": _dread_level(v[0])[0]} for k, v in factors.items()]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ── Batch DREAD ────────────────────────────────────────────────────
        if has_analysis():
            st.markdown("<br>", unsafe_allow_html=True)
            section_heading("Auto-Score Detected Threats")
            result = st.session_state["analysis_result"]
            st.markdown(f"**Auto-generating DREAD scores for {len(result.threats)} detected threats**")

            dread_rows = []
            for t in result.threats[:20]:
                # Map severity to approximate DREAD values
                base = {"Critical": 8, "High": 6, "Medium": 4, "Low": 2}.get(t.severity, 4)
                d = min(10, base + (1 if t.impact >= 4 else 0))
                r = min(10, base)
                e_val = min(10, base + (1 if t.likelihood >= 4 else -1))
                a = min(10, base)
                disc = min(10, base - 1)
                score = _dread_score(d, r, e_val, a, disc)
                level, _ = _dread_level(score)
                dread_rows.append({
                    "Threat": t.title[:45],
                    "Component": t.affected_component[:30],
                    "STRIDE": t.stride_category,
                    "D": d, "R": r, "E": e_val, "A": a, "Disc": disc,
                    "DREAD Score": score,
                    "Level": level,
                })
            df = pd.DataFrame(dread_rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Tab 2: OWASP Top 10 ────────────────────────────────────────────────
    with tab2:
        section_heading("OWASP Top 10 — 2021")

        # Summary metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Vulnerabilities", 10)
        m2.metric("Critical Risk", 3)
        m3.metric("High Risk", 4)

        # Filter
        sel_sev = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium"])
        items = OWASP_TOP_10
        if sel_sev != "All":
            items = [o for o in items if o["severity"] == sel_sev]

        for item in items:
            with st.expander(
                f"**{item['rank']}** — {item['name']} [{item['severity']}]",
                expanded=False
            ):
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.markdown(f"""
<div style="background:{item['colour']}22; border:2px solid {item['colour']};
            border-radius:12px; padding:16px; text-align:center;">
  <div style="color:{item['colour']}; font-size:1.8rem; font-weight:900;">{item['rank']}</div>
  <div style="color:{item['colour']}; font-size:0.8rem; font-weight:700; margin-top:4px;">{item['severity']}</div>
  <div style="color:#9ca3af; font-size:0.72rem; margin-top:4px;">{item['cwe']}</div>
</div>
""", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"**{item['description']}**")

                t1, t2, t3 = st.tabs(["📋 Examples", "🛡️ Mitigations", "🔗 STRIDE Mapping"])
                with t1:
                    for ex in item["examples"]:
                        st.markdown(f"• {ex}")
                with t2:
                    for mit in item["mitigations"]:
                        st.markdown(f"✅ {mit}")
                with t3:
                    # Find STRIDE categories that map to this OWASP item
                    mapped_stride = [s for s, owasps in STRIDE_OWASP_MAP.items()
                                     if item["rank"] in owasps]
                    if mapped_stride:
                        for s in mapped_stride:
                            st.markdown(f"🎯 **{s}** threats can lead to this vulnerability")
                    else:
                        st.markdown("_No direct STRIDE mapping_")

    # ── Tab 3: STRIDE → OWASP Mapping ─────────────────────────────────────
    with tab3:
        section_heading("STRIDE → OWASP Top 10 Cross-Reference")

        st.markdown("""
<div class="info-card">
  <h4>ℹ️ How to Use This Mapping</h4>
  <p>Use this table to map your STRIDE threat findings to the corresponding OWASP Top 10 vulnerabilities.
  This helps prioritize mitigations using industry-standard classifications.</p>
</div>
""", unsafe_allow_html=True)

        mapping_rows = []
        for stride_cat, owasp_ids in STRIDE_OWASP_MAP.items():
            for oid in owasp_ids:
                owasp = next((o for o in OWASP_TOP_10 if o["rank"] == oid), None)
                if owasp:
                    mapping_rows.append({
                        "STRIDE Category": stride_cat,
                        "OWASP ID": oid,
                        "OWASP Vulnerability": owasp["name"],
                        "Severity": owasp["severity"],
                    })

        st.dataframe(pd.DataFrame(mapping_rows), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        section_heading("Visual Mapping")

        # Heat map style visualization
        stride_cats = list(STRIDE_OWASP_MAP.keys())
        owasp_ids = [o["rank"] for o in OWASP_TOP_10]

        matrix = []
        for s in stride_cats:
            row = []
            for oid in owasp_ids:
                row.append(1 if oid in STRIDE_OWASP_MAP.get(s, []) else 0)
            matrix.append(row)

        fig = go.Figure(go.Heatmap(
            z=matrix,
            x=owasp_ids,
            y=stride_cats,
            colorscale=[[0, "#161b22"], [1, "#00D4FF"]],
            showscale=False,
            hovertemplate="<b>%{y}</b> → <b>%{x}</b><extra></extra>",
        ))
        fig.update_layout(
            title="STRIDE to OWASP Mapping Matrix",
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            font=dict(color="#e5e7eb"),
            xaxis=dict(side="top", gridcolor="#30363d"),
            yaxis=dict(gridcolor="#30363d"),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

        # If analysis exists, map current threats to OWASP
        if has_analysis():
            st.markdown("<br>", unsafe_allow_html=True)
            section_heading("Your Analysis → OWASP Mapping")
            result = st.session_state["analysis_result"]

            owasp_threat_rows = []
            for t in result.threats:
                mapped = STRIDE_OWASP_MAP.get(t.stride_category, [])
                for oid in mapped:
                    owasp = next((o for o in OWASP_TOP_10 if o["rank"] == oid), None)
                    if owasp:
                        owasp_threat_rows.append({
                            "Threat": t.title[:40],
                            "Component": t.affected_component[:25],
                            "STRIDE": t.stride_category,
                            "OWASP": f"{oid} — {owasp['name']}",
                            "Severity": t.severity,
                        })

            if owasp_threat_rows:
                st.dataframe(pd.DataFrame(owasp_threat_rows), use_container_width=True, hide_index=True)
            else:
                st.info("Run an assessment to see your threats mapped to OWASP.")
