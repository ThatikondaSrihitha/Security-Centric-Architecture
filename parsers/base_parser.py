"""Base parser interface."""
from abc import ABC, abstractmethod
from core.models import Architecture


class BaseParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> Architecture:
        """Parse raw text content into an Architecture model."""
