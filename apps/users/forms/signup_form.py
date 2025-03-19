from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"}),
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Create a password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm your password"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user
