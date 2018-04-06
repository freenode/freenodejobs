from freenodejobs.utils.test import TestCase


class StaticTests(TestCase):
    def test_landing(self):
        self.assertGET(200, 'static:landing')

    def test_privacy_policy(self):
        self.assertGET(200, 'static:privacy-policy')

    def test_terms_of_service(self):
        self.assertGET(200, 'static:terms-of-service')
