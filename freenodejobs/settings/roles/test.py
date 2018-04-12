import os
import copy
import tempfile

from django.utils.log import DEFAULT_LOGGING

from .local import *

IS_TEST = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

LOGGING = copy.deepcopy(DEFAULT_LOGGING)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'freenodejobs-media-root')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

XHR_SIMULATED_DELAY = 0.0
