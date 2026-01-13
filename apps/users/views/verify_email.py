from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View

from apps.users.exceptions import EmailVerificationTokenExpired, EmailVerificationTokenInvalid, \
    EmailVerificationUserNotFound, EmailAlreadyVerified
from apps.users.services.emails.verification import activate_user_email
from apps.users.services.tokens.email_verification import verify_email_token, get_user_id_from_verification_token

User = get_user_model()


class VerifyEmailView(View):
    """
    Verifies a user's email using a signed + timestamped token.
    """

    success_url = reverse_lazy("users:login")

    def get(self, request, token: str, *args, **kwargs):
        max_age = getattr(settings, "EMAIL_VERIFICATION_TOKEN_MAX_AGE_SECONDS", 60 * 60 * 24)

        try:
            user_id = get_user_id_from_verification_token(token, max_age)
            activate_user_email(user_id)
        except EmailVerificationTokenExpired:
            messages.error(request, _("This verification link has expired. Please request a new one."))
        except EmailVerificationTokenInvalid:
            messages.error(request, _("This verification link is invalid. Please request a new one."))
        except EmailVerificationUserNotFound:
            messages.error(request, _("We couldn’t find an account for this verification link."))
        except EmailAlreadyVerified:
            messages.info(request, _("Your email is already activated"))
        else:
            messages.success(request, _("Your email has been verified successfully. You can now log in."))

        return redirect(self.success_url)
