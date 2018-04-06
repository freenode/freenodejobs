from email_from_template import send_mail

from django import forms
from django.contrib.auth import get_user_model, forms as auth_forms

from .utils import get_token

UserModel = get_user_model()


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        try:
            self.cleaned_data['user'] = UserModel.objects.get(
                email=self.cleaned_data.get('email'),
            )
        except UserModel.DoesNotExist:
            self.cleaned_data['user'] = None

        return self.cleaned_data

    def save(self):
        user = self.cleaned_data['user']

        if user is None:
            return

        send_mail((user.email,), 'account/reset_password/reset.email', {
            'token': get_token(user),
        })


class SetPasswordForm(auth_forms.SetPasswordForm):
    pass
