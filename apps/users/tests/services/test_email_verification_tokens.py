from unittest import TestCase

from django.core import signing
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.test import SimpleTestCase

from apps.users.exceptions import (
    EmailVerificationTokenExpired,
    EmailVerificationTokenInvalid,
)
from apps.users.services.tokens.email_verification import (
    EMAIL_VERIFICATION_SALT,
    create_email_verification_token,
    verify_email_token,
    get_user_id_from_verification_token,
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


class GetUserIdFromVerificationTokenTests(TestCase):
    def _make_timestamped_token_for_user_id(self, user_id: int) -> str:
        signer = signing.TimestampSigner(salt=EMAIL_VERIFICATION_SALT)
        return signer.sign(str(user_id))

    def test_raises_expired_when_token_is_expired(self):
        token = self._make_timestamped_token_for_user_id(123)

        # max_age_seconds=0 means "must be younger than 0 seconds" -> always expired
        with self.assertRaises(EmailVerificationTokenExpired):
            get_user_id_from_verification_token(token=token, max_age_seconds=0)

    def test_raises_invalid_when_token_is_garbage(self):
        token = "not-a-real-token"

        with self.assertRaises(EmailVerificationTokenInvalid):
            get_user_id_from_verification_token(token=token, max_age_seconds=3600)

    def test_raises_invalid_when_token_is_tampered(self):
        token = self._make_timestamped_token_for_user_id(123)

        tampered = token + "x"

        with self.assertRaises(EmailVerificationTokenInvalid):
            get_user_id_from_verification_token(token=tampered, max_age_seconds=3600)

    def test_raises_invalid_when_token_payload_is_not_an_int(self):
        signer = signing.TimestampSigner()
        token = signer.sign("not-an-int")

        with self.assertRaises(EmailVerificationTokenInvalid):
            get_user_id_from_verification_token(token=token, max_age_seconds=3600)
