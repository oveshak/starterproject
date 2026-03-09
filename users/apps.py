# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'  # Make sure this matches your app name

    def ready(self):
        import users.signals  # Ensure it imports signals from your 'users' app

