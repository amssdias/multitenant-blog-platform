from dataclasses import FrozenInstanceError

from django.core import mail
from django.test import TestCase, SimpleTestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.users.exceptions import EmailVerificationUserNotFound, EmailAlreadyVerified
from apps.users.services.emails.verification import build_email_verification_payload, EmailVerificationEmailData, \
    get_verification_url, send_verification_email, activate_user_email
from apps.users.tests.factories.users import UserFactory


class BuildEmailVerificationPayloadTests(TestCase):
    def test_raises_value_error_when_user_has_no_email(self):
        user = UserFactory(email="")

        with self.assertRaisesMessage(ValueError, str(_("User has no email."))):
            build_email_verification_payload(user=user)

    def test_returns_payload_with_expected_fields(self):
        user = UserFactory(username="test", email="test@example.com")

        payload = build_email_verification_payload(user=user)

        self.assertIsInstance(payload, EmailVerificationEmailData)
        self.assertEqual(payload.username, "test")
        self.assertEqual(payload.email, "test@example.com")
        self.assertTrue(payload.token)

    def test_token_contains_user_id_string(self):
        user = UserFactory()

        payload = build_email_verification_payload(user=user)

        self.assertTrue(payload.token.startswith(f"{user.id}:"))

    def test_payload_is_immutable_if_dataclass_is_frozen(self):
        user = UserFactory()
        payload = build_email_verification_payload(user=user)

        with self.assertRaises(FrozenInstanceError):
            payload.email = "other@example.com"


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class GetVerificationUrlTests(SimpleTestCase):
    def test_builds_absolute_url_from_scheme_host_and_reversed_path(self):
        token = "abc123"
        scheme = "https"
        host = "bloggies.com"

        expected_path = reverse("users:verify_email", kwargs={"token": token})
        expected_url = f"{scheme}://{host}{expected_path}"

        self.assertEqual(get_verification_url(token, scheme, host), expected_url)

    def test_includes_token_in_path(self):
        token = "my-token"
        url = get_verification_url(token, "https", "bloggies.com")

        expected_path = reverse("users:verify_email", kwargs={"token": token})
        self.assertTrue(url.endswith(expected_path))


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class SendVerificationEmailTests(SimpleTestCase):
    def test_sends_email_to_user_and_message_contains_verification_url(self):
        payload = EmailVerificationEmailData(
            username="test",
            email="test@example.com",
            token="tok123",
        )
        host = "bloggies.test:8000"
        scheme = "http"

        send_verification_email(payload, host=host, scheme=scheme)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [payload.email])

        # only assert URL presence (not full body text)
        expected_path = reverse("users:verify_email", kwargs={"token": payload.token})
        expected_url = f"{scheme}://{host}{expected_path}"
        self.assertIn(expected_url, email.body)

    @override_settings(DEFAULT_FROM_EMAIL=None)
    def test_allows_default_from_email_none(self):
        payload = EmailVerificationEmailData(
            username="test",
            email="test@example.com",
            token="tok123",
        )

        send_verification_email(payload, host="bloggies.test:8000", scheme="http")

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIsNone(email.from_email)
        self.assertEqual(email.to, [payload.email])


class ActivateUserEmailTests(TestCase):
    def test_raises_user_not_found_when_user_does_not_exist(self):
        with self.assertRaises(EmailVerificationUserNotFound):
            activate_user_email(user_id=999999)

    def test_raises_email_already_verified_when_user_is_already_active(self):
        user = UserFactory(is_active=True)

        with self.assertRaises(EmailAlreadyVerified):
            activate_user_email(user_id=user.id)

    def test_activates_inactive_user_and_persists_change(self):
        user = UserFactory(is_active=False)

        activate_user_email(user_id=user.id)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
