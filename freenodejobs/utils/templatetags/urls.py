from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def ensure_absolute_url(val):
    if val.startswith('http'):
        return val
    return mark_safe('{}{}'.format(settings.SITE_URL, val))


@register.simple_tag(takes_context=True)
def querystring(context, key, value, **kwargs):
    xs = context['request'].GET.copy()
    xs[key] = value

    return xs.urlencode()
