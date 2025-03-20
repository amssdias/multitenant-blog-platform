from django.urls import path

from apps.blogs.views.create_post import PostCreateView
from apps.blogs.views.index import TenantDashboardView
from apps.blogs.views.logout import LogoutCustomView
from apps.blogs.views.post_detail import PostDetailView

app_name = "blogs"

urlpatterns = [
    path("logout/", LogoutCustomView.as_view(), name="logout"),
    path("create-post/", PostCreateView.as_view(), name="create-post"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("", TenantDashboardView.as_view(), name="tenant_index"),
]
