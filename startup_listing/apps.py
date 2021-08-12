from django.apps import AppConfig


class StartupListingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'startup_listing'
    def ready(self):
        import startup_listing.signals
