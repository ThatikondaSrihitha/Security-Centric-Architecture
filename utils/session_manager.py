"""
Streamlit session-state management.
All keys are centralised here to prevent KeyError bugs.
"""
from __future__ import annotations
import streamlit as st
from typing import Any, Optional


_DEFAULTS: dict = {
    "current_architecture":   None,   # Architecture object
    "analysis_result":        None,   # AnalysisResult object
    "current_analysis_id":    None,   # str
    "current_page":           "Home",
    "demo_loaded":            False,
}


def init_session() -> None:
    """Initialise all session-state keys with defaults (only if not already set)."""
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def get(key: str, default: Any = None) -> Any:
    return st.session_state.get(key, default)


def set(key: str, value: Any) -> None:
    st.session_state[key] = value


def has_analysis() -> bool:
    """Always check directly from session_state — never cache."""
    result = st.session_state.get("analysis_result")
    return result is not None


def clear_analysis() -> None:
    for key in ["current_architecture", "analysis_result",
                "current_analysis_id", "demo_loaded", "analysis_ts"]:
        st.session_state.pop(key, None)
