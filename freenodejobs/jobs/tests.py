from django.urls import reverse

from freenodejobs.utils.test import TestCase
from freenodejobs.jobs.enums import JobTypeEnum, StateEnum


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


class JobTest(TestCase):
    def test_new(self):
        self.job.set_state(StateEnum.NEW, self.user, "")
        self.job.save()
        self.assertStatusCode(404, self.client.get, self.job)

    def test_new_to_waiting_for_approval(self):
        self.job.set_state(StateEnum.WAITING_FOR_APPROVAL, self.user, "")
        self.job.save()
        self.assertStatusCode(404, self.client.get, self.job)

    def test_waiting_for_approval_to_new(self):
        self.job.set_state(StateEnum.WAITING_FOR_APPROVAL, self.user, "")
        self.job.save()
        self.assertStatusCode(404, self.client.get, self.job)

    def test_waiting_to_live(self):
        self.job.set_state(StateEnum.LIVE, self.user, "")
        self.job.save()
        self.assertGET(200, self.job)

    def test_live_to_removed(self):
        self.job.set_state(StateEnum.REMOVED, self.user, "")
        self.job.save()
        self.assertStatusCode(404, self.client.get, self.job)


class FeedTest(TestCase):
    def test_view(self):
        self.assertGET(200, 'jobs:feed')
