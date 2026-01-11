from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

EMAIL_VERIFICATION_SALT = "users.email_verification"


def create_email_verification_token(user_id: int) -> str:
    signer = TimestampSigner(salt=EMAIL_VERIFICATION_SALT)
    return signer.sign(str(user_id))


def verify_email_token(token: str, max_age_seconds: int = 60 * 60 * 24) -> int:
    """Validates a token and returns the user_id inside it."""
    signer = TimestampSigner(salt=EMAIL_VERIFICATION_SALT)
    user_id_str = signer.unsign(token, max_age=max_age_seconds)
    return int(user_id_str)
