from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.site_config.forms.site_settings_form import SiteSettingsForm
from apps.site_config.models import SiteSettings
from bloggies.mixins.tenant_mixin import TenantLoginRequiredMixin


class SiteSettingsEditView(UpdateView, TenantLoginRequiredMixin):
    template_name = "site_config/site_settings_form.html"
    form_class = SiteSettingsForm
    model = SiteSettings
    success_url = reverse_lazy("blogs:tenant_index")

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)
