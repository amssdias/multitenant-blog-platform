from django.conf import settings
from django.contrib.auth.views import LogoutView


class LogoutCustomView(LogoutView):

    def get_success_url(self):
        if hasattr(self.request, "tenant"):
            schema = "http" if settings.DEBUG else "https"
            port = self.request.get_port()

            domain_obj = self.request.tenant.domains.filter(is_primary=True).first() \
                         or self.request.tenant.domains.first()

            if not domain_obj:
                return "/"

            return f"{schema}://{domain_obj.domain}:{port}/"

        return "/"
