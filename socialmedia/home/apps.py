# Import AppConfig from django.apps to configure the app
from django.apps import AppConfig

# HomeConfig class to configure the 'home' application
class HomeConfig(AppConfig):
    # The default type for auto-incrementing primary keys. BigAutoField uses a 64-bit integer.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name of the application ('home' in this case)
    name = 'home'

    # The ready method is called when the app is fully loaded
    def ready(self):
        # Import the signals module within the 'home' app
        import home.signals
