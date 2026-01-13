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
