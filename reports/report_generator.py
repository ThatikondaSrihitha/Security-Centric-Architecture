"""
Orchestrates generation and saving of all report formats.
"""
from __future__ import annotations
import csv
import io
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from config import GENERATED_REPORTS_DIR
from core.models import AnalysisResult
from reports.html_generator import generate_html
from reports.pdf_generator   import generate_pdf

logger = logging.getLogger(__name__)
_REPORT_DIR = Path(GENERATED_REPORTS_DIR)


def _safe_name(arch_name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in arch_name)


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_html_report(result: AnalysisResult) -> str:
    return generate_html(result)


def get_pdf_report(result: AnalysisResult) -> bytes:
    try:
        return generate_pdf(result)
    except Exception as exc:
        logger.error("PDF generation failed: %s", exc)
        raise


def get_json_report(result: AnalysisResult) -> str:
    return json.dumps(result.to_dict(), indent=2)


def get_csv_threats(result: AnalysisResult) -> str:
    out = io.StringIO()
    w   = csv.writer(out)
    w.writerow(["ID","Category","Title","Component","Severity","Risk Score",
                "Likelihood","Impact","Mitigation","Evidence"])
    for t in result.threats:
        w.writerow([t.id, t.stride_category, t.title, t.affected_component,
                    t.severity, t.risk_score, t.likelihood, t.impact,
                    t.mitigation, t.evidence])
    return out.getvalue()


def get_csv_recommendations(result: AnalysisResult) -> str:
    out = io.StringIO()
    w   = csv.writer(out)
    w.writerow(["ID","Priority","Title","Component","Pattern","Group",
                "Explanation","Difficulty","Status"])
    for r in result.recommendations:
        w.writerow([r["id"], r["priority"], r["title"], r["component"],
                    r["pattern"], r["group"], r["explanation"][:150],
                    r["difficulty"], r["status"]])
    return out.getvalue()


def build_filename(arch_name: str, ext: str) -> str:
    return f"{_safe_name(arch_name)}_security_assessment_{_timestamp()}.{ext}"
