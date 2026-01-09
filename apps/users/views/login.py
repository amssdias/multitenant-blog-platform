from django.conf import settings
from django.contrib.auth.views import LoginView

from apps.users.forms.login_form import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)

        user = getattr(self.request, "user", None)
        if user is not None:
            self.request.session["auth_tenant_id"] = user.tenant.id

        return response

    def get_success_url(self):
        port = self.request.get_port()
        user_sub_domain = self.request.user.tenant.domains.first().domain

        is_local = settings.DEBUG

        # Build the correct URL dynamically
        if is_local:
            return f"http://{user_sub_domain}:{port}"
        else:
            return f"https://{user_sub_domain}"  # In production, remove port
