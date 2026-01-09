from django.contrib.auth import get_user_model
from django.views.generic import ListView

from apps.blogs.models import Post
from apps.site_config.models import SiteSettings

User = get_user_model()


class TenantDashboardView(ListView):
    model = Post
    template_name = "blogs/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = self.get_site_settings()
        return context

    @staticmethod
    def get_site_settings():
        site_settings = SiteSettings.objects.all()
        return site_settings.first() if site_settings.exists() else (
            SiteSettings.objects.create()
        )
