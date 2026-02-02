class EmailError(Exception):
    """Base exception for email integration."""


class EmailSendFailed(EmailError):
    """Raised when sending an email fails."""


class EmailTransientError(EmailError):
    """A temporary failure occurred. Retrying later may succeed."""


class EmailPermanentError(EmailError):
    """A non-recoverable failure occurred. Retrying won't help."""
