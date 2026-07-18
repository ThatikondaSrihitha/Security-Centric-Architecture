"""
Main analysis orchestrator – ties together all engines.
"""
from __future__ import annotations
from typing import Optional
import logging

from core.models import Architecture, AnalysisResult
from threat_engine.stride_engine import STRIDEEngine
from risk_engine.risk_calculator import RiskCalculator
from patterns.threat_pattern_mapper import ThreatPatternMapper
from recommendations.recommendation_engine import RecommendationEngine

logger = logging.getLogger(__name__)


class ArchitectureAnalyzer:
    """Runs a full security assessment on an Architecture object."""

    def __init__(self) -> None:
        self.stride_engine       = STRIDEEngine()
        self.risk_calculator     = RiskCalculator()
        self.pattern_mapper      = ThreatPatternMapper()
        self.recommendation_engine = RecommendationEngine()

    def analyze(self, arch: Architecture) -> AnalysisResult:
        logger.info("Starting analysis of '%s'", arch.name)

        # 1 – STRIDE threat detection
        threats = self.stride_engine.analyze(arch)
        logger.info("Detected %d threats", len(threats))

        # 2 – Risk calculation
        risk_summary = self.risk_calculator.calculate(threats, arch)
        logger.info("Risk summary computed: overall_risk=%s", risk_summary.get("overall_risk_level"))

        # 3 – Pattern mapping
        pattern_mappings = self.pattern_mapper.map(threats)
        logger.info("Mapped %d pattern associations", len(pattern_mappings))

        # 4 – Recommendations
        recommendations = self.recommendation_engine.generate(threats, pattern_mappings, arch)
        logger.info("Generated %d recommendations", len(recommendations))

        return AnalysisResult(
            architecture     = arch,
            threats          = threats,
            risk_summary     = risk_summary,
            pattern_mappings = pattern_mappings,
            recommendations  = recommendations,
        )
