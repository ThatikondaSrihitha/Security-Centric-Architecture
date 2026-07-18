"""XML architecture parser."""
from __future__ import annotations
import xml.etree.ElementTree as ET
from core.models import Architecture, Component, DataFlow, TrustBoundary
from core.validators import safe_bool, safe_str
from core.exceptions import ParseError
from parsers.base_parser import BaseParser


def _attr(el: ET.Element, key: str, default: str = "") -> str:
    return safe_str(el.get(key, el.get(key.lower(), default)), default)

def _bool_attr(el: ET.Element, key: str, default: bool = False) -> bool:
    v = el.get(key, el.get(key.lower()))
    if v is None:
        return default
    return safe_bool(v, default)


class XMLParser(BaseParser):
    def parse(self, content: str) -> Architecture:
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            raise ParseError(f"Invalid XML: {e}") from e

        arch = Architecture(
            name        = _attr(root, "name", "Unnamed Architecture"),
            description = _attr(root, "description"),
        )
        if root.get("id"):
            arch.id = root.get("id")

        # Components
        for section in root.findall("components"):
            for el in section.findall("component"):
                arch.components.append(_parse_component(el))
        # Also support flat <component> directly under root
        for el in root.findall("component"):
            arch.components.append(_parse_component(el))

        # Data flows
        for section in root.findall("data_flows") + root.findall("dataFlows"):
            for el in section.findall("flow") + section.findall("dataFlow"):
                arch.data_flows.append(_parse_flow(el))
        for el in root.findall("flow") + root.findall("dataFlow"):
            arch.data_flows.append(_parse_flow(el))

        # Trust boundaries
        for section in root.findall("trust_boundaries") + root.findall("trustBoundaries"):
            for el in section.findall("boundary") + section.findall("trustBoundary"):
                arch.trust_boundaries.append(_parse_boundary(el))

        return arch


def _parse_component(el: ET.Element) -> Component:
    c = Component(
        name               = _attr(el, "name"),
        type               = _attr(el, "type", "service"),
        description        = _attr(el, "description"),
        zone               = _attr(el, "zone", "internal"),
        internet_facing    = _bool_attr(el, "internet_facing"),
        data_sensitivity   = _attr(el, "data_sensitivity", "low"),
        authentication     = _bool_attr(el, "authentication", True),
        authorization      = _bool_attr(el, "authorization", True),
        encryption_at_rest = _bool_attr(el, "encryption_at_rest"),
        logging_enabled    = _bool_attr(el, "logging_enabled", True),
        rate_limiting      = _bool_attr(el, "rate_limiting"),
        input_validation   = _bool_attr(el, "input_validation", True),
    )
    if el.get("id"):
        c.id = el.get("id")
    return c


def _parse_flow(el: ET.Element) -> DataFlow:
    df = DataFlow(
        source                 = _attr(el, "source"),
        destination            = _attr(el, "destination"),
        protocol               = _attr(el, "protocol", "HTTPS"),
        data                   = _attr(el, "data"),
        encrypted              = _bool_attr(el, "encrypted", True),
        authenticated          = _bool_attr(el, "authenticated", True),
        crosses_trust_boundary = _bool_attr(el, "crosses_trust_boundary"),
        bidirectional          = _bool_attr(el, "bidirectional"),
    )
    if el.get("id"):
        df.id = el.get("id")
    return df


def _parse_boundary(el: ET.Element) -> TrustBoundary:
    tb = TrustBoundary(
        name        = _attr(el, "name"),
        zone_from   = _attr(el, "zone_from"),
        zone_to     = _attr(el, "zone_to"),
        description = _attr(el, "description"),
    )
    if el.get("id"):
        tb.id = el.get("id")
    return tb
