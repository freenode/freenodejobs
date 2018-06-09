from django import forms

from django.contrib.auth import get_user_model

from email_from_template import send_mail

from freenodejobs.utils.tokens import get_token

UserModel = get_user_model()


class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = (
            'email',
        )

    def clean_email(self):
        val = self.cleaned_data['email']

        if val == self.initial['email']:
            raise forms.ValidationError(
                "Please enter a different email address."
            )

        return val

    def save(self):
        # Ensure that we generate tokens using their existing email
        self.instance.refresh_from_db()

        new_email = self.cleaned_data['email']

        send_mail((new_email,), 'account/change_email/validate.email', {
            'token': get_token(self.instance, new_email),
        }, fail_silently=True)

        return new_email
