import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'freenodejobs.settings'

from django.core.wsgi import get_wsgi_application  # noqa
from django.contrib.staticfiles.handlers import StaticFilesHandler  # noqa

application = StaticFilesHandler(get_wsgi_application())
