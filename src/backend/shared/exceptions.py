"""Custom exception hierarchy for Lambda services."""


class ValidationError(Exception):
    """Raised when input parameters are invalid."""


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""
