from django.utils.deprecation import MiddlewareMixin


class SetRemoteAddrFromForwardedFor(MiddlewareMixin):
    def process_request(self, request):
        request.META['REMOTE_ADDR'] = request.META.get(
            'HTTP_X_FORWARDED_FOR',
            request.META['REMOTE_ADDR'],
        )
