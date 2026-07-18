"""Project Documentation page."""
import streamlit as st
from page_modules.shared_styles import inject_css, page_header, section_heading


def show() -> None:
    inject_css()
    page_header("📖", "Project Documentation", "Complete academic documentation for the B.Tech Major Project.")

    sections = {
        "Abstract": """
This project presents a **Security-Centric Architecture Assessment Framework** that implements 
Security by Design principles for software systems. The framework enables developers and architects 
to identify security vulnerabilities at the architecture design stage — before any code is written — 
using automated STRIDE threat modeling, rule-based risk assessment, and security design pattern 
recommendations. The system accepts architecture descriptions in JSON, YAML, XML, and PlantUML formats, 
performs comprehensive threat analysis, calculates risk scores, maps threats to security patterns, 
and generates professional reports in HTML, PDF, JSON, and CSV formats.
""",
        "Introduction": """
Software security has traditionally been addressed late in the development lifecycle — through code 
reviews, penetration testing, and vulnerability scanning of deployed applications. This reactive 
approach results in expensive rework, delayed releases, and persistent security vulnerabilities. 

This project addresses the problem at its root by shifting security analysis to the **earliest 
possible stage**: the software architecture design phase. By analyzing architecture diagrams before 
coding begins, the framework enables development teams to make secure design decisions when changes 
are least expensive.
""",
        "Problem Statement": """
Existing security tools (OWASP ZAP, Burp Suite, SonarQube, Nessus) require working code or deployed 
applications. They cannot analyze security at the architecture level. Manual threat modeling tools 
(OWASP Threat Dragon, Microsoft Threat Modeling Tool) exist but require significant manual effort 
and expertise, lack integrated risk scoring, and do not provide automated remediation guidance.

**Key problems identified:**
1. Security vulnerabilities are discovered late — after coding, testing, or deployment.
2. Late-discovered vulnerabilities require expensive architectural redesign.
3. Developers lack automated tools for architecture-level security assessment.
4. No integrated workflow exists combining STRIDE analysis, risk scoring, pattern mapping, and reporting.
5. Security patterns are not systematically applied during the design phase.
""",
        "Existing Systems & Tools": """
**OWASP ZAP (Zed Attack Proxy)**
- Purpose: Web application vulnerability scanner
- Stage: Post-deployment testing
- Limitation: Requires a running application; cannot analyze architecture

**Burp Suite**
- Purpose: Professional web application penetration testing
- Stage: Testing phase
- Limitation: Requires deployed application; expertise-dependent

**Nessus**
- Purpose: Network vulnerability scanner
- Stage: Post-deployment
- Limitation: Infrastructure-focused; not architecture-aware

**SonarQube**
- Purpose: Static code analysis
- Stage: Development phase (requires code)
- Limitation: Code-level analysis; cannot detect architectural design flaws

**Checkmarx**
- Purpose: Static application security testing (SAST)
- Stage: Development phase
- Limitation: Requires source code

**OWASP Threat Dragon**
- Purpose: Threat modeling diagram tool
- Stage: Design phase
- Limitation: Manual process; limited automation; no integrated risk scoring

**Microsoft Threat Modeling Tool**
- Purpose: DFD-based threat modeling
- Stage: Design phase
- Limitation: Microsoft-specific; limited integration; manual pattern application

**Common Limitation:** None of these tools provide an integrated automated workflow that:
- Accepts multiple architecture format inputs
- Applies automated STRIDE rules
- Calculates risk scores
- Maps to security patterns
- Generates professional reports
— all operating on the architecture without requiring code or deployment.
""",
        "Proposed System": """
The **Security-Centric Architecture Assessment Framework** is a web application built with Python 
and Streamlit that:

1. **Accepts multiple input formats**: JSON, YAML, XML, PlantUML
2. **Normalises** all inputs into a common architecture data model
3. **Applies automated STRIDE rules** to every component and data flow
4. **Calculates risk scores** using Likelihood × Impact formula
5. **Maps threats to security patterns** from a curated library of 24 patterns
6. **Generates prioritised recommendations** specific to the architecture
7. **Produces professional reports** in HTML, PDF, JSON, and CSV formats
8. **Stores analysis history** in SQLite for comparison and reference
9. **Visualises the architecture** as an interactive network graph
10. **Provides educational content** on security patterns and methodology
""",
        "Objectives": """
1. Implement a complete Security-by-Design assessment workflow for software architectures.
2. Build automated STRIDE threat detection using rule-based analysis.
3. Implement a transparent risk assessment formula (Likelihood × Impact).
4. Create a security pattern library with 24 patterns covering all STRIDE categories.
5. Generate professional, downloadable security assessment reports.
6. Provide architecture visualisation as an interactive network graph.
7. Maintain an analysis history database for comparison and reference.
8. Support multiple architecture input formats (JSON, YAML, XML, PlantUML).
9. Build a polished, professional web interface suitable for industry use.
10. Create a fully demonstrable application without external dependencies.
""",
        "System Modules": """
| Module | Description |
|--------|-------------|
| **Architecture Input** | File upload, sample selection, manual form entry |
| **Architecture Parser** | JSON, YAML, XML, PlantUML parsers with common data model |
| **STRIDE Engine** | Rule-based threat detection across 6 categories |
| **Risk Calculator** | Likelihood × Impact risk scoring and classification |
| **Pattern Mapper** | Threat-to-pattern mapping from 24-pattern library |
| **Recommendation Engine** | Prioritised, architecture-specific recommendations |
| **Visualisation** | NetworkX + Plotly interactive architecture graph |
| **Dashboard** | 9 interactive Plotly charts with real analysis data |
| **Report Generator** | HTML, PDF, JSON, CSV report generation |
| **History Database** | SQLite storage for analysis persistence |
| **Security Pattern Library** | Searchable, filterable pattern catalogue |
""",
        "Technology Stack": """
| Technology | Purpose | Version |
|-----------|---------|---------|
| Python | Primary language | 3.11+ |
| Streamlit | Web application framework | 1.35+ |
| Plotly | Interactive charts and graphs | 5.x |
| NetworkX | Graph construction for architecture | 3.x |
| Pandas | Data manipulation and CSV export | 2.x |
| PyYAML | YAML architecture parsing | 6.x |
| ReportLab | PDF report generation | 4.x |
| SQLite3 | Analysis history database | Built-in |
| Jinja2 | HTML template engine | 3.x |
| hashlib | File identification | Built-in |
| pathlib | Safe file path handling | Built-in |
| pytest | Automated testing | 7.x |
""",
        "Functional Requirements": """
1. The system shall accept architecture files in JSON, YAML, XML, and PlantUML formats.
2. The system shall validate uploaded architecture files and report errors clearly.
3. The system shall extract components, data flows, trust boundaries, and attributes.
4. The system shall apply STRIDE threat modeling rules to every component and data flow.
5. The system shall calculate risk scores (Likelihood × Impact, 1–25 scale).
6. The system shall classify risks as Low, Medium, High, or Critical.
7. The system shall map each threat to relevant security design patterns.
8. The system shall generate prioritised, architecture-specific recommendations.
9. The system shall display an interactive architecture graph.
10. The system shall provide a dashboard with at least 9 interactive charts.
11. The system shall generate downloadable HTML, PDF, JSON, and CSV reports.
12. The system shall save analysis results to a persistent SQLite database.
13. The system shall allow users to reload, compare, and delete previous analyses.
14. The system shall provide built-in sample architectures for demonstration.
""",
        "Non-Functional Requirements": """
- **Performance:** Analysis of a 15-component architecture shall complete within 5 seconds.
- **Usability:** Interface must be usable by a developer without security expertise.
- **Reliability:** Application must not crash on invalid input; all errors handled gracefully.
- **Security:** Uploaded files must be validated; no code execution of uploads; parameterised SQL.
- **Portability:** Must run on Windows, macOS, and Linux without modification.
- **Deployability:** Must deploy to Streamlit Community Cloud without additional configuration.
- **Maintainability:** Code must be modular, documented, and follow PEP 8 standards.
""",
        "Future Scope": """
1. **ML-Enhanced Threat Detection**: Train models on CVE databases for pattern recognition.
2. **Real-Time Collaboration**: Multi-user architecture assessment with shared sessions.
3. **IDE Integration**: VS Code extension for in-editor architecture assessment.
4. **CI/CD Integration**: GitHub Actions workflow to assess architecture on every commit.
5. **Custom Rule Engine**: Allow organisations to define custom threat detection rules.
6. **MITRE ATT&CK Mapping**: Map threats to MITRE ATT&CK tactics and techniques.
7. **Compliance Mapping**: Map recommendations to GDPR, HIPAA, PCI-DSS, ISO 27001 controls.
8. **Architecture Comparison**: Side-by-side comparison of secure vs insecure architecture versions.
9. **Export to Threat Dragon**: Export results to OWASP Threat Dragon format for further analysis.
10. **User Authentication**: Multi-user support with role-based access control.
""",
        "Conclusion": """
The Security-Centric Architecture Assessment Framework successfully demonstrates that security 
assessment can and should begin at the architecture design stage. By providing automated STRIDE 
threat analysis, transparent risk scoring, curated security pattern recommendations, and professional 
report generation — all without requiring code or deployment — the framework fills a genuine gap 
in the software security toolchain.

The framework is practical, demonstrable, and extensible. It can serve as both an academic 
research prototype and a foundation for production-ready architecture security tooling.
""",
    }

    for title, content in sections.items():
        with st.expander(f"📝 {title}", expanded=(title == "Abstract")):
            st.markdown(content)
