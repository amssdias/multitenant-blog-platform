from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.core.cache import cache


class LogoutCustomView(LogoutView):

    def post(self, request, *args, **kwargs):
        request = self.request

        auth_token = request.COOKIES.get("auth_token")

        if auth_token:
            cache.delete(f"auth_token:{auth_token}")

        response = super().post(request, *args, **kwargs)

        current_host = request.get_host().split(":")[0]

        # Clear session cookie
        response.delete_cookie(settings.COOKIE_NAME, domain=f".{current_host}")

        return response

    def get_success_url(self):
        if hasattr(self.request, "tenant"):
            schema = "http" if settings.DEBUG else "https"
            port = self.request.get_port()

            return f"{schema}://{self.request.tenant.domain_url}:{port}/"
