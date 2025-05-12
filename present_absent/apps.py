from django.apps import AppConfig


class PresentAbsentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'present_absent'

    def ready(self):
        import present_absent.signals