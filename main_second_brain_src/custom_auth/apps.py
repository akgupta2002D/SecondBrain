from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    """
    Configuration class for the custom_auth application.

    Attributes:
        default_auto_field (str): The default auto field type for the application.
        name (str): The name of the application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "custom_auth"

    def ready(self):
        """
        Import the signals module to connect signal handlers.

        This method is called when the application is ready to use. It ensures
        that the signal handlers defined in custom_auth.signals are connected.
        """
        import custom_auth.signals
