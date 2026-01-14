from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from apps.users.tasks.emails.verification import send_email_verification_task

User = get_user_model()


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Create a password"}
        )

    def clean(self):

        user = User.objects.get(username=self.cleaned_data["username"])
        if not user.is_active:
            send_email_verification_task.delay(
                user.id, self.request.get_host(), self.request.scheme
            )
            raise forms.ValidationError(
                _(
                    "Your account is not yet activated. Please check your email and follow the verification link."
                ),
                code="not_activated",
            )

        tenant = getattr(user, "tenant", None)
        if tenant is None:
            raise forms.ValidationError(
                _(
                    "Your account isn’t linked to a workspace yet. Please contact support."
                ),
                code="no_tenant",
            )

        domain_qs = getattr(tenant, "domains", None)
        if domain_qs is None or not domain_qs.exists():
            raise forms.ValidationError(
                _(
                    "Your workspace isn’t configured yet (missing domain). Please contact support."
                ),
                code="no_domain",
            )

        cleaned_data = super().clean()
        return cleaned_data
