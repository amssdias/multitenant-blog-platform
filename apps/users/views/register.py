from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.utils.translation import gettext as _
from apps.users.forms.signup_form import CustomSignupForm
from apps.users.tasks.emails.verification import send_email_verification_task

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
        response = super().form_valid(form)
        user = self.object

        host = self.request.get_host()
        scheme = self.request.scheme

        send_email_verification_task.delay(user.id, host, scheme)

        messages.info(
            self.request,
            _(
                "Account created! Please check your email and click the verification link to activate your account."
            ),
        )

        return response
