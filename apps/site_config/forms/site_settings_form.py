from django import forms

from apps.site_config.models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "blog_name",
            "subtitle",
            "background_color",
            "card_background_color",
            "card_border_color",
            "heading_font_family",
            "hero_image_url",
        )

        widgets = {
            "blog_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "subtitle": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "background_color": forms.TextInput(
                attrs={
                    "class": "form-control form-control-color",
                    "type": "color",
                    "value": "#f5f5f5",
                }
            ),
            "card_background_color": forms.TextInput(
                attrs={
                    "class": "form-control form-control-color",
                    "type": "color",
                    "value": "#f5f5f5",
                }
            ),
            "card_border_color": forms.TextInput(
                attrs={
                    "class": "form-control form-control-color",
                    "type": "color",
                    "value": "#f5f5f5",
                }
            ),
            "heading_font_family": forms.Select(attrs={"class": "form-select"}),
            "hero_image_url": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
