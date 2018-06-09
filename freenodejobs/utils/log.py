import logging

from django.contrib.gis.geoip2 import GeoIP2

GEOIP = GeoIP2()
MISSING_DATA = (None,)


def error(*args, **kwargs):
    _log(logging.ERROR, *args, **kwargs)


def warning(*args, **kwargs):
    _log(logging.WARNING, *args, **kwargs)


def info(*args, **kwargs):
    _log(logging.INFO, *args, **kwargs)


def _log(level, *args, **kwargs):
    logger = logging.getLogger('freenodejobs')

    request = kwargs.pop('request', None)
    changed_data = []

    try:
        form = kwargs.pop('form')
        for x in form.changed_data:
            prev = form.initial.get(x, MISSING_DATA)
            current = form.cleaned_data[x]

            if prev != current:
                changed_data.append((x, prev, current))
    except KeyError:
        pass

    logger.log(logging.INFO, *args, **kwargs, extra={
        'request': request,
        'changed_data': changed_data,
    })


class FreenodejobsFormatter(logging.Formatter):
    def __init__(self, fmt=None, *args, **kwargs):
        fmt = '{remote_addr:>15s} ({geoip}) {levelname:.1}: {email} ' \
              '{message}'

        super().__init__(fmt, style='{', *args, **kwargs)

    def format(self, record):
        request = record.request

        if record.changed_data:
            xs = []
            for name, prev, current in record.changed_data:
                if prev is MISSING_DATA:
                    xs.append('{}: {!r}'.format(name, current))
                else:
                    xs.append('{}: {!r} -> {!r}'.format(name, prev, current))
            record.msg = '{} ({})'.format(record.msg, ', '.join(xs))

        record.email = '-'
        record.geoip = 'unknown'
        record.remote_addr = 'unknown'

        if request is not None:
            record.path_info = request.path
            record.remote_addr = request.META['REMOTE_ADDR']
            record.email = request.user.email \
                if request.user.is_authenticated else '(anonymous)'

        try:
            data = GEOIP.city(request.META['REMOTE_ADDR'])
            record.geoip = ", ".join(
                data[x] for x in ('city', 'country_name') if data[x]
            )
        except Exception:
            pass

        return super().format(record)
