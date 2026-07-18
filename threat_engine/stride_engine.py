"""
STRIDE threat analysis engine.
Applies rule sets to every component and data flow in an architecture.
"""
from __future__ import annotations
import logging
from typing import List

from core.models import Architecture, Threat
from threat_engine.threat_rules import COMPONENT_RULES, FLOW_RULES

logger = logging.getLogger(__name__)

_SEVERITY_ORDER = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


def _risk_score(likelihood: int, impact: int) -> int:
    return likelihood * impact


def _severity_from_score(score: int) -> str:
    if score <= 4:
        return "Low"
    if score <= 9:
        return "Medium"
    if score <= 16:
        return "High"
    return "Critical"


class STRIDEEngine:
    """Applies all STRIDE rules to an Architecture and returns a list of Threats."""

    def analyze(self, arch: Architecture) -> List[Threat]:
        threats: List[Threat] = []

        # Component-level analysis
        for component in arch.components:
            for rule in COMPONENT_RULES:
                try:
                    if rule["check"](component, arch):
                        score = _risk_score(rule["likelihood"], rule["impact"])
                        t = Threat(
                            id                   = f"{rule['id']}-{component.id}",
                            stride_category      = rule["stride_category"],
                            title                = rule["title"],
                            description          = rule["description"],
                            affected_component   = component.name,
                            detection_reason     = f"Rule {rule['id']} triggered on component '{component.name}'.",
                            potential_impact     = rule.get("mitigation", ""),
                            likelihood           = rule["likelihood"],
                            impact               = rule["impact"],
                            risk_score           = score,
                            severity             = _severity_from_score(score),
                            recommended_patterns = rule.get("patterns", []),
                            mitigation           = rule.get("mitigation", ""),
                            evidence             = rule["evidence_fn"](component, arch),
                        )
                        threats.append(t)
                        logger.debug("Threat detected: %s on %s", t.title, component.name)
                except Exception as exc:
                    logger.warning("Rule %s failed on component %s: %s", rule["id"], component.name, exc)

        # Data-flow level analysis
        for flow in arch.data_flows:
            for rule in FLOW_RULES:
                try:
                    if rule["check"](flow, arch):
                        score = _risk_score(rule["likelihood"], rule["impact"])
                        t = Threat(
                            id                   = f"{rule['id']}-{flow.id}",
                            stride_category      = rule["stride_category"],
                            title                = rule["title"],
                            description          = rule["description"],
                            affected_component   = f"{flow.source} → {flow.destination}",
                            affected_flow        = flow.id,
                            detection_reason     = f"Rule {rule['id']} triggered on flow {flow.source}→{flow.destination}.",
                            potential_impact     = rule.get("mitigation", ""),
                            likelihood           = rule["likelihood"],
                            impact               = rule["impact"],
                            risk_score           = score,
                            severity             = _severity_from_score(score),
                            recommended_patterns = rule.get("patterns", []),
                            mitigation           = rule.get("mitigation", ""),
                            evidence             = rule["evidence_fn"](flow, arch),
                        )
                        threats.append(t)
                except Exception as exc:
                    logger.warning("Rule %s failed on flow %s→%s: %s",
                                   rule["id"], flow.source, flow.destination, exc)

        # Deduplicate same rule + same component
        seen: set = set()
        unique: List[Threat] = []
        for t in threats:
            key = (t.stride_category, t.title, t.affected_component)
            if key not in seen:
                seen.add(key)
                unique.append(t)

        # Sort: Critical → High → Medium → Low
        unique.sort(key=lambda t: _SEVERITY_ORDER.get(t.severity, 0), reverse=True)
        return unique
