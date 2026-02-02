class EmailVerificationError(Exception):
    """Base error for email verification flow."""


class EmailVerificationTokenExpired(EmailVerificationError):
    pass


class EmailVerificationTokenInvalid(EmailVerificationError):
    pass


class EmailVerificationUserNotFound(EmailVerificationError):
    pass


class EmailAlreadyVerified(EmailVerificationError):
    pass


class EmailVerificationFailed(EmailVerificationError):
    pass


class EmailVerificationFailedTransient(EmailVerificationFailed):
    """Verification email failed due to a temporary issue (retryable)."""


class EmailVerificationFailedPermanent(EmailVerificationFailed):
    """Verification email failed due to a permanent issue (non-retryable)."""
