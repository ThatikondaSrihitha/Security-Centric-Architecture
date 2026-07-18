"""End-to-end integration tests."""
import json
from pathlib import Path
import pytest

from parsers.json_parser import JSONParser
from core.analyzer import ArchitectureAnalyzer
from reports.report_generator import get_html_report, get_json_report, get_csv_threats


def _run_ecommerce() -> "AnalysisResult":
    content = Path("data/sample_ecommerce.json").read_text()
    arch    = JSONParser().parse(content)
    return ArchitectureAnalyzer().analyze(arch)


def test_end_to_end_ecommerce():
    result = _run_ecommerce()
    assert result.architecture.name == "E-Commerce System"
    assert len(result.threats)          > 0
    assert len(result.pattern_mappings) > 0
    assert len(result.recommendations)  > 0
    assert result.risk_summary["total_threats"] > 0
    assert result.risk_summary["overall_risk_level"] in ("Low","Medium","High","Critical")


def test_all_threats_have_patterns():
    result = _run_ecommerce()
    for t in result.threats:
        assert len(t.recommended_patterns) > 0, f"Threat {t.id} has no patterns"


def test_html_report_generated():
    result = _run_ecommerce()
    html   = get_html_report(result)
    assert "<html" in html.lower()
    assert "Security Assessment Report" in html
    assert result.architecture.name in html


def test_json_report_parseable():
    result   = _run_ecommerce()
    json_str = get_json_report(result)
    data     = json.loads(json_str)
    assert "analysis_id"  in data
    assert "threats"      in data
    assert "risk_summary" in data


def test_csv_threats():
    result  = _run_ecommerce()
    csv_str = get_csv_threats(result)
    lines   = csv_str.strip().splitlines()
    assert len(lines) > 1, "CSV should have header + at least one data row"
    assert "Severity" in lines[0]


def test_pdf_report_generated():
    result = _run_ecommerce()
    from reports.report_generator import get_pdf_report
    pdf = get_pdf_report(result)
    assert pdf[:4] == b"%PDF", "Output must start with PDF magic bytes"


def test_risk_summary_completeness():
    result = _run_ecommerce()
    rs     = result.risk_summary
    required_keys = [
        "total_threats","low_count","medium_count","high_count","critical_count",
        "avg_risk_score","max_risk_score","overall_risk_pct","overall_risk_level",
        "component_risk","stride_risk",
    ]
    for k in required_keys:
        assert k in rs, f"Missing key in risk_summary: {k}"


def test_analysis_result_serialisable():
    result = _run_ecommerce()
    d      = result.to_dict()
    # Must be JSON-serialisable
    json_str = json.dumps(d)
    data     = json.loads(json_str)
    assert data["analysis_id"] == result.analysis_id
