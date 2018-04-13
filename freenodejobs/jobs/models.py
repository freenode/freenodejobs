import functools

from enumfields import EnumIntegerField

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from .enums import JobTypeEnum, StateEnum
from .managers import JobManager
from .transitions import dispatch

UserModel = get_user_model()


class Job(models.Model):
    user = models.ForeignKey(
        UserModel,
        related_name='jobs',
        on_delete=models.CASCADE,
    )

    slug = models.CharField(
        unique=True,
        max_length=8,
        default=functools.partial(get_random_string, 8, 'acefhkjprutwvyx'),
    )

    state = EnumIntegerField(StateEnum, default=StateEnum.NEW)

    title = models.CharField(max_length=255)
    job_type = EnumIntegerField(JobTypeEnum)
    location = models.CharField(max_length=255)
    apply_url = models.URLField()
    description = models.TextField()

    tags = models.ManyToManyField(
        'jobs_tags.Tag',
        blank=True,
        through='jobs_tags.JobTag',
        through_fields=('job', 'tag'),
    )

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    objects = JobManager()

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def get_absolute_url(self):
        return reverse('jobs:view', args=(slugify(self.title), self.slug))

    def __str__(self):
        return "pk={0.pk} slug={0.slug} title={0.title!r}".format(self)

    def set_state(self, new_state, *args, **kwargs):
        dispatch(self, self.state, new_state, *args, **kwargs)

        self.state = new_state
