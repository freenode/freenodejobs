from django.conf import settings
from django.utils.functional import SimpleLazyObject

from two_factor.utils import default_device


def settings_context(request):
    """
    Expose the settings directly in the template. This is preferable to
    site_context etc.
    """

    return {'settings': settings}


def django_otp_context(request):
    """
    Lazily expose the 2FA "default_device" directly in the template for the
    current user.
    """

    def callback():
        return default_device(request.user)

    return {'default_device': SimpleLazyObject(callback)}
