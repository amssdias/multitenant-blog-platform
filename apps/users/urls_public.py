from django.urls import path

from apps.users.views.login import CustomLoginView
from apps.users.views.register import RegisterView
from apps.users.views.verify_email import VerifyEmailView

app_name = "users"

urlpatterns = [
    path("signup", RegisterView.as_view(), name="signup"),
    path("login", CustomLoginView.as_view(), name="login"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify_email"),
]
