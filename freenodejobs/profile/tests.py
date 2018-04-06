from django.contrib.staticfiles.finders import find

from freenodejobs.utils.test import TestCase

TEST_IMAGE = find('img/f_generic_base/favicon.png')


class NoProfileTests(TestCase):
    def setUp(self):
        super().setUp()

        self.user.profile.delete()
        self.user.jobs.all().delete()
        self.user.refresh_from_db()

        self.assertFalse(hasattr(self.user, 'profile'))

    def test_GET(self):
        self.assertGET(200, 'profile:view')

    def test_POST(self):
        with self.assertSendsMail(0):
            with open(TEST_IMAGE, 'rb') as f:
                self.assertPOST({
                    'name': "Name",
                    'url': "https://example.com/",
                    'image': f,
                }, 'profile:view')

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.name, "Name")


class ProfileTests(TestCase):
    def test_GET(self):
        self.assertGET(200, 'profile:view')

    def test_POST(self):
        self.assertTrue(self.user.jobs.live().exists())

        with self.assertSendsMail():
            with open(TEST_IMAGE, 'rb') as f:
                self.assertPOST({
                    'name': "New name",
                    'url': "https://example.com/",
                    'image': f,
                }, 'profile:view')

        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.name, "New name")
        self.assertFalse(self.user.jobs.live().exists())
        self.assertTrue(self.user.profile.image.original.exists())
