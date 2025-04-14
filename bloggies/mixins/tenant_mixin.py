from django.core.cache import cache
from django.http import Http404
from django.views.generic.base import ContextMixin


class TenantUserContextMixin(ContextMixin):
    def dispatch(self, request, *args, **kwargs):
        auth_token = request.COOKIES.get("auth_token")
        self.user_data = cache.get(f"auth_token:{auth_token}") if auth_token else None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user_data and self.request.tenant.schema_name == self.user_data.get("tenant"):
            context["user_authenticated"] = True
            context["username"] = self.user_data["username"]
        else:
            context["user_authenticated"] = False
        return context


class TenantLoginRequiredMixin(TenantUserContextMixin):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not self.user_data or self.user_data.get("tenant") != request.tenant.schema_name:
            raise Http404("Page not available")
        return response
