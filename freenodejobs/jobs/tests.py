from django.urls import reverse
from django.contrib.auth import get_user_model

from freenodejobs.utils.test import TestCase
from freenodejobs.jobs.enums import JobTypeEnum, StateEnum

UserModel = get_user_model()


class ViewTest(TestCase):
    def test_view(self):
        self.assertGET(200, 'jobs:view')

    def test_search(self):
        self.assertGET(200, '{}?q=foo'.format(reverse('jobs:view')))

    def test_redirect(self):
        response = self.assertGET(302, '{}?job_type={}'.format(
            reverse('jobs:view'),
            JobTypeEnum.FULL_TIME.value,
        ))
        self.assertRedirectsToUrl(response, 'jobs:full-time')

    def test_redirect_invalid(self):
        response = self.assertGET(
            302,
            '{}?job_type=invalid'.format(reverse('jobs:view')),
        )
        self.assertRedirectsToUrl(response, 'jobs:view')

    def test_filtered(self):
        self.assertGET(200, 'jobs:full-time')

    def test_search_filtered(self):
        self.assertGET(200, '{}?q=foo'.format(reverse('jobs:full-time')))


class BaseJobTestCase(TestCase):
    def setUp(self, state):
        super().setUp()

        self.job.set_state(state, self.user, "")
        self.job.save()

        self.other = UserModel.objects.create_user(
            'other@example.com',
            'password',
        )

    def assertJobStatusCode(self, status, user):
        self.assertStatusCode(status, self.client.get, self.job, login=user)


class NewJobTest(BaseJobTestCase):
    def setUp(self):
        super().setUp(StateEnum.NEW)

    def test_anonymous(self):
        self.assertJobStatusCode(404, None)

    def test_creator(self):
        self.assertJobStatusCode(200, self.user)

    def test_other_user(self):
        self.assertJobStatusCode(404, self.other)

    def test_staff(self):
        self.assertJobStatusCode(200, self.admin)


class WaitingForApprovalJobTest(BaseJobTestCase):
    def setUp(self):
        super().setUp(StateEnum.WAITING_FOR_APPROVAL)

    def test_anonymous(self):
        self.assertJobStatusCode(404, None)

    def test_creator(self):
        self.assertJobStatusCode(200, self.user)

    def test_other_user(self):
        self.assertJobStatusCode(404, self.other)

    def test_staff(self):
        self.assertJobStatusCode(200, self.admin)


class LiveJobTest(BaseJobTestCase):
    def setUp(self):
        super().setUp(StateEnum.LIVE)

    def test_anonymous(self):
        self.assertJobStatusCode(200, None)

    def test_creator(self):
        self.assertJobStatusCode(200, self.user)

    def test_other_user(self):
        self.assertJobStatusCode(200, self.other)

    def test_staff(self):
        self.assertJobStatusCode(200, self.admin)


class RemovedJobTest(BaseJobTestCase):
    def setUp(self):
        super().setUp(StateEnum.REMOVED)

    def test_anonymous(self):
        self.assertJobStatusCode(410, None)

    def test_creator(self):
        self.assertJobStatusCode(410, self.user)

    def test_other_user(self):
        self.assertJobStatusCode(410, self.other)

    def test_staff(self):
        self.assertJobStatusCode(410, self.admin)


class FeedTest(TestCase):
    def test_view(self):
        self.assertGET(200, 'jobs:feed')
