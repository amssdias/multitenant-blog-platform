from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.users.forms.signup_form import CustomSignupForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = CustomSignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)
