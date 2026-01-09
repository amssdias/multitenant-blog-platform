from django.db import models


class FontFamily(models.TextChoices):
    INTER = "inter", "Inter"
    ROBOTO = "roboto", "Roboto"
    GEORGIA = "georgia", "Georgia"
    SYSTEM = "system", "System UI"
    AIRAL = "Arial", "Arial"
    COURIR_NEW = "Courier New", "Courier New"
    VERDANA = "Verdana", "Verdana"
