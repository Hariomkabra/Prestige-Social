from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        # Create default profile images on startup
        from users.signals import ensure_default_images
        ensure_default_images()
