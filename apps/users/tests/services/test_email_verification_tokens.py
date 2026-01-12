from django.test import SimpleTestCase
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

from apps.users.services.tokens.email_verification import (
    EMAIL_VERIFICATION_SALT,
    create_email_verification_token,
    verify_email_token,
)


class EmailVerificationTokenTests(SimpleTestCase):
    def test_create_token_returns_non_empty_string(self):
        token = create_email_verification_token(123)
        self.assertIsInstance(token, str)
        self.assertTrue(token)

    def test_verify_token_returns_same_user_id(self):
        user_id = 123
        token = create_email_verification_token(user_id)

        result = verify_email_token(token, max_age_seconds=60 * 60)
        self.assertEqual(result, user_id)

    def test_verify_token_raises_bad_signature_when_tampered(self):
        token = create_email_verification_token(123)

        tampered = token + "x"

        with self.assertRaises(BadSignature):
            verify_email_token(tampered, max_age_seconds=60 * 60)

    def test_verify_token_raises_signature_expired_when_max_age_is_zero(self):
        token = create_email_verification_token(123)

        # max_age=0 means "must be created right now" — even tiny delay can fail.
        # Use a tiny max_age to make the test deterministic:
        with self.assertRaises(SignatureExpired):
            verify_email_token(token, max_age_seconds=-1)

    def test_verify_token_raises_value_error_when_payload_is_not_int(self):
        signer = TimestampSigner(salt=EMAIL_VERIFICATION_SALT)
        token = signer.sign("not-an-int")

        with self.assertRaises(ValueError):
            verify_email_token(token, max_age_seconds=60 * 60)
