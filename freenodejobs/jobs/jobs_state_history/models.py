from enumfields import EnumIntegerField

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..enums import StateEnum

UserModel = get_user_model()


class History(models.Model):
    job = models.ForeignKey(
        'jobs.Job',
        related_name='state_history',
        on_delete=models.CASCADE,
    )

    old_state = EnumIntegerField(StateEnum)
    new_state = EnumIntegerField(StateEnum)

    actor = models.ForeignKey(
        UserModel,
        related_name='state_history_changes',
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=255)

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __str__(self):
        return "pk={0.pk} '{0.old_state}' -> '{0.new_state}'".format(self)
