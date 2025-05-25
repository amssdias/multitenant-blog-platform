from django.db import models

from bloggies.models.timestampable import Timestampable


class SiteSettings(Timestampable):
    background_color = models.CharField(max_length=7, default="#f8f9fa")
    # hero_image = models.ImageField(upload_to="hero/")
    font_style = models.CharField(max_length=100, default="Segoe UI")
