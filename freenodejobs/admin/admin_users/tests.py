from freenodejobs.utils.test import TestCase


class SmokeTest(TestCase):
    def test_view(self):
        self.assertGET(200, 'admin:users:view', login=self.admin)

    def test_set_admin(self):
        self.assertFalse(self.user.is_staff)
        self.assertPOST(
            {},
            'admin:users:set-admin',
            self.user.pk,
            login=self.admin,
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)

    def test_remove_admin(self):
        self.test_set_admin()

        self.assertPOST(
            {},
            'admin:users:remove-admin',
            self.user.pk,
            login=self.admin,
        )
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
