from django.db import models

from .enums import StateEnum


class JobManager(models.Manager):
    def live(self):
        return self.filter(state=StateEnum.LIVE)

    def editable(self):
        return self.exclude(state=StateEnum.REMOVED)

    def by_state(self):
        counts = dict(self.order_by().values_list('state').annotate(
            models.Count('state'),
        ))

        result = []
        for x in StateEnum:
            result.append((x, counts.get(x, 0)))

        return result
