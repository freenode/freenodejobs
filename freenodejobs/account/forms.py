from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as django_forms


class AuthenticationForm(django_forms.AuthenticationForm):
    email = forms.EmailField()
    username = forms.CharField(required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password,
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
