from django.contrib.syndication.views import Feed

from .models import Job


class AllJobs(Feed):
    link = '/'
    title = "Freenode Jobs"
    title_template = 'jobs/feed/title.html'
    description_template = 'jobs/feed/description.html'

    def items(self):
        return Job.objects.live()

    def item_pubdate(self, obj):
        return obj.updated
