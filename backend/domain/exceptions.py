class BankError(Exception):
    """Base class for all bank-related (domain) errors."""


class ValidationError(BankError):
    """Raised when user input is invalid (e.g., negative deposit)."""


class AuthError(BankError):
    """Raised for authentication/authorization problems."""


class NotFoundError(BankError):
    """Raised when a requested entity does not exist."""


class InsufficientFundsError(BankError):
    """Raised when an account cannot withdraw the requested amount."""

