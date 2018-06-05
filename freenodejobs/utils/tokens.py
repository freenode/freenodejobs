from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature

UserModel = get_user_model()


def get_token(user):
    return TimestampSigner(salt=user.password).sign(user.email)


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
