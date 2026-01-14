import logging
import smtplib
from celery import shared_task
from django.contrib.auth import get_user_model

from apps.users.services.emails.verification import (
    build_email_verification_payload,
    send_verification_email,
)

logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_verification_task(self, user_id: int, host: str, scheme: str) -> None:
    try:
        user = User.objects.only("id", "username", "email").get(id=user_id)
        email_payload = build_email_verification_payload(user=user)
        send_verification_email(email_payload, host=host, scheme=scheme)

    except User.DoesNotExist:
        logger.warning("Verification email not sent: user %s does not exist.", user_id)
        return

    except (
            smtplib.SMTPServerDisconnected,
            smtplib.SMTPConnectError,
            TimeoutError,
    ) as exc:
        raise self.retry(exc=exc)
