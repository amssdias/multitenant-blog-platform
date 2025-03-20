from django.urls import path

from apps.blogs.views.index import TenantDashboardView

app_name = "blogs"

urlpatterns = [
    # path("logout", LogoutCustomView.as_view(), name="logout"),
    path("", TenantDashboardView.as_view(), name="tenant_index"),
]
