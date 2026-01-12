from django.contrib.messages import get_messages
from django.core.signing import TimestampSigner
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.users.services.tokens.email_verification import (
    EMAIL_VERIFICATION_SALT,
    create_email_verification_token,
)
from apps.users.tests.factories.users import UserFactory


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class TestVerifyEmailView(TestCase):
    def setUp(self):
        self.user = UserFactory(
            username="dias",
            email="dias@example.com",
            password="StrongPass12345!",
            is_active=False,
        )

    def _url(self, token: str) -> str:
        return reverse("users:verify_email", kwargs={"token": token})

    def _messages_text(self, response):
        storage = list(get_messages(response.wsgi_request))
        return [m.message for m in storage]

    def test_valid_token_activates_user_and_redirects_with_success_message(self):
        token = create_email_verification_token(self.user.id)

        response = self.client.get(self._url(token), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("users:login"))

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        msgs = self._messages_text(response)
        self.assertIn(
            "Your email has been verified successfully. You can now log in.",
            msgs,
        )

    def test_already_active_user_redirects_with_info_message_and_keeps_active(self):
        self.user.is_active = True
        self.user.save(update_fields=["is_active"])

        token = create_email_verification_token(self.user.id)
        response = self.client.get(self._url(token), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("users:login"))

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        msgs = self._messages_text(response)
        self.assertIn("Your email is already activated", msgs)

    def test_invalid_token_redirects_with_error_message(self):
        response = self.client.get(self._url("not-a-valid-token"), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("users:login"))

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        msgs = self._messages_text(response)
        self.assertIn(
            "This verification link is invalid. Please request a new one.",
            msgs,
        )

    def test_token_with_non_int_user_id_valueerror_redirects_with_error(self):
        signer = TimestampSigner(salt=EMAIL_VERIFICATION_SALT)
        bad_payload_token = signer.sign("not-an-int")

        response = self.client.get(self._url(bad_payload_token), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("users:login"))

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        msgs = self._messages_text(response)
        self.assertIn(
            "This verification link is invalid. Please request a new one.",
            msgs,
        )

    def test_valid_token_but_user_does_not_exist_redirects_with_error(self):
        token = create_email_verification_token(999999999)

        response = self.client.get(self._url(token), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("users:login"))

        msgs = self._messages_text(response)
        self.assertIn(
            "We couldn’t find an account for this verification link.",
            msgs,
        )

    def test_invalid_token_does_not_activate_user(self):
        token = "totally-invalid"
        self.client.get(self._url(token), follow=False)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_expired_token_does_not_activate_user(self):
        with override_settings(EMAIL_VERIFICATION_TOKEN_MAX_AGE_SECONDS=0):
            token = create_email_verification_token(self.user.id)
            response = self.client.get(self._url(token), follow=False)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        msgs = self._messages_text(response)
        self.assertIn(
            "This verification link has expired. Please request a new one.",
            msgs,
        )
