from django.urls import reverse
from freenodejobs.utils.test import TestCase


class SmokeTest(TestCase):
    def test_view(self):
        self.assertGET(200, 'admin:users:view', login=self.admin)

    def test_view_admins(self):
        self.assertGET(
            200,
            '{}?only_admins=on'.format(reverse('admin:users:view')),
            login=self.admin,
        )

    def test_edit_GET(self):
        self.assertGET(200, 'admin:users:edit', self.user.pk, login=self.admin)

    def test_edit_POST(self):
        new_email = 'updated@example.com'
        self.user.email_validated = None
        self.user.save()

        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

        self.assertPOST({
            'email': new_email,
            'is_staff': 'on',
            'is_active': '',
            'email_validated': True,
        }, 'admin:users:edit', self.user.pk, login=self.admin)

        self.user.refresh_from_db()

        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.email_validated)
        self.assertFalse(self.user.is_active)
        self.assertEqual(self.user.email, new_email)
