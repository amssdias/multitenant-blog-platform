from django.conf import settings
from django.db import models
from django_tenants.models import TenantMixin


class Tenant(TenantMixin):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tenant"
    )
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # Default schema & auto-creation
    auto_create_schema = True  # This will automatically create the schema
