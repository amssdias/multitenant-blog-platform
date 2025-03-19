from django.contrib.auth.views import LoginView

from apps.users.forms.login_form import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomLoginForm

    def form_valid(self, form):
        return super().form_valid(form)
