from django.urls import path

from apps.blogs.views.index import TenantDashboardView
from apps.blogs.views.post import PostCreateView, PostEditView, PostDetailView, PostDeleteView

app_name = "blogs"

urlpatterns = [
    path("post/", PostCreateView.as_view(), name="create-post"),
    path("post/<int:pk>/", PostEditView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("", TenantDashboardView.as_view(), name="tenant_index"),
]
