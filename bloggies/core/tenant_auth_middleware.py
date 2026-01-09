from django.contrib.auth.models import AnonymousUser


class TenantAuthMiddleware:
    """
    Keeps global login session, but marks the user as "tenant-authenticated"
    only when the current tenant matches request.session['active_tenant_id'].

    Optionally masks request.user to AnonymousUser for protected areas
    (e.g. tenant admin/dashboard) WITHOUT logging out.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = getattr(request, "tenant", None)

        request.tenant_is_authenticated = False
        request.tenant_auth_mismatch = False

        if tenant is not None and request.user.is_authenticated:
            active_tenant_id = request.session.get("auth_tenant_id")
            request.tenant_is_authenticated = (str(active_tenant_id) == str(tenant.id))
            request.tenant_auth_mismatch = not request.tenant_is_authenticated

            # Mask user only for sensitive tenant paths
            # so Django permissions/guards see them as anonymous there,
            # but they remain logged-in globally.
            if request.tenant_auth_mismatch:
                request._cached_user = AnonymousUser()

        return self.get_response(request)
