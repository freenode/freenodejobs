from django.urls import reverse
from django.conf import settings

from freenodejobs.utils.test import TestCase

from freenodejobs.jobs.enums import StateEnum


class SmokeTest(TestCase):
    def test_view(self):
        response = self.assertGET(302, 'admin:view', login=self.admin)

        self.assertRedirectsToUrl(
            response,
            'admin:view',
            'waiting_for_approval',
        )

    def test_waiting_for_approval(self):
        self.assertGET(
            200, 'admin:view', 'waiting_for_approval', login=self.admin,
        )


class ApproveTests(TestCase):
    def setUp(self):
        super().setUp()
        self.job.state = StateEnum.WAITING_FOR_APPROVAL
        self.job.save()

    def test_GET(self):
        self.assertGET(
            200, 'admin:approve', self.job.slug, login=self.admin,
        )

    def test_POST(self):
        response = self.assertPOST(
            {}, 'admin:approve', self.job.slug, login=self.admin,
        )

        self.assertRedirectsToUrl(response, 'admin:view')

        history = self.job.state_history.latest()
        self.assertEqual(history.actor, self.admin)
        self.assertEqual(history.description, "Approved.")


class RejectTests(TestCase):
    def setUp(self):
        super().setUp()
        self.job.state = StateEnum.WAITING_FOR_APPROVAL
        self.job.save()

    def test_GET(self):
        self.assertGET(
            200, 'admin:reject', self.job.slug, login=self.admin,
        )

    def test_POST(self):
        with self.assertSendsMail():
            response = self.assertPOST({
                'reason': "Reason for rejection.",
            }, 'admin:reject', self.job.slug, login=self.admin)

        self.assertRedirectsToUrl(response, 'admin:view')

        history = self.job.state_history.latest()
        self.assertEqual(history.actor, self.admin)
        self.assertEqual(history.old_state, StateEnum.WAITING_FOR_APPROVAL)
        self.assertEqual(history.new_state, StateEnum.NEW)
        self.assertEqual(history.description, "Reason for rejection.")

    def test_POST_invalid(self):
        response = self.assertPOST(
            {},
            'admin:reject',
            self.job.slug,
            login=self.admin,
            status_code=200,
        )

        self.assertFormError(response, 'form', 'reason', [
            "This field is required."
        ])


class RemoveTests(TestCase):
    def test_GET(self):
        self.assertGET(
            200, 'admin:remove', self.job.slug, login=self.admin,
        )

    def test_POST(self):
        with self.assertSendsMail():
            response = self.assertPOST({
                'reason': "Reason for removal.",
            }, 'admin:remove', self.job.slug, login=self.admin)

        self.assertRedirectsToUrl(response, 'admin:view')

        history = self.job.state_history.latest()
        self.assertEqual(history.actor, self.admin)
        self.assertEqual(history.old_state, StateEnum.LIVE)
        self.assertEqual(history.new_state, StateEnum.REMOVED)
        self.assertEqual(history.description, "Reason for removal.")


class PermissionTests(TestCase):
    def test_not_admin(self):
        self.assertGET(403, 'admin:view')

    def test_logged_out(self):
        response = self.assertGET(302, 'admin:view', login=None)

        self.assertRedirects(response, '{}?next={}'.format(
            reverse(settings.LOGIN_URL),
            reverse('admin:view'),
        ))
