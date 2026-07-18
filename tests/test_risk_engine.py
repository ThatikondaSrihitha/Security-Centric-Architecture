"""Tests for risk calculator."""
import pytest
from core.models import Architecture, Threat
from risk_engine.risk_calculator import RiskCalculator, _classify


def _make_threat(likelihood: int, impact: int, severity: str = "Medium") -> Threat:
    t = Threat()
    t.likelihood    = likelihood
    t.impact        = impact
    t.risk_score    = likelihood * impact
    t.severity      = severity
    t.stride_category = "Spoofing"
    t.affected_component = "TestComponent"
    return t


def test_risk_classification():
    assert _classify(1)  == "Low"
    assert _classify(4)  == "Low"
    assert _classify(5)  == "Medium"
    assert _classify(9)  == "Medium"
    assert _classify(10) == "High"
    assert _classify(16) == "High"
    assert _classify(17) == "Critical"
    assert _classify(25) == "Critical"


def test_risk_score_formula():
    t = _make_threat(3, 4)
    assert t.risk_score == 12  # 3 × 4


def test_calculate_empty_threats():
    arch = Architecture(name="Test")
    rs   = RiskCalculator().calculate([], arch)
    assert rs["total_threats"]   == 0
    assert rs["overall_risk_pct"] == 0


def test_calculate_with_threats():
    arch = Architecture(name="Test")
    arch.components = []
    threats = [
        _make_threat(5, 5, "Critical"),   # score = 25
        _make_threat(3, 3, "Medium"),     # score = 9
        _make_threat(1, 1, "Low"),        # score = 1
    ]
    rs = RiskCalculator().calculate(threats, arch)
    assert rs["total_threats"]    == 3
    assert rs["critical_count"]   == 1
    assert rs["medium_count"]     == 1
    assert rs["low_count"]        == 1
    assert rs["max_risk_score"]   == 25
    assert rs["avg_risk_score"]   == pytest.approx((25 + 9 + 1) / 3, abs=0.01)


def test_overall_risk_percentage():
    arch    = Architecture(name="Test")
    threats = [_make_threat(5, 5, "Critical")]
    rs      = RiskCalculator().calculate(threats, arch)
    assert rs["overall_risk_pct"] == 100.0


def test_component_risk_tracking():
    arch = Architecture(name="Test")
    t1 = _make_threat(4, 4, "High")
    t1.affected_component = "API Gateway"
    t2 = _make_threat(2, 2, "Low")
    t2.affected_component = "Auth Service"
    rs = RiskCalculator().calculate([t1, t2], arch)
    assert "API Gateway"   in rs["component_risk"]
    assert "Auth Service"  in rs["component_risk"]
    assert rs["component_risk"]["API Gateway"]["score"] == 16
