"""
Research Hub — NIST, OWASP, CIS, IEEE resources with summaries.
"""
from __future__ import annotations
import streamlit as st
from page_modules.shared_styles import inject_css, page_header, section_heading

RESOURCES = {
    "NIST": [
        {
            "id": "NIST-CSF", "title": "NIST Cybersecurity Framework 2.0",
            "type": "Framework", "year": 2024, "colour": "#00D4FF",
            "url": "https://www.nist.gov/cyberframework",
            "summary": "The NIST CSF provides a policy framework of computer security guidance for private sector organizations to assess and improve their ability to prevent, detect, and respond to cyber attacks.",
            "key_points": ["6 functions: Govern, Identify, Protect, Detect, Respond, Recover", "Risk-based approach to cybersecurity", "Applicable to any organization size", "Framework Profiles for customization", "Tiers 1-4 for maturity assessment"],
            "relevance": "Architecture Assessment, Risk Management",
            "tags": ["Framework", "Risk", "Governance"],
        },
        {
            "id": "NIST-SP800-53", "title": "NIST SP 800-53 Rev 5 — Security Controls",
            "type": "Standard", "year": 2020, "colour": "#00D4FF",
            "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
            "summary": "Comprehensive catalog of security and privacy controls for information systems and organizations. Covers 20 control families with hundreds of specific controls.",
            "key_points": ["20 control families (AC, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SC, SI, SR, AT)", "Baseline controls: Low, Moderate, High", "Privacy controls integrated", "Supply chain risk management", "Zero Trust alignment"],
            "relevance": "Security Controls, Compliance, Architecture",
            "tags": ["Controls", "Compliance", "Federal"],
        },
        {
            "id": "NIST-SP800-190", "title": "NIST SP 800-190 — Container Security",
            "type": "Guide", "year": 2017, "colour": "#00D4FF",
            "url": "https://csrc.nist.gov/publications/detail/sp/800-190/final",
            "summary": "Application Container Security Guide covering threats and countermeasures for container-based deployments including Docker and Kubernetes.",
            "key_points": ["Image vulnerabilities and hardening", "Registry security", "Orchestrator security (Kubernetes)", "Container runtime security", "Host OS hardening"],
            "relevance": "DevSecOps, Microservices, Cloud-Native",
            "tags": ["Containers", "Docker", "Kubernetes"],
        },
        {
            "id": "NIST-ZTA", "title": "NIST SP 800-207 — Zero Trust Architecture",
            "type": "Standard", "year": 2020, "colour": "#00D4FF",
            "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final",
            "summary": "Defines Zero Trust Architecture principles and deployment models. Core principle: never trust, always verify — every access request must be authenticated and authorized.",
            "key_points": ["7 Zero Trust tenets", "3 ZTA deployment models", "Policy Engine and Enforcement Point", "Enhanced Identity Governance", "Micro-segmentation approaches"],
            "relevance": "Zero Trust, Network Security, Architecture",
            "tags": ["Zero Trust", "Identity", "Network"],
        },
    ],
    "OWASP": [
        {
            "id": "OWASP-T10", "title": "OWASP Top 10 — 2021",
            "type": "Standard", "year": 2021, "colour": "#FF8C00",
            "url": "https://owasp.org/Top10/",
            "summary": "The most critical web application security risks, updated every 3-4 years based on data from hundreds of organizations.",
            "key_points": ["A01 Broken Access Control", "A02 Cryptographic Failures", "A03 Injection", "A04 Insecure Design", "A05 Security Misconfiguration", "A06 Vulnerable Components", "A07 Auth Failures", "A08 Data Integrity Failures", "A09 Logging Failures", "A10 SSRF"],
            "relevance": "Web Security, Threat Modeling, Developer Training",
            "tags": ["Web", "Vulnerabilities", "Top10"],
        },
        {
            "id": "OWASP-ASVS", "title": "OWASP ASVS 4.0 — Application Security Verification Standard",
            "type": "Standard", "year": 2019, "colour": "#FF8C00",
            "url": "https://owasp.org/www-project-application-security-verification-standard/",
            "summary": "Provides a basis for testing web application technical security controls. Three verification levels: L1 (minimum), L2 (most apps), L3 (critical apps).",
            "key_points": ["14 verification categories", "Level 1: Automated testing possible", "Level 2: Defense in depth", "Level 3: Advanced cryptography and sensitive systems", "286 requirements total"],
            "relevance": "Security Testing, Compliance, Architecture Review",
            "tags": ["Testing", "Verification", "Standards"],
        },
        {
            "id": "OWASP-SAMM", "title": "OWASP SAMM — Software Assurance Maturity Model",
            "type": "Framework", "year": 2020, "colour": "#FF8C00",
            "url": "https://owaspsamm.org/",
            "summary": "Measurable way to analyze and improve secure software development practices. 5 business functions, 15 security practices, 3 maturity levels each.",
            "key_points": ["5 business functions: Governance, Design, Implementation, Verification, Operations", "Maturity levels 0-3 per practice", "Measurable improvement roadmap", "Agile and traditional SDLC support", "Benchmark against industry"],
            "relevance": "SDLC Security, Maturity Assessment, DevSecOps",
            "tags": ["SDLC", "Maturity", "Governance"],
        },
        {
            "id": "OWASP-TD", "title": "OWASP Threat Dragon",
            "type": "Tool", "year": 2023, "colour": "#FF8C00",
            "url": "https://owasp.org/www-project-threat-dragon/",
            "summary": "Free, open-source threat modeling tool from OWASP. Creates threat model diagrams and automatically generates threats based on STRIDE methodology.",
            "key_points": ["Visual threat modeling", "STRIDE threat generation", "Mitigation tracking", "JSON export format", "Web and desktop versions"],
            "relevance": "Threat Modeling, Architecture Review",
            "tags": ["Tool", "Threat Modeling", "STRIDE"],
        },
    ],
    "CIS": [
        {
            "id": "CIS-CSC", "title": "CIS Controls v8 — 18 Critical Security Controls",
            "type": "Framework", "year": 2021, "colour": "#4ECDC4",
            "url": "https://www.cisecurity.org/controls/",
            "summary": "Prioritized set of 18 actions to stop the most pervasive cyber attacks. Implementation Groups IG1, IG2, IG3 allow scalable adoption.",
            "key_points": ["18 controls, 153 safeguards", "IG1: Basic cyber hygiene (56 safeguards)", "IG2: Most organizations (130 safeguards)", "IG3: Mature security teams (153 safeguards)", "Covers asset management, access control, logging, incident response"],
            "relevance": "Security Baseline, Governance, Compliance",
            "tags": ["Controls", "Baseline", "Governance"],
        },
        {
            "id": "CIS-BENCH", "title": "CIS Benchmarks — Configuration Standards",
            "type": "Standard", "year": 2024, "colour": "#4ECDC4",
            "url": "https://www.cisecurity.org/cis-benchmarks/",
            "summary": "Consensus-developed secure configuration guidelines for 100+ technologies including operating systems, cloud platforms, web servers, and databases.",
            "key_points": ["OS hardening (Windows, Linux, macOS)", "Cloud platform baselines (AWS, Azure, GCP)", "Web server configs (Apache, Nginx)", "Database security (MySQL, PostgreSQL)", "Container security (Docker, Kubernetes)"],
            "relevance": "Hardening, Configuration Management, DevSecOps",
            "tags": ["Hardening", "Configuration", "Cloud"],
        },
        {
            "id": "CIS-DEVSECOPS", "title": "CIS Software Supply Chain Security Guide",
            "type": "Guide", "year": 2022, "colour": "#4ECDC4",
            "url": "https://www.cisecurity.org/insights/white-papers/cis-software-supply-chain-security-guide",
            "summary": "Guidance for securing the software supply chain, covering source code, build pipeline, dependencies, and deployment artifacts.",
            "key_points": ["Source code security controls", "Build process hardening", "Dependency management", "Artifact signing and verification", "CI/CD pipeline security"],
            "relevance": "DevSecOps, Supply Chain, CI/CD",
            "tags": ["DevSecOps", "Supply Chain", "CI/CD"],
        },
    ],
    "IEEE / Academic": [
        {
            "id": "IEEE-ARCH", "title": "IEEE 1471 — Software Architecture Description",
            "type": "Standard", "year": 2000, "colour": "#7E57C2",
            "url": "https://standards.ieee.org/ieee/1471/2187/",
            "summary": "Defines recommended practice for Architectural Description of Software-Intensive Systems. Provides vocabulary and conceptual framework for architecture.",
            "key_points": ["Stakeholder concerns concept", "Viewpoints and views", "Rationale documentation", "Architecture description language", "System context definition"],
            "relevance": "Architecture Documentation, Academic Research",
            "tags": ["Architecture", "Standard", "Documentation"],
        },
        {
            "id": "IEEE-SECURE-SW", "title": "IEEE 2675 — DevOps: Building Reliable and Secure Systems",
            "type": "Standard", "year": 2021, "colour": "#7E57C2",
            "url": "https://standards.ieee.org/ieee/2675/7849/",
            "summary": "Provides framework for organizations adopting DevOps to build reliable and secure systems, covering practices, processes, and measurements.",
            "key_points": ["Security integration in CI/CD", "Automated security testing", "Infrastructure as Code security", "Monitoring and observability", "Feedback loops for security"],
            "relevance": "DevSecOps, CI/CD, Architecture",
            "tags": ["DevOps", "Security", "CI/CD"],
        },
        {
            "id": "STRIDE-PAPER", "title": "The STRIDE Threat Model (Microsoft Research)",
            "type": "Research Paper", "year": 2006, "colour": "#7E57C2",
            "url": "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats",
            "summary": "Original Microsoft paper introducing STRIDE threat modeling methodology for systematically identifying security threats in software systems.",
            "key_points": ["STRIDE categories definition", "Threat per element methodology", "DFD-based threat modeling", "Mitigation strategies per category", "Integration with SDL"],
            "relevance": "Threat Modeling, STRIDE, Architecture Security",
            "tags": ["STRIDE", "Threat Modeling", "Microsoft"],
        },
        {
            "id": "DREAD-REF", "title": "DREAD Risk Assessment Model",
            "type": "Methodology", "year": 2003, "colour": "#7E57C2",
            "url": "https://docs.microsoft.com/en-us/archive/blogs/david_leblanc/dreadful",
            "summary": "Microsoft-developed quantitative risk scoring model: Damage, Reproducibility, Exploitability, Affected Users, Discoverability. Provides numeric risk ranking.",
            "key_points": ["5-factor scoring model", "0-10 scale per factor", "Average score = risk rating", "Enables threat prioritization", "Complements STRIDE"],
            "relevance": "Risk Assessment, Threat Prioritization",
            "tags": ["DREAD", "Risk Scoring", "Methodology"],
        },
    ],
}


def show() -> None:
    inject_css()
    page_header("Research Hub",
                "NIST, OWASP, CIS, and IEEE resources with summaries for academic and professional reference.")

    total = sum(len(v) for v in RESOURCES.values())
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Resources", total)
    m2.metric("NIST Documents", len(RESOURCES["NIST"]))
    m3.metric("OWASP Resources", len(RESOURCES["OWASP"]))
    m4.metric("CIS + IEEE", len(RESOURCES["CIS"]) + len(RESOURCES["IEEE / Academic"]))

    section_heading("Search & Filter")
    f1, f2 = st.columns(2)
    sel_org = f1.selectbox("Organization", ["All"] + list(RESOURCES.keys()))
    search = f2.text_input("Search resources", placeholder="keyword, topic, standard…")

    tabs = st.tabs(["🔵 NIST", "🟠 OWASP", "🟢 CIS", "🟣 IEEE / Academic"])
    tab_map = {"NIST": 0, "OWASP": 1, "CIS": 2, "IEEE / Academic": 3}

    for org, tab in zip(RESOURCES.keys(), tabs):
        with tab:
            items = RESOURCES[org]
            if search:
                s = search.lower()
                items = [r for r in items if
                         s in r["title"].lower() or s in r["summary"].lower() or
                         any(s in t.lower() for t in r["tags"])]

            section_heading(f"{org} Resources ({len(items)})")

            for res in items:
                with st.expander(f"**{res['id']}** — {res['title']} ({res['year']})", expanded=False):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.markdown(f"**Type:** {res['type']}")
                    c2.markdown(f"**Year:** {res['year']}")
                    c3.markdown(f"**Relevance:** {res['relevance'][:30]}…" if len(res['relevance']) > 30 else f"**Relevance:** {res['relevance']}")
                    c4.markdown(f"**Tags:** {', '.join(res['tags'])}")

                    st.markdown(f"**📖 Summary:** {res['summary']}")

                    t1, t2 = st.tabs(["🔑 Key Points", "🔗 Access Resource"])
                    with t1:
                        for point in res["key_points"]:
                            st.markdown(f"• {point}")
                    with t2:
                        st.markdown(f"""
<div style="background:#0f2d5c; border:1px solid rgba(0,212,255,0.3);
            border-radius:12px; padding:16px; text-align:center;">
  <a href="{res['url']}" target="_blank"
     style="color:#00D4FF; font-weight:700; font-size:1rem; text-decoration:none;">
    🔗 Open: {res['title']}
  </a><br>
  <span style="color:#9ca3af; font-size:0.82rem; margin-top:8px; display:block;">{res['url']}</span>
</div>
""", unsafe_allow_html=True)

    # Quick reference table
    st.markdown("<br>", unsafe_allow_html=True)
    section_heading("All Resources — Quick Reference")
    import pandas as pd
    all_rows = []
    for org, items in RESOURCES.items():
        for res in items:
            all_rows.append({
                "ID": res["id"],
                "Organization": org,
                "Title": res["title"][:50],
                "Type": res["type"],
                "Year": res["year"],
                "Relevance": res["relevance"][:40],
            })
    st.dataframe(pd.DataFrame(all_rows), use_container_width=True, hide_index=True)
