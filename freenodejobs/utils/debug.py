from .templatetags.urls import ensure_absolute_url


def get_keyerror_user_info(request):
    x = {}

    if hasattr(request.user, 'profile'):
        if request.user.profile.image.exists():
            x['avatar_url'] = ensure_absolute_url(
                request.user.profile.image.resized.url,
            )

    return x
