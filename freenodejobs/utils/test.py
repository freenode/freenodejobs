import shutil
import contextlib

from django.conf import settings
from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from freenodejobs.jobs.enums import StateEnum, JobTypeEnum

from freenodejobs.profile.models import Profile
from freenodejobs.jobs.jobs_tags.models import Tag

UserModel = get_user_model()


class TestCase(TestCase):
    def setUp(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

        self.user = UserModel.objects.create_user(
            'test@example.com',
            'password',
        )

        self.user.email_validated = self.user.date_joined
        self.user.save()

        Profile.objects.create(
            user=self.user,
            name="Profile name",
            url="https://example.com/",
        )

        self.admin = UserModel.objects.create_staff(
            'admin@example.com',
            'password',
        )

        self.job = self.user.jobs.create(
            title="Job title",
            state=StateEnum.LIVE,
            job_type=JobTypeEnum.FULL_TIME,
        )

        self.tag = Tag.objects.create(
            title="Tag name",
            slug='tag-name',
            user=self.user,
        )

        self.job.job_tags.create(tag=self.tag, user=self.user)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def assertStatusCode(self, status_code, fn, urlconf, *args, **kwargs):
        user = kwargs.pop('login', self.user)
        if user:
            self.client.login(email=user.email, password='password')

        if hasattr(urlconf, 'get_absolute_url'):
            urlconf = urlconf.get_absolute_url()

        if not urlconf.startswith('/'):
            urlconf = reverse(urlconf, args=args, kwargs=kwargs)

        response = fn(urlconf)

        self.assertEqual(
            response.status_code,
            status_code,
            response.content or response,
        )

        return response

    def assertGET(self, status_code, *args, **kwargs):
        client_kwargs = {
            'follow': kwargs.pop('follow', False),
        }
        if kwargs.pop('is_ajax', False):
            client_kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return self.assertStatusCode(
            status_code,
            lambda x: self.client.get(x, **client_kwargs),
            *args,
            **kwargs
        )

    def assertPOST(self, data, *args, **kwargs):
        status_code = kwargs.pop('status_code', 302)

        client_kwargs = {}
        if kwargs.pop('is_ajax', False):
            client_kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        return self.assertStatusCode(
            status_code,
            lambda x: self.client.post(x, data, **client_kwargs),
            *args,
            **kwargs
        )

    def assertRedirectsToUrl(self, response, urlconf, *args, **kwargs):
        return self.assertRedirects(
            response,
            reverse(urlconf, args=args, kwargs=kwargs),
            fetch_redirect_response=False,
        )

    @contextlib.contextmanager
    def assertSendsMail(self, num_expected=1):
        num_before = len(mail.outbox)
        yield
        num_sent = len(mail.outbox) - num_before

        self.assertTrue(
            num_expected == num_sent,
            "Expected {} mail{} to be sent (saw {})".format(
                num_expected, 's' if num_expected != 1 else '', num_sent,
            ),
        )
