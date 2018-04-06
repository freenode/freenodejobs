import redis_rate_limit

from django.conf import settings


def rate_limit(*args, **kwargs):
    if not settings.REDIS_ENABLED:
        return False

    try:
        with redis_rate_limit.RateLimit(*args, **kwargs):
            return False
    except redis_rate_limit.TooManyRequests:
        return True
