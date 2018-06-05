from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from email_from_template import send_mail

from freenodejobs.utils.tokens import get_token

UserModel = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = (
            'email',
        )

    def save(self):
        user = super().save()

        send_mail((user.email,), 'registration/validate.email', {
            'token': get_token(user),
        }, fail_silently=True)

        return user
