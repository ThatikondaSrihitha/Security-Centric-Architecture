"""Threat repository utilities – helpers for grouping / querying threats."""
from __future__ import annotations
from collections import defaultdict
from typing import Dict, List
from core.models import Threat


def group_by_stride(threats: List[Threat]) -> Dict[str, List[Threat]]:
    groups: Dict[str, List[Threat]] = defaultdict(list)
    for t in threats:
        groups[t.stride_category].append(t)
    return dict(groups)


def group_by_severity(threats: List[Threat]) -> Dict[str, List[Threat]]:
    groups: Dict[str, List[Threat]] = defaultdict(list)
    for t in threats:
        groups[t.severity].append(t)
    return dict(groups)


def group_by_component(threats: List[Threat]) -> Dict[str, List[Threat]]:
    groups: Dict[str, List[Threat]] = defaultdict(list)
    for t in threats:
        groups[t.affected_component].append(t)
    return dict(groups)
