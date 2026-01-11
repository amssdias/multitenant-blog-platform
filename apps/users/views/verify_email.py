from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View

from apps.users.services.tokens.email_verification import verify_email_token

User = get_user_model()


class VerifyEmailView(View):
    """
    Verifies a user's email using a signed + timestamped token.
    """

    success_url = reverse_lazy("users:login")

    def get(self, request, token: str, *args, **kwargs):
        max_age = getattr(
            settings, "EMAIL_VERIFICATION_TOKEN_MAX_AGE_SECONDS", 60 * 60 * 24
        )

        try:
            user_id = verify_email_token(token, max_age)
        except SignatureExpired:
            messages.error(
                request,
                _("This verification link has expired. Please request a new one."),
            )
            return redirect(self.success_url)
        except (BadSignature, ValueError):
            messages.error(
                request,
                _("This verification link is invalid. Please request a new one."),
            )
            return redirect(self.success_url)

        user = User.objects.filter(id=user_id).first()
        if not user:
            messages.error(
                request, _("We couldn’t find an account for this verification link.")
            )
            return redirect(self.success_url)

        if user.is_active:
            messages.info(request, _("Your email is already activated"))
            return redirect(self.success_url)

        user.is_active = True
        user.save(update_fields=["is_active"])

        messages.success(
            request, _("Your email has been verified successfully. You can now log in.")
        )
        return redirect(self.success_url)
