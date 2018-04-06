from freenodejobs.utils.test import TestCase


class SmokeTests(TestCase):
    def test_view(self):
        self.assertGET(200, 'account:two-factor-auth:view')

    def test_enabled(self):
        response = self.assertGET(302, 'account:two-factor-auth:enabled')

        self.assertRedirectsToUrl(response, 'account:two-factor-auth:view')

    def test_disable(self):
        self.assertPOST({}, 'account:two-factor-auth:disable')

    def test_setup(self):
        self.assertGET(200, 'account:two-factor-auth:setup')
