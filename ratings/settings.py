from django.conf import settings

# Settings can be overridden in the main settings file.

# Virtual path to the root of the static files needed by this app.
MEDIA_URL = getattr(settings, 'RABIDRATINGS_MEDIA_URL', settings.MEDIA_URL)
