from freenodejobs.utils.test import TestCase

from freenodejobs.jobs.enums import JobTypeEnum, StateEnum


class NoProfileTests(TestCase):
    def setUp(self):
        super().setUp()

        self.user.profile.delete()
        self.user.refresh_from_db()

    def test_add(self):
        response = self.assertGET(302, 'jobs:add-edit:add')
        self.assertRedirectsToUrl(response, 'profile:view')

    def test_edit(self):
        response = self.assertGET(302, 'jobs:add-edit:edit', self.job.slug)
        self.assertRedirectsToUrl(response, 'profile:view')


class AddTests(TestCase):
    def test_GET(self):
        self.assertGET(200, 'jobs:add-edit:add')

    def test_POST(self):
        self.assertEqual(self.user.jobs.count(), 1)

        self.assertPOST({
            'title': "Job title",
            'location': "Job location",
            'description': "Job description",
            'apply_url': 'https://example.com/',
            'job_type': JobTypeEnum.CONTRACT.value,
        }, 'jobs:add-edit:add')

        self.assertEqual(self.user.jobs.count(), 2)

    def test_POST_invalid(self):
        response = self.assertPOST({}, 'jobs:add-edit:add', status_code=200)

        self.assertFormError(response, 'form', 'title', [
            "This field is required."
        ])


class EditTests(TestCase):
    def test_GET(self):
        self.assertGET(200, 'jobs:add-edit:edit', self.job.slug)

    def test_GET_removed(self):
        self.job.state = StateEnum.REMOVED
        self.job.save()
        self.assertGET(404, 'jobs:add-edit:edit', self.job.slug)

    def test_POST(self):
        self.assertEqual(self.job.state, StateEnum.LIVE)

        with self.assertSendsMail():
            self.assertPOST({
                'title': "New job title",
                'location': "New job location",
                'description': "New job description",
                'apply_url': 'https://example.com/new',
                'job_type': JobTypeEnum.FULL_TIME.value,
            }, 'jobs:add-edit:edit', self.job.slug)

        self.job.refresh_from_db()
        self.assertEqual(self.job.title, "New job title")
        self.assertEqual(self.job.state, StateEnum.WAITING_FOR_APPROVAL)

        history = self.job.state_history.latest()
        self.assertEqual(history.actor, self.user)
        self.assertEqual(history.old_state, StateEnum.LIVE)
        self.assertEqual(history.new_state, StateEnum.WAITING_FOR_APPROVAL)
        self.assertEqual(history.description, "Edited whilst live.")

    def test_POST_invalid(self):
        response = self.assertPOST(
            {}, 'jobs:add-edit:edit', self.job.slug, status_code=200,
        )

        self.assertFormError(response, 'form', 'title', [
            "This field is required."
        ])


class RemoveTests(TestCase):
    def test_GET(self):
        self.assertGET(200, 'jobs:add-edit:remove', self.job.slug)

    def test_POST(self):
        self.assertEqual(self.job.state, StateEnum.LIVE)

        with self.assertSendsMail():
            self.assertPOST({
                'reason': "Reason for removal."
            }, 'jobs:add-edit:remove', self.job.slug)

        self.job.refresh_from_db()
        self.assertEqual(self.job.state, StateEnum.REMOVED)

        history = self.job.state_history.latest()
        self.assertEqual(history.actor, self.user)
        self.assertEqual(history.description, "Reason for removal.")


class SubmitForApprovalTests(TestCase):
    def test_GET(self):
        self.assertGET(405, 'jobs:add-edit:submit-for-approval', self.job.slug)

    def test_POST(self):
        self.job.state = StateEnum.NEW
        self.job.save()

        with self.assertSendsMail():
            self.assertPOST(
                {},
                'jobs:add-edit:submit-for-approval',
                self.job.slug,
            )

        self.job.refresh_from_db()
        self.assertEqual(self.job.state, StateEnum.WAITING_FOR_APPROVAL)

        history = self.job.state_history.latest()
        self.assertEqual(history.actor, self.user)
        self.assertEqual(history.old_state, StateEnum.NEW)
        self.assertEqual(history.new_state, StateEnum.WAITING_FOR_APPROVAL)
        self.assertEqual(history.description, "Submitted for approval.")

    def test_POST_waiting_for_approval(self):
        self.job.state = StateEnum.WAITING_FOR_APPROVAL
        self.job.save()

        self.assertPOST(
            {}, 'jobs:add-edit:remove', self.job.slug, status_code=200,
        )

    def test_POST_removed(self):
        self.job.state = StateEnum.REMOVED
        self.job.save()

        self.assertPOST(
            {}, 'jobs:add-edit:remove', self.job.slug, status_code=404,
        )
