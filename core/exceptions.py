"""Custom exceptions for the framework."""


class FrameworkError(Exception):
    """Base exception."""


class ParseError(FrameworkError):
    """Raised when architecture parsing fails."""


class ValidationError(FrameworkError):
    """Raised when architecture validation fails."""


class AnalysisError(FrameworkError):
    """Raised when threat analysis fails."""


class ReportError(FrameworkError):
    """Raised when report generation fails."""


class DatabaseError(FrameworkError):
    """Raised on database failures."""
