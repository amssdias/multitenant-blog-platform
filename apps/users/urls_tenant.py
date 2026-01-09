from django.urls import path

from apps.users.views.logout import LogoutCustomView

app_name = "users"

urlpatterns = [
    path("logout/", LogoutCustomView.as_view(), name="logout"),
]
