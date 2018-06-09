from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature

UserModel = get_user_model()


def get_token(user, *args):
    keys = [user.email]
    keys.extend(args)

    return TimestampSigner(salt=user.password).sign(':'.join(keys))


def get_user_from_token(token):
    try:
        user = UserModel.objects.get(email=token.split(':', 1)[0])
    except UserModel.DoesNotExist:
        return None

    try:
        TimestampSigner(salt=user.password).unsign(
            token, max_age=60 * 60 * 24,
        )
    except BadSignature:
        return None

    return user


def get_value_from_token(token, idx):
    parts = token.split(':')

    # Ensure we have enough values
    if len(parts) < 4 + idx:
        return None

    return parts[idx + 1]
