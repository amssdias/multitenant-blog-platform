import uuid

from django.conf import settings
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.http import JsonResponse

from apps.users.forms.login_form import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session.save()

        response = JsonResponse({"redirect_url": self.build_subdomain_url()})

        current_host = self.request.get_host().split(":")[0]

        # Generate and store authentication token
        auth_token = str(uuid.uuid4())
        cache.set(f"auth_token:{auth_token}", {
            "user_id": self.request.user.id,
            "username": self.request.user.username,
            "tenant": self.request.user.tenant.schema_name,
        }, timeout=3600)

        # Set the cookie BEFORE redirecting (browser will store it)
        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=auth_token,
            domain=f".{current_host}",  # ✅ Available on all subdomains
            httponly=True,  # ✅ Prevents JavaScript access (security)
            secure=False,  # ✅ Must be True in production (HTTPS)
            # samesite="None"  # ✅ Allow cross-origin authentication
        )

        return response  # ✅ JavaScript will handle the redirect

    def build_subdomain_url(self):
        port = self.request.get_port()
        user_sub_domain = self.request.user.tenant.domains.first().domain

        # Get the base domain
        current_host = self.request.get_host().split(":")[0]
        is_local = "localhost" in current_host

        # Build the correct URL dynamically
        if is_local:
            return f"http://{user_sub_domain}:{port}"  # Ensure it's correctly formatted
        else:
            return f"https://{user_sub_domain}"  # In production, remove port
