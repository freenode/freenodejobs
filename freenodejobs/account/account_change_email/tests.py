from django.contrib.auth import get_user_model

from freenodejobs.utils.test import TestCase
from freenodejobs.utils.tokens import get_token

UserModel = get_user_model()


class ChangeEmailTests(TestCase):
    NEW_EMAIL = 'new@example.com'

    def test_GET(self):
        self.assertGET(200, 'account:change-email:view')

    def test_POST(self):
        with self.assertSendsMail():
            self.assertPOST(
                {'email': self.NEW_EMAIL},
                'account:change-email:view',
            )

        self.user.refresh_from_db()

    def test_POST_same(self):
        with self.assertSendsMail(0):
            response = self.assertPOST({
                'email': self.user.email,
            }, 'account:change-email:view', status_code=200)

        self.assertFormError(response, 'form', 'email', [
            "Please enter a different email address.",
        ])

    def test_validate(self):
        old_email_validated = self.user.email_validated

        self.assertGET(
            302,
            'account:change-email:validate',
            get_token(self.user, self.NEW_EMAIL),
            login=None,
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, self.NEW_EMAIL)
        self.assertNotEqual(self.user.email_validated, old_email_validated)

    def test_validate_invalid_token(self):
        old_email_validated = self.user.email_validated

        self.assertGET(302, 'account:change-email:validate', 'invalid-token')

        self.user.refresh_from_db()
        self.assertEqual(self.user.email_validated, old_email_validated)
        self.assertNotEqual(self.user.email, self.NEW_EMAIL)
