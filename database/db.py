"""
SQLite database layer for analysis history.
Uses parameterised queries exclusively to prevent SQL injection.
"""
from __future__ import annotations
import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import DATABASE_PATH

logger = logging.getLogger(__name__)
_DB_PATH = Path(DATABASE_PATH)


def _get_conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id            TEXT PRIMARY KEY,
                arch_name     TEXT NOT NULL,
                timestamp     TEXT NOT NULL,
                components    INTEGER DEFAULT 0,
                data_flows    INTEGER DEFAULT 0,
                threats       INTEGER DEFAULT 0,
                risk_score    REAL    DEFAULT 0,
                risk_level    TEXT    DEFAULT 'Low',
                filename      TEXT    DEFAULT '',
                result_json   TEXT    NOT NULL
            )
        """)
        conn.commit()
    logger.info("Database initialised at %s", _DB_PATH)


def save_analysis(result: "AnalysisResult") -> None:  # type: ignore[name-defined]
    """Persist a full AnalysisResult to history."""
    from core.models import AnalysisResult  # local import to avoid cycles
    try:
        rs  = result.risk_summary
        row = {
            "id":          result.analysis_id,
            "arch_name":   result.architecture.name,
            "timestamp":   result.timestamp,
            "components":  len(result.architecture.components),
            "data_flows":  len(result.architecture.data_flows),
            "threats":     len(result.threats),
            "risk_score":  rs.get("overall_risk_pct", 0),
            "risk_level":  rs.get("overall_risk_level", "Low"),
            "filename":    result.architecture.metadata.get("source_file", ""),
            "result_json": json.dumps(result.to_dict()),
        }
        with _get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO analysis_history
                    (id, arch_name, timestamp, components, data_flows,
                     threats, risk_score, risk_level, filename, result_json)
                VALUES
                    (:id, :arch_name, :timestamp, :components, :data_flows,
                     :threats, :risk_score, :risk_level, :filename, :result_json)
            """, row)
            conn.commit()
        logger.info("Analysis '%s' saved to history.", result.analysis_id)
    except Exception as exc:
        logger.error("Failed to save analysis: %s", exc)


def list_analyses() -> List[Dict[str, Any]]:
    """Return summary rows for all stored analyses."""
    init_db()
    try:
        with _get_conn() as conn:
            rows = conn.execute(
                "SELECT id, arch_name, timestamp, components, data_flows, "
                "threats, risk_score, risk_level, filename "
                "FROM analysis_history ORDER BY timestamp DESC"
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as exc:
        logger.error("Failed to list analyses: %s", exc)
        return []


def load_analysis(analysis_id: str) -> Optional[Dict[str, Any]]:
    """Load the full result JSON for a specific analysis."""
    init_db()
    try:
        with _get_conn() as conn:
            row = conn.execute(
                "SELECT result_json FROM analysis_history WHERE id = ?",
                (analysis_id,)
            ).fetchone()
        if row:
            return json.loads(row["result_json"])
        return None
    except Exception as exc:
        logger.error("Failed to load analysis %s: %s", analysis_id, exc)
        return None


def delete_analysis(analysis_id: str) -> bool:
    """Delete an analysis from history."""
    init_db()
    try:
        with _get_conn() as conn:
            conn.execute(
                "DELETE FROM analysis_history WHERE id = ?",
                (analysis_id,)
            )
            conn.commit()
        return True
    except Exception as exc:
        logger.error("Failed to delete analysis %s: %s", analysis_id, exc)
        return False
