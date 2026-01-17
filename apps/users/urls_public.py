from django.urls import path, reverse_lazy

from apps.users.forms.password_reset import BootstrapPasswordResetForm
from apps.users.forms.password_reset_confirm import BootstrapSetPasswordForm
from apps.users.views.login import CustomLoginView
from apps.users.views.register import RegisterView
from apps.users.views.verify_email import VerifyEmailView
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("signup", RegisterView.as_view(), name="signup"),
    path("login", CustomLoginView.as_view(), name="login"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify_email"),

    # Reset password
    path("password-reset/", auth_views.PasswordResetView.as_view(
        form_class=BootstrapPasswordResetForm,
        template_name="users/registration/password_reset_form.html",
        html_email_template_name="users/registration/password_reset_email.html",
        email_template_name="users/registration/password_reset_email.html",
        subject_template_name="users/registration/password_reset_subject.txt",
        success_url=reverse_lazy("users:password_reset_done")
    ), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="users/registration/password_reset_done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        form_class=BootstrapSetPasswordForm,
        template_name="users/registration/password_reset_confirm.html",
        success_url=reverse_lazy("users:password_reset_complete")
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="users/registration/password_reset_complete.html"
    ), name="password_reset_complete"),

]
