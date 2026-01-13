from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.users.exceptions import EmailVerificationUserNotFound, EmailAlreadyVerified
from apps.users.services.tokens.email_verification import (
    create_email_verification_token,
)

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
    email_verification_url = get_verification_url(user_email_data.token, scheme, host)

    subject = _("Confirm your email")
    message = _(
        "Hi {username},\n\n"
        "Thanks for signing up. Please confirm your email by clicking the link below:\n"
        "{verify_url}\n\n"
        "If you didn’t create this account, you can ignore this email.\n"
    ).format(username=user_email_data.username, verify_url=email_verification_url)

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    recipient_list = [user_email_data.email]

    send_mail(
        subject=str(subject),
        message=str(message),
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def get_verification_url(token, scheme, host):
    verify_path = reverse("users:verify_email", kwargs={"token": token})
    return f"{scheme}://{host}{verify_path}"


def activate_user_email(user_id: int) -> None:
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise EmailVerificationUserNotFound()

    if user.is_active:
        raise EmailAlreadyVerified()

    user.is_active = True
    user.save(update_fields=["is_active"])
