"""JSON architecture parser."""
from __future__ import annotations
import json
from core.models import Architecture, Component, DataFlow, TrustBoundary
from core.validators import safe_bool, safe_str
from core.exceptions import ParseError
from parsers.base_parser import BaseParser


class JSONParser(BaseParser):
    def parse(self, content: str) -> Architecture:
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ParseError(f"Invalid JSON: {e}") from e
        return _build_architecture(data)


def _build_architecture(data: dict) -> Architecture:
    arch = Architecture(
        name        = safe_str(data.get("name"), "Unnamed Architecture"),
        description = safe_str(data.get("description")),
    )
    if "id" in data:
        arch.id = safe_str(data["id"]) or arch.id

    # Components
    for raw in data.get("components", []):
        arch.components.append(_build_component(raw))

    # Data flows
    for raw in data.get("data_flows", data.get("dataFlows", [])):
        arch.data_flows.append(_build_flow(raw))

    # Trust boundaries
    for raw in data.get("trust_boundaries", data.get("trustBoundaries", [])):
        arch.trust_boundaries.append(_build_boundary(raw))

    arch.external_entities = data.get("external_entities", data.get("externalEntities", []))
    arch.assets             = data.get("assets", [])
    arch.metadata           = data.get("metadata", {})
    return arch


def _build_component(raw: dict) -> Component:
    c = Component(
        name              = safe_str(raw.get("name")),
        type              = safe_str(raw.get("type"), "service"),
        description       = safe_str(raw.get("description")),
        zone              = safe_str(raw.get("zone"), "internal"),
        internet_facing   = safe_bool(raw.get("internet_facing", raw.get("internetFacing", False))),
        data_sensitivity  = safe_str(raw.get("data_sensitivity", raw.get("dataSensitivity")), "low"),
        authentication    = safe_bool(raw.get("authentication", True)),
        authorization     = safe_bool(raw.get("authorization", True)),
        encryption_at_rest= safe_bool(raw.get("encryption_at_rest", raw.get("encryptionAtRest", False))),
        logging_enabled   = safe_bool(raw.get("logging_enabled", raw.get("loggingEnabled", True))),
        rate_limiting     = safe_bool(raw.get("rate_limiting", raw.get("rateLimiting", False))),
        input_validation  = safe_bool(raw.get("input_validation", raw.get("inputValidation", True))),
        metadata          = raw.get("metadata", {}),
    )
    if "id" in raw:
        c.id = safe_str(raw["id"]) or c.id
    return c


def _build_flow(raw: dict) -> DataFlow:
    df = DataFlow(
        source               = safe_str(raw.get("source")),
        destination          = safe_str(raw.get("destination")),
        protocol             = safe_str(raw.get("protocol"), "HTTPS"),
        data                 = safe_str(raw.get("data")),
        encrypted            = safe_bool(raw.get("encrypted", True)),
        authenticated        = safe_bool(raw.get("authenticated", True)),
        crosses_trust_boundary = safe_bool(raw.get("crosses_trust_boundary", raw.get("crossesTrustBoundary", False))),
        bidirectional        = safe_bool(raw.get("bidirectional", False)),
        metadata             = raw.get("metadata", {}),
    )
    if "id" in raw:
        df.id = safe_str(raw["id"]) or df.id
    return df


def _build_boundary(raw: dict) -> TrustBoundary:
    tb = TrustBoundary(
        name        = safe_str(raw.get("name")),
        zone_from   = safe_str(raw.get("zone_from", raw.get("zoneFrom"))),
        zone_to     = safe_str(raw.get("zone_to", raw.get("zoneTo"))),
        description = safe_str(raw.get("description")),
    )
    if "id" in raw:
        tb.id = safe_str(raw["id"]) or tb.id
    return tb
