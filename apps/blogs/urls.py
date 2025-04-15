from django.urls import path

from apps.blogs.views.index import TenantDashboardView
from apps.blogs.views.logout import LogoutCustomView
from apps.blogs.views.post import PostCreateView, PostEditView, PostDetailView

app_name = "blogs"

urlpatterns = [
    path("logout/", LogoutCustomView.as_view(), name="logout"),
    path("create-post/", PostCreateView.as_view(), name="create-post"),
    path("edit-post/<int:pk>/", PostEditView.as_view(), name="post_edit"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("", TenantDashboardView.as_view(), name="tenant_index"),
]
