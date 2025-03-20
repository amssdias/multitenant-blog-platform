from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.views.generic import ListView

from apps.blogs.forms.post_form import PostForm
from apps.blogs.models import Post

User = get_user_model()


class TenantDashboardView(ListView):
    model = Post
    template_name = "blogs/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        """Check for auth token and provide user data in template context."""
        context = super().get_context_data(**kwargs)
        request = self.request

        auth_token = request.COOKIES.get("auth_token")

        if auth_token:
            user_data = cache.get(f"auth_token:{auth_token}")

            if user_data and user_data["tenant"] == request.tenant.schema_name:
                context["user_authenticated"] = True
                context["username"] = user_data["username"]
                context["form"] = PostForm()
            else:
                context["user_authenticated"] = False

        return context
