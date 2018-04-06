import functools

from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login


def logout_required(fn):
    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return fn(request, *args, **kwargs)
    return wrapper


def staff_required(fn):
    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return fn(request, *args, **kwargs)
            return HttpResponseForbidden(
                "You are logged-in, but you are not a staff member."
            )
        return redirect_to_login(request.path)
    return wrapper
