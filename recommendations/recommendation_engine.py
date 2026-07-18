"""
Generates prioritised, architecture-specific recommendations from threats and pattern mappings.
"""
from __future__ import annotations
from typing import Any, Dict, List
import uuid

from core.models import Architecture, Threat
from patterns.security_patterns import get_pattern_by_name


_DIFFICULTY = {
    "Critical": "Medium",
    "High":     "Medium",
    "Medium":   "Low",
    "Low":      "Low",
}

_PRIORITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


class RecommendationEngine:
    def generate(
        self,
        threats: List[Threat],
        pattern_mappings: List[Dict],
        arch: Architecture,
    ) -> List[Dict[str, Any]]:

        recs: List[Dict[str, Any]] = []
        seen: set = set()

        for threat in sorted(threats, key=lambda t: _PRIORITY_ORDER.get(t.severity, 4)):
            # Primary recommendation: the threat mitigation
            key = (threat.title, threat.affected_component)
            if key not in seen:
                seen.add(key)
                pattern = threat.recommended_patterns[0] if threat.recommended_patterns else "General Security"
                p_data  = get_pattern_by_name(pattern)
                recs.append({
                    "id":             f"REC-{str(uuid.uuid4())[:6].upper()}",
                    "title":          f"Mitigate: {threat.title}",
                    "priority":       threat.severity,
                    "threat_id":      threat.id,
                    "threat_title":   threat.title,
                    "component":      threat.affected_component,
                    "pattern":        pattern,
                    "explanation":    threat.description,
                    "implementation": _impl_detail(threat, p_data),
                    "improvement":    _expected_improvement(threat),
                    "difficulty":     _DIFFICULTY.get(threat.severity, "Medium"),
                    "group":          _group_label(threat.severity),
                    "status":         "Open",
                })

        # Deduplicate very similar recommendations
        unique: List[Dict] = []
        used_titles: set = set()
        for r in recs:
            if r["title"] not in used_titles:
                used_titles.add(r["title"])
                unique.append(r)

        return unique


def _impl_detail(threat: Threat, pattern_data: Dict) -> str:
    base = threat.mitigation or "Apply appropriate security controls."
    if pattern_data:
        base += f"\n\nPattern guidance ({pattern_data['name']}): {pattern_data.get('implementation', '')}"
    return base


def _expected_improvement(threat: Threat) -> str:
    mapping = {
        "Spoofing":             "Reduces risk of identity fraud and account takeover.",
        "Tampering":            "Prevents data corruption and injection attacks.",
        "Repudiation":          "Enables forensic investigation and non-repudiation.",
        "InformationDisclosure":"Protects confidential data from exposure.",
        "DenialOfService":      "Improves system availability and resilience.",
        "ElevationOfPrivilege": "Limits blast radius of compromised accounts.",
    }
    return mapping.get(threat.stride_category, "Improves overall security posture.")


def _group_label(severity: str) -> str:
    if severity == "Critical":
        return "Immediate Actions"
    if severity == "High":
        return "High-Priority Improvements"
    if severity == "Medium":
        return "Medium-Priority Improvements"
    return "Best-Practice Enhancements"
