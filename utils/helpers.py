"""General helper utilities."""
from __future__ import annotations
import hashlib
import re
from pathlib import Path
from typing import Optional

from config import MAX_UPLOAD_MB, ALLOWED_EXTENSIONS


def validate_upload(filename: str, size_bytes: int) -> tuple[bool, str]:
    """Return (valid, error_message)."""
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type '{suffix}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    if size_bytes > MAX_UPLOAD_MB * 1024 * 1024:
        return False, f"File exceeds {MAX_UPLOAD_MB} MB limit."
    return True, ""


def sanitise_filename(name: str) -> str:
    """Remove path-traversal characters from filenames."""
    return re.sub(r"[^\w\-.]", "_", Path(name).name)


def file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()[:16]


def truncate(text: str, max_len: int = 80) -> str:
    return text if len(text) <= max_len else text[:max_len] + "…"
