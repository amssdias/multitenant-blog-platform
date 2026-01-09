from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.site_config.choices.font_family import FontFamily
from bloggies.models.timestampable import Timestampable

HEX_COLOR_VALIDATOR = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Color must be a valid hex value like #RRGGBB.",
)


class SiteSettings(Timestampable):
    # Brand
    blog_name = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=200, blank=True)

    # Theme
    background_color = models.CharField(
        max_length=7, default="#f8f9fa", validators=[HEX_COLOR_VALIDATOR]
    )
    card_background_color = models.CharField(
        max_length=7, default="#ffffff", validators=[HEX_COLOR_VALIDATOR]
    )
    card_border_color = models.CharField(
        max_length=7, default="#e9ecef", validators=[HEX_COLOR_VALIDATOR]
    )

    # Typography
    heading_font_family = models.CharField(max_length=100, choices=FontFamily.choices, default=FontFamily.ROBOTO)
    body_font_family = models.CharField(max_length=100, choices=FontFamily.choices, default=FontFamily.ROBOTO)

    # Hero
    hero_image_url = models.URLField(blank=True)
    hero_overlay_opacity = models.PositiveSmallIntegerField(
        default=40,
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        help_text="Overlay opacity percentage from 0 to 60 for better text readability.",
    )
    hero_text_color = models.CharField(
        max_length=7, default="#ffffff", validators=[HEX_COLOR_VALIDATOR]
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self) -> str:
        return f"SiteSettings({self.blog_name})"
