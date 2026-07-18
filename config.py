"""
Application configuration for Security-Centric Architecture Assessment Framework.
Edit student details here - they appear on the About page and in reports.
"""

# ── Student & Academic Details ──────────────────────────────────────────────
STUDENT_NAME = "Your Name"
ROLL_NUMBER  = "XXXX-XX-XXXX"
DEPARTMENT   = "Computer Science & Engineering"
COLLEGE      = "Your College Name"
GUIDE_NAME   = "Prof. Guide Name"
ACADEMIC_YEAR = "2025-2026"

# ── Application Meta ─────────────────────────────────────────────────────────
APP_NAME     = "Security-Centric Architecture Assessment Framework"
APP_TAGLINE  = "Analyze, Assess, and Secure Software Architecture Before Coding Begins."
APP_VERSION  = "1.0.0"
APP_DOMAIN   = "Cybersecurity & Software Architecture"
APP_CONCEPT  = "Security by Design"
APP_METHOD   = "STRIDE Threat Modeling"

# ── File & Upload Limits ──────────────────────────────────────────────────────
MAX_UPLOAD_MB          = 10
ALLOWED_EXTENSIONS     = {".json", ".yaml", ".yml", ".xml", ".puml", ".txt"}
GENERATED_REPORTS_DIR  = "generated_reports"
DATABASE_PATH          = "database/security_framework.db"
LOG_PATH               = "logs/app.log"

# ── Risk Thresholds ───────────────────────────────────────────────────────────
RISK_LOW      = (1, 4)
RISK_MEDIUM   = (5, 9)
RISK_HIGH     = (10, 16)
RISK_CRITICAL = (17, 25)
