"""
Architecture validation utilities.
"""
from __future__ import annotations
from typing import List, Tuple
from core.models import Architecture
from core.exceptions import ValidationError


def validate_architecture(arch: Architecture) -> Tuple[bool, List[str]]:
    """
    Validate an Architecture object.
    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []

    if not arch.name or arch.name.strip() == "":
        errors.append("Architecture name is required.")

    if not arch.components:
        errors.append("Architecture must have at least one component.")

    seen_ids: set = set()
    for c in arch.components:
        if not c.name:
            errors.append(f"Component with id '{c.id}' has no name.")
        if c.id in seen_ids:
            errors.append(f"Duplicate component id: '{c.id}'.")
        seen_ids.add(c.id)

    component_names = {c.name for c in arch.components}
    component_ids   = {c.id   for c in arch.components}
    valid_refs      = component_names | component_ids

    for df in arch.data_flows:
        if df.source not in valid_refs:
            errors.append(
                f"DataFlow '{df.id}' references unknown source: '{df.source}'."
            )
        if df.destination not in valid_refs:
            errors.append(
                f"DataFlow '{df.id}' references unknown destination: '{df.destination}'."
            )

    return (len(errors) == 0), errors


def safe_bool(value, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "yes", "1", "on")
    if isinstance(value, int):
        return value != 0
    return default


def safe_str(value, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def safe_int(value, default: int = 1, min_val: int = 1, max_val: int = 5) -> int:
    try:
        v = int(value)
        return max(min_val, min(max_val, v))
    except (TypeError, ValueError):
        return default
