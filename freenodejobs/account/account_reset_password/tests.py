from django.conf import settings

from freenodejobs.utils.test import TestCase

from .utils import get_token


class ViewTests(TestCase):
    def test_logged_in(self):
        response = self.assertGET(302, 'account:reset-password:view')
        self.assertRedirectsToUrl(response, settings.LOGIN_REDIRECT_URL)

    def test_GET(self):
        self.assertGET(200, 'account:reset-password:view', login=False)

    def test_POST(self):
        with self.assertSendsMail(1):
            self.assertPOST({
                'email': self.user.email,
            }, 'account:reset-password:view', login=False)

    def test_POST_not_match(self):
        with self.assertSendsMail(0):
            self.assertPOST({
                'email': 'invalid@example.com',
            }, 'account:reset-password:view', login=False)

    def test_POST_missing(self):
        response = self.assertPOST(
            {}, 'account:reset-password:view', login=False, status_code=200,
        )

        self.assertFormError(response, 'form', 'email', [
            "This field is required."
        ])


class ResetTests(TestCase):
    def test_logged_in(self):
        response = self.assertGET(
            302,
            'account:reset-password:reset',
            get_token(self.user),
        )

        self.assertRedirectsToUrl(response, settings.LOGIN_REDIRECT_URL)

    def test_GET_invalid_email(self):
        token = 'invalid-prefix{}x'.format(get_token(self.user))

        response = self.assertGET(
            302, 'account:reset-password:reset', token, login=False,
        )

        self.assertRedirectsToUrl(response, settings.LOGIN_REDIRECT_URL)

    def test_GET_invalid_token(self):
        token = '{}invalid-suffix'.format(get_token(self.user))

        response = self.assertGET(
            302, 'account:reset-password:reset', token, login=False,
        )

        self.assertRedirectsToUrl(response, settings.LOGIN_REDIRECT_URL)

    def test_GET(self):
        self.assertGET(
            200,
            'account:reset-password:reset',
            get_token(self.user),
            login=False,
        )

    def test_POST(self):
        old_password = self.user.password

        self.assertPOST(
            {
                'new_password1': 'foobarbaz',
                'new_password2': 'foobarbaz',
            },
            'account:reset-password:reset',
            get_token(self.user),
            login=False,
        )

        self.user.refresh_from_db()
        self.assertNotEqual(old_password, self.user.password)

    def test_POST_missing(self):
        response = self.assertPOST(
            {},
            'account:reset-password:reset',
            get_token(self.user),
            login=False,
            status_code=200,
        )

        self.assertFormError(response, 'form', 'new_password1', [
            "This field is required."
        ])

    def test_POST_not_match(self):
        response = self.assertPOST(
            {
                'new_password1': 'foobarbaz1',
                'new_password2': 'foobarbaz2',
            },
            'account:reset-password:reset',
            get_token(self.user),
            login=False,
            status_code=200,
        )

        self.assertFormError(response, 'form', 'new_password2', [
            "The two password fields didn't match.",
        ])
