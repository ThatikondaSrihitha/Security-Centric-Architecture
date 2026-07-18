"""Tests for architecture parsers."""
import json
import pytest
from pathlib import Path

from parsers.json_parser    import JSONParser
from parsers.yaml_parser    import YAMLParser
from parsers.xml_parser     import XMLParser
from parsers.plantuml_parser import PlantUMLParser
from core.exceptions import ParseError


# ── JSON ─────────────────────────────────────────────────────────────────────

def test_json_parser_ecommerce():
    content = Path("data/sample_ecommerce.json").read_text()
    arch = JSONParser().parse(content)
    assert arch.name == "E-Commerce System"
    assert len(arch.components) >= 10
    assert len(arch.data_flows) >= 10
    assert len(arch.trust_boundaries) >= 3


def test_json_parser_minimal():
    data = {
        "name": "Test Arch",
        "components": [{"name":"Service A","type":"service"}],
        "data_flows": [],
    }
    arch = JSONParser().parse(json.dumps(data))
    assert arch.name == "Test Arch"
    assert len(arch.components) == 1


def test_json_parser_invalid():
    with pytest.raises(ParseError):
        JSONParser().parse("not valid json {{{")


def test_json_parser_defaults():
    """Missing optional fields should be populated with safe defaults."""
    data = {"name":"Minimal","components":[{"name":"X"}]}
    arch = JSONParser().parse(json.dumps(data))
    c = arch.components[0]
    assert c.type == "service"
    assert c.authentication is True


# ── YAML ──────────────────────────────────────────────────────────────────────

def test_yaml_parser_banking():
    content = Path("data/sample_banking.yaml").read_text()
    arch = YAMLParser().parse(content)
    assert "Banking" in arch.name
    assert len(arch.components) >= 5
    assert len(arch.data_flows)  >= 4


def test_yaml_parser_invalid():
    with pytest.raises(ParseError):
        YAMLParser().parse(": : invalid: yaml: - -")


def test_yaml_parser_inline():
    yaml_content = """
name: YAML Test
components:
  - name: Auth Service
    type: service
    authentication: true
    authorization: false
data_flows:
  - source: Auth Service
    destination: Auth Service
    protocol: HTTPS
"""
    arch = YAMLParser().parse(yaml_content)
    assert arch.name == "YAML Test"
    assert arch.components[0].authorization is False


# ── XML ───────────────────────────────────────────────────────────────────────

def test_xml_parser_hospital():
    content = Path("data/sample_hospital.xml").read_text()
    arch = XMLParser().parse(content)
    assert "Hospital" in arch.name
    assert len(arch.components) >= 5
    assert len(arch.data_flows)  >= 4


def test_xml_parser_invalid():
    with pytest.raises(ParseError):
        XMLParser().parse("<broken><xml>")


def test_xml_parser_inline():
    xml_content = """<architecture name="XML Test">
  <components>
    <component name="Web App" type="service" internet_facing="true" authentication="false"/>
    <component name="Database" type="database" data_sensitivity="critical"/>
  </components>
  <data_flows>
    <flow source="Web App" destination="Database" protocol="SQL" encrypted="false"/>
  </data_flows>
</architecture>"""
    arch = XMLParser().parse(xml_content)
    assert len(arch.components) == 2
    assert arch.components[0].internet_facing is True
    assert arch.components[0].authentication is False
    assert arch.components[1].data_sensitivity == "critical"


# ── PlantUML ─────────────────────────────────────────────────────────────────

def test_plantuml_parser_microservices():
    content = Path("data/sample_microservices.puml").read_text()
    arch = PlantUMLParser().parse(content)
    assert len(arch.components) >= 5
    assert len(arch.data_flows)  >= 5


def test_plantuml_inline():
    puml = """
@startuml
title My Service
component "Service A" as SA
database "DB B" as DB
SA -> DB : SQL query
@enduml
"""
    arch = PlantUMLParser().parse(puml)
    assert arch.name == "My Service"
    assert any(c.name == "Service A" for c in arch.components)
    assert len(arch.data_flows) >= 1
