from django.apps import AppConfig


class NaukriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'naukri'


class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import signals
