from django.apps import AppConfig


class SocialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social'


    def ready(self):
        import social.signals


    name = 'social'
    verbose_name = 'social'

    def ready(self):
        import social.signals
