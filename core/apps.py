from django.apps import AppConfig
from django.core.management import call_command


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        try:
            call_command('clearsessions')
        except Exception:
            # Prevent crash during migrations or startup
            pass