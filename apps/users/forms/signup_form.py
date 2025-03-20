from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from apps.tenants.models import Tenant, Domain

User = get_user_model()

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address."
    )
    subdomain = forms.CharField(
        max_length=50,
        required=True,
        help_text="Choose a unique subdomain for your blog."
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "subdomain"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"}),
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Create a password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm your password"})
        self.fields["subdomain"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your subdomain"})

    def clean_subdomain(self):
        subdomain = self.cleaned_data["subdomain"].lower()
        if Tenant.objects.filter(schema_name=subdomain).exists():
            raise forms.ValidationError("This subdomain is already taken. Please choose another.")
        return subdomain

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            tenant = self.save_tenant(user=user)
            self.save_domain(tenant)

        return user

    def save_tenant(self, user: User):
        subdomain = self.cleaned_data["subdomain"]
        tenant = Tenant(schema_name=subdomain, name=f"{user.username}'s Blog", owner=user)
        tenant.save()
        return tenant

    def save_domain(self, tenant):
        subdomain = self.cleaned_data["subdomain"]
        domain = Domain(domain=f"{subdomain}.{self.request.get_host().split(':')[0]}", tenant=tenant)
        domain.save()
