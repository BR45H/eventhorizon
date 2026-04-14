#Custom exception hierarchy for Event Horizon.

class EventHorizonError(Exception):
    """Base exception for all expected Event Horizon errors."""


class TargetError(EventHorizonError):
    """Raised when target parsing, normalization, or loading fails."""


class ValidationError(EventHorizonError):
    """Raised when user input or argument combinations are invalid."""


class FileInputError(EventHorizonError):
    """Raised when a required file is missing, unreadable, or invalid."""