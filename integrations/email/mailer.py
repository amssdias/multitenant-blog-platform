import smtplib
import socket

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import render_to_string

from integrations.email.exceptions import EmailTransientError, EmailPermanentError


def send_templated_email(
        subject,
        to: list[str],
        context: dict,
        template_html,
        template_txt,
        from_email=None,
        reply_to=None,
) -> None:
    from_email = from_email or getattr(settings, "DEFAULT_FROM_EMAIL", None)
    text_body, html_body = _render_email_bodies(template_txt, template_html, context)

    try:
        msg = EmailMultiAlternatives(
            subject=str(subject),
            body=text_body,
            from_email=from_email,
            to=to,
            reply_to=reply_to,
        )

        if html_body:
            msg.attach_alternative(html_body, "text/html")

        msg.send(fail_silently=False)

    except Exception as exc:
        _raise_email_send_error(exc)


def _render_email_bodies(template_txt, template_html, context):
    try:
        text_body = render_to_string(template_txt, context) if template_txt else ""
        html_body = render_to_string(template_html, context) if template_html else None
        return text_body, html_body
    except (TemplateDoesNotExist, TemplateSyntaxError, KeyError, ValueError) as exc:
        raise EmailPermanentError("Failed to render email template.") from exc


def _raise_email_send_error(exc: Exception) -> None:
    # SMTP responses with codes (4xx transient, 5xx permanent)
    if isinstance(exc, smtplib.SMTPResponseException):
        code = getattr(exc, "smtp_code", None)
        if isinstance(code, int) and 400 <= code < 500:
            raise EmailTransientError(f"Temporary SMTP error ({code}).") from exc
        raise EmailPermanentError(f"Permanent SMTP error ({code}).") from exc

    # Transient network/connectivity problems
    if isinstance(
            exc,
            (
                    smtplib.SMTPServerDisconnected,
                    smtplib.SMTPConnectError,
                    TimeoutError,
                    socket.timeout,
                    socket.gaierror,
                    ConnectionError,
                    OSError,
            ),
    ):
        raise EmailTransientError("Email send failed due to a transient network/SMTP issue.") from exc

    if isinstance(
            exc,
            (
                    smtplib.SMTPAuthenticationError,
                    smtplib.SMTPRecipientsRefused,
                    smtplib.SMTPSenderRefused,
            ),
    ):
        raise EmailPermanentError("Email send failed due to auth/recipient/sender error.") from exc

    raise EmailPermanentError("Unexpected error while sending email.") from exc
