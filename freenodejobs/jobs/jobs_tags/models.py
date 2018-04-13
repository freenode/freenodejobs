from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    user = models.ForeignKey(
        UserModel,
        related_name='tags_created',
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('title',)
        get_latest_by = 'created'

    def __str__(self):
        return "pk={0.pk} slug={0.slug}".format(self)


class JobTag(models.Model):
    job = models.ForeignKey(
        'jobs.Job',
        related_name='job_tags',
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        'Tag',
        related_name='job_tags',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        related_name='job_tags_created',
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('tag__title',)
        get_latest_by = 'created'
        unique_together = (
            ('job', 'tag'),
        )
