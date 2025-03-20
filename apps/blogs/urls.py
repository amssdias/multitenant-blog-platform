from django.urls import path

from apps.blogs.views.create_post import PostCreateView
from apps.blogs.views.index import TenantDashboardView
from apps.blogs.views.logout import LogoutCustomView

app_name = "blogs"

urlpatterns = [
    path("logout", LogoutCustomView.as_view(), name="logout"),
    path("create-post", PostCreateView.as_view(), name="create-post"),
    path("", TenantDashboardView.as_view(), name="tenant_index"),
]
