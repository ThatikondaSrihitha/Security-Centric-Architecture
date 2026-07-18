# 🔐 Security-Centric Architecture Assessment Framework

> **Analyze, Assess, and Secure Software Architecture Before Coding Begins.**

A fully functional B.Tech Major Project that implements **Security by Design** through automated 
STRIDE threat modeling, risk assessment, security pattern mapping, and professional report generation 
— all operating on architecture diagrams **before any code is written**.

---

## 🎯 Project Overview

Traditional software security tools (OWASP ZAP, Burp Suite, SonarQube) require running code or 
deployed applications. This framework analyzes **architecture descriptions** at the design stage, 
identifying security vulnerabilities when they are cheapest to fix.

**Key capabilities:**
- Automated STRIDE threat modeling across 6 categories
- Likelihood × Impact risk scoring (1–25 scale)
- 24-pattern security design pattern library
- Prioritised architecture-specific recommendations
- Professional HTML, PDF, JSON, and CSV reports
- Interactive architecture visualization
- Analysis history with SQLite persistence

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Multi-Format Input** | JSON, YAML, XML, PlantUML architecture files |
| **STRIDE Engine** | 20+ rule-based threat detection rules |
| **Risk Calculator** | Likelihood × Impact with percentage normalisation |
| **Pattern Library** | 24 curated security design patterns |
| **Smart Recommendations** | Architecture-specific, grouped by priority |
| **Architecture Graph** | Interactive NetworkX + Plotly visualization |
| **9-Chart Dashboard** | Real-time charts from analysis results |
| **4-Format Reports** | HTML, PDF, JSON, CSV downloadable |
| **Analysis History** | SQLite storage for previous analyses |
| **One-Click Demo** | E-Commerce demo requires no file upload |

---

## 📱 Application Pages

1. **Home** – Landing page with workflow overview
2. **Security Dashboard** – 9 interactive charts and risk gauge
3. **New Architecture Assessment** – Upload, sample, or manual entry
4. **Architecture Visualization** – Interactive graph
5. **STRIDE Threat Analysis** – Detailed threat cards with evidence
6. **Risk Assessment** – Risk scores, matrix, component ranking
7. **Security Pattern Library** – Searchable 24-pattern catalogue
8. **Recommendations** – Prioritised remediation steps
9. **Reports** – HTML/PDF/JSON/CSV downloads
10. **Analysis History** – View, reload, delete previous analyses
11. **Methodology** – STRIDE explanation, risk formula, comparison
12. **Project Documentation** – Full academic documentation
13. **About** – Project and student information

---

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Primary language |
| Streamlit | 1.35+ | Web framework |
| Plotly | 5.22+ | Interactive charts |
| NetworkX | 3.3+ | Architecture graph |
| Pandas | 2.2+ | Data tables |
| PyYAML | 6.0+ | YAML parsing |
| ReportLab | 4.2+ | PDF generation |
| SQLite3 | Built-in | History database |
| pytest | 8.2+ | Automated testing |

---

## 📁 Folder Structure

```
security_architecture_framework/
│
├── app.py                      # Main Streamlit application
├── config.py                   # Student details and configuration
├── requirements.txt
├── runtime.txt
├── README.md
├── PROJECT_STATUS.md
│
├── core/                       # Core data models and analysis
│   ├── models.py               # Architecture, Component, DataFlow, Threat, AnalysisResult
│   ├── validators.py           # Input validation utilities
│   ├── analyzer.py             # Main analysis orchestrator
│   └── exceptions.py           # Custom exceptions
│
├── parsers/                    # Architecture file parsers
│   ├── json_parser.py
│   ├── yaml_parser.py
│   ├── xml_parser.py
│   └── plantuml_parser.py
│
├── threat_engine/              # STRIDE threat detection
│   ├── stride_engine.py        # Rule application engine
│   ├── threat_rules.py         # 20+ STRIDE rules
│   └── threat_repository.py   # Grouping utilities
│
├── risk_engine/
│   └── risk_calculator.py      # Risk scoring
│
├── patterns/                   # Security patterns
│   ├── security_patterns.py    # 24 curated patterns
│   └── threat_pattern_mapper.py
│
├── recommendations/
│   └── recommendation_engine.py
│
├── reports/                    # Report generation
│   ├── report_generator.py
│   ├── html_generator.py
│   └── pdf_generator.py
│
├── visualization/
│   ├── architecture_graph.py   # NetworkX + Plotly graph
│   └── dashboard_charts.py     # 9 Plotly charts
│
├── database/
│   └── db.py                   # SQLite operations
│
├── data/                       # Sample architectures
│   ├── sample_ecommerce.json
│   ├── sample_banking.yaml
│   ├── sample_hospital.xml
│   ├── sample_microservices.puml
│   └── sample_iot.json
│
├── pages/                      # Streamlit pages
│   ├── shared_styles.py        # CSS theme
│   ├── home.py
│   ├── dashboard.py
│   ├── assessment.py
│   ├── visualization.py
│   ├── threats.py
│   ├── risks.py
│   ├── patterns.py
│   ├── recommendations.py
│   ├── reports.py
│   ├── history.py
│   ├── methodology.py
│   ├── documentation.py
│   └── about.py
│
├── utils/
│   ├── helpers.py
│   ├── session_manager.py
│   └── logger.py
│
└── tests/
    ├── test_parsers.py
    ├── test_stride_engine.py
    ├── test_risk_engine.py
    └── test_integration.py
```

---

## 🚀 Installation & Running

### Windows

```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The application will open at: **http://localhost:8501**

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_parsers.py -v
pytest tests/test_integration.py -v
```

---

## 📐 Risk Formula

```
Risk Score = Likelihood (1–5) × Impact (1–5)

Classification:
  1–4   = Low Risk     (🟢)
  5–9   = Medium Risk  (🟡)
 10–16  = High Risk    (🟠)
 17–25  = Critical Risk (🔴)

Overall Risk % = (Average Risk Score / 25) × 100
```

---

## 🎯 STRIDE Categories

| Letter | Category | Description |
|--------|----------|-------------|
| **S** | Spoofing | Impersonating identity |
| **T** | Tampering | Modifying data or code |
| **R** | Repudiation | Denying performed actions |
| **I** | Information Disclosure | Data leakage |
| **D** | Denial of Service | Disrupting availability |
| **E** | Elevation of Privilege | Gaining unauthorised access |

---

## 📥 Sample Input Formats

### JSON
```json
{
  "name": "My Architecture",
  "components": [
    {"name": "API Gateway", "type": "api", "internet_facing": true, "authentication": false}
  ],
  "data_flows": [
    {"source": "API Gateway", "destination": "API Gateway", "protocol": "HTTPS", "encrypted": false}
  ]
}
```

### YAML
```yaml
name: My Architecture
components:
  - name: Auth Service
    type: service
    authentication: true
    authorization: false
```

### PlantUML
```
@startuml
component "Web App" as WA
database "Database" as DB
WA -> DB : SQL query
@enduml
```

---

## 🌐 Deployment (Streamlit Community Cloud)

1. Push code to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select your repository, branch (`main`), and main file (`app.py`)
5. Click **Deploy**

The app starts automatically with `streamlit run app.py`.  
No secrets or API keys required.

---

## 📸 Screenshots

*(Add screenshots after deployment)*

- Home page
- E-Commerce Demo analysis running
- Architecture graph
- STRIDE threat cards
- Risk assessment dashboard
- Security pattern library
- PDF report download

---

## 🔮 Future Scope

- ML-enhanced threat detection from CVE databases
- MITRE ATT&CK mapping
- Compliance mapping (GDPR, HIPAA, PCI-DSS)
- CI/CD integration via GitHub Actions
- Custom rule engine for organisations
- Multi-user collaboration support

---

## ⚠️ Academic Disclaimer

This project is developed as a B.Tech Major Project for academic purposes. The security assessments 
generated are based on architectural analysis and should be supplemented with professional security 
reviews for production systems.

---

*Security-Centric Architecture Assessment Framework v1.0.0 | Security by Design | STRIDE Threat Modeling*
