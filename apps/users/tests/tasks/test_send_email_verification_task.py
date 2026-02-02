from unittest.mock import patch

from django.core import mail
from django.core.signing import TimestampSigner
from django.test import TestCase

from apps.users.domain.exceptions import (
    EmailVerificationFailedTransient,
    EmailVerificationFailedPermanent,
)
from apps.users.services.emails.verification import EmailVerificationEmailData
from apps.users.services.tokens.email_verification import EMAIL_VERIFICATION_SALT
from apps.users.tasks import send_email_verification_task
from apps.users.tests.factories.users import UserFactory


class SendEmailVerificationTaskTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="send-email-verification")
        signer = TimestampSigner(salt=EMAIL_VERIFICATION_SALT)
        cls.token = signer.sign(str(cls.user.id))
        cls.email_payload = EmailVerificationEmailData(
            username=cls.user.username, email=cls.user.email, token=cls.token
        )

    def test_success_sends_verification_email(self):
        send_email_verification_task.run(
            user_id=self.user.id,
            host="example.com",
            scheme="https",
        )
        self.assertEqual(len(mail.outbox), 1)

    @patch("apps.users.tasks.emails.verification.send_verification_email")
    def test_success_sends_verification_email_payload(self, send_email):
        send_email_verification_task.run(
            user_id=self.user.id,
            host="example.com",
            scheme="https",
        )

        send_email.assert_called_once_with(
            self.email_payload,
            host="example.com",
            scheme="https",
        )

    @patch("apps.users.tasks.emails.verification.logger")
    @patch("apps.users.tasks.emails.verification.send_verification_email")
    @patch("apps.users.tasks.emails.verification.build_email_verification_payload")
    def test_user_does_not_exist_logs_warning_and_returns(
            self, build_payload, send_email, logger
    ):
        missing_id = 999999

        send_email_verification_task.run(
            user_id=missing_id,
            host="example.com",
            scheme="https",
        )

        logger.warning.assert_called_once()
        build_payload.assert_not_called()
        send_email.assert_not_called()

    @patch("apps.users.tasks.emails.verification.send_verification_email")
    def test_email_verification_transient_failure_calls_retry(self, send_email):
        send_email.side_effect = EmailVerificationFailedTransient("mail server down")

        TaskCls = send_email_verification_task.__class__

        with patch.object(
                TaskCls, "retry", autospec=True, side_effect=RuntimeError("retry-called")
        ) as retry_mock:
            with self.assertRaises(RuntimeError):
                send_email_verification_task.run(
                    user_id=self.user.id,
                    host="example.com",
                    scheme="https",
                )

            retry_mock.assert_called_once()

    @patch("apps.users.tasks.emails.verification.logger")
    @patch("apps.users.tasks.emails.verification.send_verification_email")
    def test_permanent_failure_logs_exception_and_returns(self, send_email, logger):
        send_email.side_effect = EmailVerificationFailedPermanent("invalid email")

        send_email_verification_task.run(
            user_id=self.user.id,
            host="example.com",
            scheme="https",
        )

        logger.exception.assert_called_once()
