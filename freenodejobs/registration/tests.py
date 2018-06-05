from django.conf import settings
from django.contrib.auth import get_user_model

from freenodejobs.utils.test import TestCase
from freenodejobs.utils.tokens import get_token

UserModel = get_user_model()


class RegistrationTests(TestCase):
    def assertRegister(self):
        email = 'new@email.com'

        self.assertPOST({
            'email': 'new@email.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }, 'registration:view', login=None)

        return UserModel.objects.get(email=email)

    def test_logged_in(self):
        response = self.assertGET(302, 'registration:view')
        self.assertRedirectsToUrl(response, settings.LOGIN_REDIRECT_URL)

    def test_logged_out(self):
        self.assertGET(200, 'registration:view', login=None)

    def test_POST(self):
        user = self.assertRegister()

        self.assertFalse(user.email_validated)

    def test_POST_duplicate_email(self):
        response = self.assertPOST({
            'email': self.user.email,
            'password1': 'newpassword',
            'password2': 'newpassword',
        }, 'registration:view', status_code=200, login=None)

        self.assertFormError(response, 'form', 'email', [
            "User with this Email already exists.",
        ])

    def test_validate(self):
        user = self.assertRegister()

        self.assertGET(
            200,
            'registration:validate',
            get_token(user),
            login=None,
            follow=True,
        )

        user.refresh_from_db()
        self.assertTrue(user.email_validated)

    def test_validate_invalid_token(self):
        user = self.assertRegister()

        self.assertGET(
            200,
            'registration:validate',
            'invalid-token',
            login=None,
            follow=True,
        )

        user.refresh_from_db()
        self.assertFalse(user.email_validated)
