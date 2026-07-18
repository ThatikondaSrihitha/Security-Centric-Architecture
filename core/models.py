"""
Core data models for the Security Architecture Assessment Framework.
All parsers convert their input into these standardised models.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


def _uid() -> str:
    return str(uuid.uuid4())[:8]


# ────────────────────────────────────────────────────────────────────────────
@dataclass
class Component:
    id: str                        = field(default_factory=_uid)
    name: str                      = ""
    type: str                      = "service"          # service|database|user|external|api|queue|storage
    description: str               = ""
    zone: str                      = "internal"
    internet_facing: bool          = False
    data_sensitivity: str          = "low"             # low|medium|high|critical
    authentication: bool           = True
    authorization: bool            = True
    encryption_at_rest: bool       = False
    logging_enabled: bool          = True
    rate_limiting: bool            = False
    input_validation: bool         = True
    metadata: Dict[str, Any]       = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class DataFlow:
    id: str                        = field(default_factory=_uid)
    source: str                    = ""
    destination: str               = ""
    protocol: str                  = "HTTPS"
    data: str                      = ""
    encrypted: bool                = True
    authenticated: bool            = True
    crosses_trust_boundary: bool   = False
    bidirectional: bool            = False
    metadata: Dict[str, Any]       = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class TrustBoundary:
    id: str                  = field(default_factory=_uid)
    name: str                = ""
    zone_from: str           = ""
    zone_to: str             = ""
    description: str         = ""

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class Architecture:
    id: str                              = field(default_factory=_uid)
    name: str                            = "Unnamed Architecture"
    description: str                     = ""
    created_at: str                      = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    components: List[Component]          = field(default_factory=list)
    data_flows: List[DataFlow]           = field(default_factory=list)
    trust_boundaries: List[TrustBoundary]= field(default_factory=list)
    external_entities: List[str]         = field(default_factory=list)
    assets: List[Dict[str, Any]]         = field(default_factory=list)
    metadata: Dict[str, Any]             = field(default_factory=dict)

    # ── helpers ──────────────────────────────────────────────────────────────
    def get_component(self, name_or_id: str) -> Optional[Component]:
        for c in self.components:
            if c.id == name_or_id or c.name == name_or_id:
                return c
        return None

    def component_names(self) -> List[str]:
        return [c.name for c in self.components]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":               self.id,
            "name":             self.name,
            "description":      self.description,
            "created_at":       self.created_at,
            "components":       [c.to_dict() for c in self.components],
            "data_flows":       [d.to_dict() for d in self.data_flows],
            "trust_boundaries": [t.to_dict() for t in self.trust_boundaries],
            "external_entities":self.external_entities,
            "assets":           self.assets,
            "metadata":         self.metadata,
        }


# ────────────────────────────────────────────────────────────────────────────
@dataclass
class Threat:
    id: str                          = field(default_factory=_uid)
    stride_category: str             = ""   # Spoofing|Tampering|Repudiation|InformationDisclosure|DenialOfService|ElevationOfPrivilege
    title: str                       = ""
    description: str                 = ""
    affected_component: str          = ""
    affected_flow: str               = ""
    detection_reason: str            = ""
    potential_impact: str            = ""
    likelihood: int                  = 1
    impact: int                      = 1
    severity: str                    = "Low"
    risk_score: int                  = 1
    recommended_patterns: List[str]  = field(default_factory=list)
    mitigation: str                  = ""
    status: str                      = "Open"
    evidence: str                    = ""

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class AnalysisResult:
    architecture: Architecture
    threats: List[Threat]             = field(default_factory=list)
    risk_summary: Dict[str, Any]      = field(default_factory=dict)
    pattern_mappings: List[Dict]      = field(default_factory=list)
    recommendations: List[Dict]       = field(default_factory=list)
    analysis_id: str                  = field(default_factory=_uid)
    timestamp: str                    = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_id":      self.analysis_id,
            "timestamp":        self.timestamp,
            "architecture":     self.architecture.to_dict(),
            "threats":          [t.to_dict() for t in self.threats],
            "risk_summary":     self.risk_summary,
            "pattern_mappings": self.pattern_mappings,
            "recommendations":  self.recommendations,
        }
