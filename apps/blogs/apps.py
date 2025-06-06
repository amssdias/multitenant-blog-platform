from django.apps import AppConfig


class BlogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.blogs"

    def ready(self):
        from apps.blogs import signals

        return super().ready()
