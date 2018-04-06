from django.conf import settings

from freenodejobs.utils.test import TestCase


class LoginTest(TestCase):
    def test_logged_in(self):
        response = self.assertGET(302, 'account:login')
        self.assertRedirectsToUrl(response, settings.LOGIN_REDIRECT_URL)

    def test_GET(self):
        self.assertGET(200, 'account:login', login=None)

    def test_POST(self):
        self.assertPOST({
            'auth-email': self.user.email,
            'auth-password': 'password',
            'login_view-current_step': 1,
        }, 'account:login', login=None)

    def test_POST_invalid(self):
        response = self.assertPOST({
            'auth-email': self.user.email,
            'auth-password': 'invalid',
            'login_view-current_step': 1,
        }, 'account:login', login=None, status_code=200)

        self.assertFormError(response, 'form', None, [
            "Please enter a correct email and password. Note that both fields "
            "may be case-sensitive."
        ])


class LogoutTest(TestCase):
    def test_GET(self):
        response = self.assertGET(302, 'account:logout')
        self.assertRedirectsToUrl(response, settings.LOGIN_URL)


class PasswordChangeTests(TestCase):
    def test_GET(self):
        self.assertGET(200, 'account:password-change')

    def test_POST(self):
        self.assertPOST({
            'old_password': 'password',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        }, 'account:password-change')

    def test_POST_not_match(self):
        response = self.assertPOST({
            'old_password': 'password',
            'new_password1': 'these-passwords',
            'new_password2': 'do-not-match',
        }, 'account:password-change', status_code=200)

        self.assertFormError(response, 'form', 'new_password2', [
            "The two password fields didn't match.",
        ])

    def test_POST_missing(self):
        response = self.assertPOST(
            {},
            'account:password-change',
            status_code=200,
        )

        self.assertFormError(response, 'form', 'old_password', [
            "This field is required."
        ])
