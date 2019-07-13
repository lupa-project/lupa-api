from lupa.settings.production import *

# Settings for Development

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Django Debug Toolbar Settings
INTERNAL_IPS = ('127.0.0.1', 'localhost',)
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)
