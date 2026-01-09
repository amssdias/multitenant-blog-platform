from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden


class TenantLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not getattr(request, "tenant_is_authenticated", False):
            return HttpResponseForbidden("Not allowed for this tenant.")

        return super().dispatch(request, *args, **kwargs)
