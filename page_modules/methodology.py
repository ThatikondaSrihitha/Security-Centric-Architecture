"""Methodology page."""
import streamlit as st
from page_modules.shared_styles import inject_css, page_header, section_heading


def show() -> None:
    inject_css()
    page_header("Methodology", "How the Security-Centric Architecture Assessment Framework works.")

    section_heading("Security by Design")
    st.markdown("""
**Security by Design** means incorporating security requirements, threat analysis, and risk mitigation 
**before development begins** — not as an afterthought.

This framework implements Security by Design at the **architecture phase**, identifying vulnerabilities 
when they are cheapest to fix — during design, not after deployment.

> **Industry research shows that a security flaw fixed at the design stage costs 10–100× less to remediate 
> than the same flaw discovered post-deployment.**
""")

    # Methodology flow
    section_heading("Assessment Methodology Flow")
    steps = [
        ("📥 Architecture Input",       "User uploads an architecture file (JSON/YAML/XML/PlantUML) or selects a sample."),
        ("⚙️ Architecture Parsing",     "The parser extracts components, data flows, trust boundaries, and attributes into a normalised internal model."),
        ("🔎 Component Extraction",     "Each component is classified by type, zone, internet exposure, sensitivity, and security controls."),
        ("🎯 STRIDE Threat Analysis",   "20+ rule-based checks are applied to every component and data flow across all 6 STRIDE categories."),
        ("📊 Risk Calculation",         "Each threat is assigned Likelihood (1–5) and Impact (1–5). Risk = L × I. Max = 25."),
        ("🗺️ Pattern Mapping",          "Each threat is mapped to one or more of 24 security design patterns that address the root cause."),
        ("💡 Recommendations",          "Architecture-specific, prioritised recommendations are generated from threats and pattern mappings."),
        ("📄 Report Generation",        "Professional HTML, PDF, JSON, and CSV reports are produced for download."),
    ]
    for icon_title, desc in steps:
        cols = st.columns([1, 6])
        with cols[0]:
            st.markdown(f"<div style='background:#0f3460;border-radius:8px;padding:10px;text-align:center;font-size:1.5rem'>{'⬇️' if steps.index((icon_title,desc)) < len(steps)-1 else '✅'}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{icon_title}**: {desc}")

    # STRIDE
    section_heading("STRIDE Threat Categories")
    stride_info = [
        ("S", "Spoofing",              "#FF6B6B",
         "Pretending to be someone or something else.",
         "An attacker uses stolen credentials to impersonate a legitimate user and access sensitive data.",
         "Strong Authentication, MFA, Token-Based Authentication"),
        ("T", "Tampering",             "#FFA726",
         "Unauthorised modification of data or code.",
         "An attacker intercepts an unencrypted API call and modifies the order amount.",
         "Input Validation, Integrity Verification, Encryption in Transit"),
        ("R", "Repudiation",           "#FFEE58",
         "Claiming not to have performed an action.",
         "A user denies making a fraudulent transaction because there is no audit log.",
         "Secure Logging, Audit Trail, Digital Signatures"),
        ("I", "Information Disclosure","#AB47BC",
         "Exposing data to unauthorised parties.",
         "A database without encryption at rest is stolen, exposing all customer PII.",
         "Encryption at Rest, Network Segmentation, Secrets Management"),
        ("D", "Denial of Service",     "#29B6F6",
         "Making a system unavailable to legitimate users.",
         "An attacker floods the public API with requests, bringing down the service.",
         "Rate Limiting, Circuit Breaker, Redundancy and Failover"),
        ("E", "Elevation of Privilege","#EF5350",
         "Gaining more access rights than authorised.",
         "A regular user accesses admin functions due to missing authorisation checks.",
         "RBAC, Least Privilege, Zero Trust"),
    ]
    for letter, name, colour, definition, example, patterns in stride_info:
        with st.expander(f"**{letter} – {name}**", expanded=False):
            c1, c2 = st.columns([1, 4])
            with c1:
                st.markdown(f"<div style='background:{colour};color:#000;border-radius:50%;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-size:1.8rem;font-weight:900;'>{letter}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**Definition:** {definition}")
                st.markdown(f"**Example:** {example}")
                st.markdown(f"**Security Patterns:** {patterns}")

    # Risk formula
    section_heading("Risk Calculation Formula")
    st.markdown("""
```
Risk Score = Likelihood (1–5) × Impact (1–5)

Range → Classification:
  1 – 4   →  🟢 Low
  5 – 9   →  🟡 Medium
 10 – 16  →  🟠 High
 17 – 25  →  🔴 Critical

Overall Architecture Risk (%) = (Average Risk Score / 25) × 100
```

**Likelihood** is rated based on:
- Whether the component is internet-facing
- Whether security controls (auth, rate limiting) are missing
- Historical threat intelligence

**Impact** is rated based on:
- Data sensitivity level (low/medium/high/critical)
- Whether the component is on a critical path
- The STRIDE category severity
""")

    # Comparison with existing tools
    section_heading("Comparison With Existing Security Tools")
    st.markdown("""
| Tool              | Stage         | Requires Code? | Architecture-Level? | This Framework? |
|-------------------|---------------|----------------|---------------------|-----------------|
| OWASP ZAP         | Post-deploy   | ✅ Yes          | ❌ No               | ❌              |
| Burp Suite        | Testing       | ✅ Yes          | ❌ No               | ❌              |
| Nessus            | Post-deploy   | ✅ Yes          | ❌ No               | ❌              |
| SonarQube         | Development   | ✅ Yes          | ❌ No               | ❌              |
| Checkmarx         | Development   | ✅ Yes          | ❌ No               | ❌              |
| OWASP Threat Dragon| Design       | ❌ No           | ✅ Yes (manual)     | ❌              |
| MS TMT            | Design        | ❌ No           | ✅ Yes (manual)     | ❌              |
| **This Framework**| **Design**    | **❌ No**       | **✅ Yes (automated)**| **✅**       |

**This framework uniquely combines:** automated STRIDE analysis + risk scoring + pattern mapping + 
report generation — all operating on architecture descriptions before any code is written.
""")
