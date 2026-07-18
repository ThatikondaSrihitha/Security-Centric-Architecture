"""Maps each detected threat to relevant security patterns."""
from __future__ import annotations
from typing import Any, Dict, List

from core.models import Threat
from patterns.security_patterns import PATTERN_BY_NAME, get_pattern_by_name

# STRIDE → default pattern names
_STRIDE_DEFAULTS: Dict[str, List[str]] = {
    "Spoofing":             ["Strong Authentication", "Multi-Factor Authentication",
                             "Secure Session Management", "Token-Based Authentication"],
    "Tampering":            ["Input Validation", "Integrity Verification",
                             "Digital Signatures", "Database Access Control",
                             "Encryption in Transit"],
    "Repudiation":          ["Secure Logging", "Audit Trail", "Digital Signatures"],
    "InformationDisclosure":["Encryption in Transit", "Encryption at Rest",
                             "Secrets Management", "Network Segmentation"],
    "DenialOfService":      ["Rate Limiting", "Circuit Breaker",
                             "Redundancy and Failover", "API Gateway"],
    "ElevationOfPrivilege": ["Role-Based Access Control", "Attribute-Based Access Control",
                             "Least Privilege", "Zero Trust"],
}


class ThreatPatternMapper:
    def map(self, threats: List[Threat]) -> List[Dict[str, Any]]:
        mappings: List[Dict[str, Any]] = []
        for threat in threats:
            # Collect pattern names from rule + STRIDE defaults, deduplicated
            pattern_names = list(dict.fromkeys(
                threat.recommended_patterns
                + _STRIDE_DEFAULTS.get(threat.stride_category, [])
            ))
            for name in pattern_names:
                p = get_pattern_by_name(name)
                if not p:
                    continue
                mappings.append({
                    "threat_id":        threat.id,
                    "threat_title":     threat.title,
                    "stride_category":  threat.stride_category,
                    "affected_element": threat.affected_component,
                    "pattern_id":       p["id"],
                    "pattern_name":     p["name"],
                    "pattern_category": p.get("category", ""),
                    "relevance":        _why_relevant(threat, p),
                    "implementation":   p.get("implementation", ""),
                    "priority":         p.get("priority", "Medium"),
                })
        return mappings


def _why_relevant(threat: Threat, pattern: Dict) -> str:
    return (
        f"The pattern '{pattern['name']}' directly addresses the "
        f"{threat.stride_category} threat by: {pattern['description']}"
    )
