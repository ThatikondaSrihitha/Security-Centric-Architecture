"""Tests for STRIDE threat engine."""
import json
from pathlib import Path
import pytest

from parsers.json_parser import JSONParser
from threat_engine.stride_engine import STRIDEEngine
from core.models import Architecture, Component, DataFlow


def _ecommerce_arch():
    content = Path("data/sample_ecommerce.json").read_text()
    return JSONParser().parse(content)


def test_stride_detects_threats_on_ecommerce():
    arch    = _ecommerce_arch()
    engine  = STRIDEEngine()
    threats = engine.analyze(arch)
    assert len(threats) > 0


def test_stride_covers_all_categories():
    arch    = _ecommerce_arch()
    engine  = STRIDEEngine()
    threats = engine.analyze(arch)
    categories = {t.stride_category for t in threats}
    # E-commerce sample should produce all 6 STRIDE categories
    expected = {"Spoofing","Tampering","Repudiation","InformationDisclosure","DenialOfService","ElevationOfPrivilege"}
    assert expected.issubset(categories), f"Missing categories: {expected - categories}"


def test_threat_has_required_fields():
    arch    = _ecommerce_arch()
    threats = STRIDEEngine().analyze(arch)
    for t in threats:
        assert t.id
        assert t.title
        assert t.stride_category
        assert t.evidence
        assert 1 <= t.likelihood <= 5
        assert 1 <= t.impact     <= 5
        assert t.risk_score == t.likelihood * t.impact
        assert t.severity in ("Low","Medium","High","Critical")


def test_internet_facing_no_auth_generates_spoofing():
    arch = Architecture(name="Test")
    arch.components.append(Component(
        name="Public API", type="api",
        internet_facing=True, authentication=False,
    ))
    threats = STRIDEEngine().analyze(arch)
    spoof   = [t for t in threats if t.stride_category == "Spoofing"]
    assert len(spoof) > 0, "Expected at least one Spoofing threat for internet-facing component without auth"


def test_unencrypted_flow_generates_tampering():
    arch = Architecture(name="Test")
    arch.components.append(Component(name="A", type="service"))
    arch.components.append(Component(name="B", type="service"))
    arch.data_flows.append(DataFlow(source="A", destination="B", encrypted=False, protocol="HTTP"))
    threats = STRIDEEngine().analyze(arch)
    tam = [t for t in threats if t.stride_category == "Tampering"]
    assert len(tam) > 0


def test_no_logging_generates_repudiation():
    arch = Architecture(name="Test")
    arch.components.append(Component(
        name="Order Service", type="service",
        logging_enabled=False, data_sensitivity="high",
    ))
    threats = STRIDEEngine().analyze(arch)
    rep = [t for t in threats if t.stride_category == "Repudiation"]
    assert len(rep) > 0


def test_no_duplicate_threats():
    arch    = _ecommerce_arch()
    threats = STRIDEEngine().analyze(arch)
    keys = [(t.stride_category, t.title, t.affected_component) for t in threats]
    assert len(keys) == len(set(keys)), "Duplicate threats detected"
