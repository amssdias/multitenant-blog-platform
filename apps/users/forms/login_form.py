from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your email"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Create a password"})

    def clean(self):
        cleaned_data = super().clean()

        user = getattr(self, "user_cache", None)
        if not user:
            return cleaned_data

        tenant = getattr(user, "tenant", None)
        if tenant is None:
            raise forms.ValidationError(
                _("Your account isn’t linked to a workspace yet. Please contact support."),
                code="no_tenant",
            )

        domain_qs = getattr(tenant, "domains", None)
        if domain_qs is None or not domain_qs.exists():
            raise forms.ValidationError(
                _("Your workspace isn’t configured yet (missing domain). Please contact support."),
                code="no_domain",
            )

        return cleaned_data
