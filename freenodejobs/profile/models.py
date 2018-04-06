from django_yadt import YADTImageField
from django_auto_one_to_one import PerUserData

from django.db import models
from django.utils import timezone


class Profile(PerUserData(auto=False)):
    name = models.CharField(max_length=255)
    url = models.URLField()

    image = YADTImageField(variants={
        'resized': {
            'format': 'jpeg',
            'pipeline': [{
                'name': 'thumbnail',
                'width': 200,
                'height': 200,
            }],
        },
    }, cachebust=True)

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __str__(self):
        return u"pk={.pk}".format(self)
