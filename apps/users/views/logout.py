from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.core.cache import cache


class LogoutCustomView(LogoutView):

    def get_success_url(self):
        if hasattr(self.request, "tenant"):
            schema = "http" if settings.DEBUG else "https"
            port = self.request.get_port()

            return f"{schema}://{self.request.tenant.domain_url}:{port}/"
