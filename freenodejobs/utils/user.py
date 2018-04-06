from django.conf import settings
from django.contrib.auth import login as django_login


def login(request, user):
    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    django_login(request, user)
