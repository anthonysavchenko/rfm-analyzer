from rfm_analyser.settings.production import *

DEBUG = True

# django-debug-toolbar has an issue when debugging on Windows machine
# Error in browser console: Loading module from
# “http://127.0.0.1:8000/static/debug_toolbar/js/toolbar.js” was blocked
# because of a disallowed MIME type (“text/plain”).
# This is work around to fix it
# See https://github.com/jazzband/django-debug-toolbar/issues/1336
# And https://stackoverflow.com/questions/16303098/django-development-server-and-mime-types/16355034
if DEBUG:
    import mimetypes
    mimetypes.add_type('application/javascript', '.js', True)

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1"
]
