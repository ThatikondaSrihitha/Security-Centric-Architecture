"""
Risk calculation engine.
Formula: Risk Score = Likelihood (1-5) × Impact (1-5)
1-4   = Low
5-9   = Medium
10-16 = High
17-25 = Critical
"""
from __future__ import annotations
from collections import defaultdict
from typing import Any, Dict, List

from core.models import Architecture, Threat


def _classify(score: int) -> str:
    if score <= 4:
        return "Low"
    if score <= 9:
        return "Medium"
    if score <= 16:
        return "High"
    return "Critical"


class RiskCalculator:
    def calculate(self, threats: List[Threat], arch: Architecture) -> Dict[str, Any]:
        if not threats:
            return _empty_summary(arch)

        scores    = [t.risk_score for t in threats]
        total     = len(threats)
        avg_score = sum(scores) / total
        max_score = max(scores)

        counts: Dict[str, int] = defaultdict(int)
        for t in threats:
            counts[t.severity] += 1

        # Normalised overall risk
        # Formula: weighted blend of avg and critical threat ratio
        critical_ratio = counts.get("Critical", 0) / total
        high_ratio     = counts.get("High", 0) / total
        threat_weight  = (critical_ratio * 1.0 + high_ratio * 0.5)
        overall_pct    = min(100, round(((avg_score / 25) * 100 * (1 + threat_weight)), 1))
        overall_norm   = round(overall_pct / 100, 4)
        overall_level  = _classify(round(avg_score))

        # Component-level risk
        comp_risk: Dict[str, Dict] = defaultdict(lambda: {"score": 0, "count": 0, "level": "Low"})
        for t in threats:
            comp_risk[t.affected_component]["score"] = max(
                comp_risk[t.affected_component]["score"], t.risk_score
            )
            comp_risk[t.affected_component]["count"] += 1
            comp_risk[t.affected_component]["level"] = _classify(comp_risk[t.affected_component]["score"])

        # STRIDE category risk
        stride_risk: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "max_score": 0, "level": "Low"})
        for t in threats:
            stride_risk[t.stride_category]["count"] += 1
            stride_risk[t.stride_category]["max_score"] = max(
                stride_risk[t.stride_category]["max_score"], t.risk_score
            )
            stride_risk[t.stride_category]["level"] = _classify(stride_risk[t.stride_category]["max_score"])

        return {
            "total_threats":     total,
            "low_count":         counts.get("Low",      0),
            "medium_count":      counts.get("Medium",   0),
            "high_count":        counts.get("High",     0),
            "critical_count":    counts.get("Critical", 0),
            "avg_risk_score":    round(avg_score, 2),
            "max_risk_score":    max_score,
            "overall_risk_pct":  overall_pct,
            "overall_risk_norm": overall_norm,
            "overall_risk_level":overall_level,
            "component_risk":    dict(comp_risk),
            "stride_risk":       dict(stride_risk),
            "architecture_name": arch.name,
            "component_count":   len(arch.components),
            "flow_count":        len(arch.data_flows),
            "boundary_count":    len(arch.trust_boundaries),
        }


def _empty_summary(arch: Architecture) -> Dict[str, Any]:
    return {
        "total_threats": 0,
        "low_count": 0, "medium_count": 0,
        "high_count": 0, "critical_count": 0,
        "avg_risk_score": 0, "max_risk_score": 0,
        "overall_risk_pct": 0, "overall_risk_norm": 0,
        "overall_risk_level": "Low",
        "component_risk": {}, "stride_risk": {},
        "architecture_name": arch.name,
        "component_count": len(arch.components),
        "flow_count": len(arch.data_flows),
        "boundary_count": len(arch.trust_boundaries),
    }
