"""YAML architecture parser."""
from __future__ import annotations
import yaml
from core.exceptions import ParseError
from parsers.base_parser import BaseParser
from parsers.json_parser import _build_architecture
from core.models import Architecture


class YAMLParser(BaseParser):
    def parse(self, content: str) -> Architecture:
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ParseError(f"Invalid YAML: {e}") from e
        if not isinstance(data, dict):
            raise ParseError("YAML root must be a mapping (dictionary).")
        return _build_architecture(data)
