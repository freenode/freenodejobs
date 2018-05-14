import os
import copy
import envparse

from os.path import abspath, dirname, join

from django.utils.log import DEFAULT_LOGGING

envparse.env.read_envfile()

from .apps import *  # noqa


DEBUG = False
ADMINS = MANAGER = ()

BASE_DIR = os.environ.get(
    'DJANGO_BASE_DIR',
    dirname(dirname(dirname(dirname(abspath(__file__))))),
)

ALLOWED_HOSTS = ['*']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'freenodejobs',
    }
}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        join(BASE_DIR, 'templates'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.media',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'freenodejobs.utils.context_processors.settings_context',
        ],
        'builtins': [
            'django.contrib.humanize.templatetags.humanize',
            'django.contrib.staticfiles.templatetags.staticfiles',
            'markdown_deux.templatetags.markdown_deux_tags',
            'switch_templatetag.templatetags.switch',
            'freenodejobs.utils.templatetags.urls',
        ],
    },
}]

MIDDLEWARE = (
    'freenodejobs.utils.middleware.SetRemoteAddrFromForwardedFor',
    'django_keyerror.middleware.KeyErrorMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


WSGI_APPLICATION = 'freenodejobs.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'freenodejobs',
        'USER': 'freenodejobs',
        'PASSWORD': 'freenodejobs',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False

TIME_FORMAT = 'g:i A'
DATE_FORMAT = 'M jS Y'
DATETIME_FORMAT = '{}, {}'.format(DATE_FORMAT, TIME_FORMAT)

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')
STATICFILES_DIRS = (join(BASE_DIR, 'media'),)
STATICFILES_STORAGE = \
    'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_FINDERS = (
    'staticfiles_dotd.finders.DotDFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DOTD_RENDER_PIPELINE = (
    'staticfiles_dotd.pipeline.scss',
)

CSRF_COOKIE_SECURE = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SESSION_COOKIE_AGE = 86400 * 365 * 10
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

SITE_URL = os.environ.get('DJANGO_SITE_URL', 'http://127.0.0.1:8000')
LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'
ROOT_URLCONF = 'freenodejobs.urls'
LOGIN_REDIRECT_URL = 'dashboard:view'
LOGOUT_REDIRECT_URL = LOGIN_URL

SECRET_KEY = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# Third party #################################################

REDIS_ENABLED = True

KEYERROR_SECRET_KEY = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
KEYERROR_USER_INFO_CALLBACK = 'freenodejobs.utils.debug.get_keyerror_user_info'

DEFAULT_EMAIL = 'admin@jobs.freenode.net'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Freenode Jobs <{}>'.format(DEFAULT_EMAIL)

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = '/storage/'
MEDIA_ROOT = '/srv/freenodejobs.chris-lamb.co.uk/storage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

AWS_DEFAULT_ACL = 'private'
AWS_S3_ENCRYPTION = True
AWS_QUERYSTRING_EXPIRE = 86400 * 7  # Max of 1 week
AWS_STORAGE_BUCKET_NAME = 'freenodejobs'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.{}'.format(x)}
    for x in (
        'UserAttributeSimilarityValidator',
        'MinimumLengthValidator',
        'CommonPasswordValidator',
        'NumericPasswordValidator',
    )
]

# Log to console
LOGGING = copy.deepcopy(DEFAULT_LOGGING)

LOGGING['handlers']['console']['filters'] = []

LOGGING['formatters']['freenodejobs'] = {
    '()': 'freenodejobs.utils.log.FreenodejobsFormatter',
}
LOGGING['handlers']['freenodejobs'] = {
    'level': 'INFO',
    'class': 'watchtower.CloudWatchLogHandler',
    'log_group': 'freenodejobs',
    'formatter': 'freenodejobs',
}
LOGGING['loggers']['freenodejobs'] = {
    'level': 'INFO',
    'handlers': ['freenodejobs'],
}

GEOIP_PATH = os.path.join(BASE_DIR, 'data')

AUTH_USER_MODEL = 'account.User'

IS_TEST = False
XHR_SIMULATED_DELAY = 0.0
