from django.contrib import admin

from apps.tenants.models import Tenant, Domain


class TenantAdminSite(admin.AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(Tenant)
        self.register(Domain)


tenant_admin_site = TenantAdminSite(name="tenant_admin_site")
