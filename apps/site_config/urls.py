from django.urls import path

from apps.site_config.views.site_config import SiteSettingsEditView

app_name = "site_config"

urlpatterns = [
    path("update/<int:pk>/", SiteSettingsEditView.as_view(), name="site_settings_update"),
]
