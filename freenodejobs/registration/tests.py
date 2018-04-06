from django.conf import settings

from freenodejobs.utils.test import TestCase


class RegistrationTests(TestCase):
    def test_logged_in(self):
        response = self.assertGET(302, 'registration:view')
        self.assertRedirectsToUrl(response, settings.LOGIN_REDIRECT_URL)

    def test_logged_out(self):
        self.assertGET(200, 'registration:view', login=None)

    def test_POST(self):
        self.assertPOST({
            'email': 'new@email.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }, 'registration:view', login=None)

    def test_POST_duplicate_email(self):
        response = self.assertPOST({
            'email': self.user.email,
            'password1': 'newpassword',
            'password2': 'newpassword',
        }, 'registration:view', status_code=200, login=None)

        self.assertFormError(response, 'form', 'email', [
            "User with this Email already exists.",
        ])
