from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.users.domain.exceptions import (
    EmailVerificationUserNotFound,
    EmailAlreadyVerified,
    EmailVerificationFailedTransient,
    EmailVerificationFailedPermanent,
)
from apps.users.services.tokens.email_verification import (
    create_email_verification_token,
)
from integrations.email.exceptions import EmailTransientError, EmailPermanentError
from integrations.email.mailer import send_templated_email

User = get_user_model()


@dataclass(frozen=True)
class EmailVerificationEmailData:
    username: str
    email: str
    token: str


def build_email_verification_payload(*, user):
    if not user.email:
        raise ValueError(_("User has no email."))

    token = create_email_verification_token(user.id)
    return EmailVerificationEmailData(
        username=user.username, email=user.email, token=token
    )


def send_verification_email(user_email_data: EmailVerificationEmailData, host, scheme):
    verify_url = get_verification_url(user_email_data.token, scheme, host)

    subject = _("Confirm your email")

    context = {
        "site_name": getattr(settings, "SITE_NAME", "Bloggies"),
        "protocol": scheme,
        "domain": host,
        "token": user_email_data.token,
        "username": user_email_data.username,
        "verify_url": verify_url,
    }

    try:

        send_templated_email(
            subject=subject,
            to=[user_email_data.email],
            template_html="users/registration/verification_email.html",
            template_txt="users/registration/verification_email.txt",
            context=context,
        )
    except EmailTransientError as exc:
        raise EmailVerificationFailedTransient() from exc
    except EmailPermanentError as exc:
        raise EmailVerificationFailedPermanent() from exc


def get_verification_url(token, scheme, host):
    verify_path = reverse(
        "users:verify_email",
        kwargs={"token": token},
        urlconf=settings.PUBLIC_SCHEMA_URLCONF,
    )
    return f"{scheme}://{host}{verify_path}"


def activate_user_email(user_id: int) -> None:
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise EmailVerificationUserNotFound()

    if user.is_active:
        raise EmailAlreadyVerified()

    user.is_active = True
    user.save(update_fields=["is_active"])
