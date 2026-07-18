"""Application logging setup."""
import logging
import os
from pathlib import Path

from config import LOG_PATH


def setup_logging() -> None:
    log_path = Path(LOG_PATH)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(str(log_path), encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logging.getLogger("streamlit").setLevel(logging.WARNING)
