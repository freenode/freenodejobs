from urllib.parse import urlencode

from django import forms
from django.urls import reverse
from django.db.models import Q
from django.utils.safestring import mark_safe

from .enums import JobTypeEnum, JOB_TYPE_MAP
from .models import Job


class FilterForm(forms.ModelForm):
    q = forms.CharField(required=False)

    class Meta:
        model = Job
        fields = (
            'job_type',
        )

    def __init__(self, job_type, data, *args, **kwargs):
        self.orig_data = data

        data = self.orig_data.copy()
        data['job_type'] = job_type

        super().__init__(data, *args, **kwargs)

        self.fields['job_type'].required = False

    def get_redirect(self):
        if not self.is_valid():
            return 'jobs:view'

        if 'job_type' in self.orig_data:
            try:
                enum = JobTypeEnum(int(self.orig_data['job_type']))
                target = 'jobs:{}'.format(JOB_TYPE_MAP[enum])
            except ValueError:
                target = 'jobs:view'

            q = self.orig_data.get('q', '')
            if q:
                target = '{}?{}'.format(reverse(target), urlencode({'q': q}))

            return target

        return None

    def get_title(self):
        x = "{} jobs".format(self.cleaned_data['job_type'].label
                             if self.cleaned_data['job_type'] else "All")

        if self.cleaned_data['q']:
            x = "{} matching <em>{}</em>".format(x, self.cleaned_data['q'])

        return mark_safe(x)

    def get_queryset(self):
        self.full_clean()

        qs = Job.objects.live()

        if self.cleaned_data['job_type']:
            qs = qs.filter(job_type=self.cleaned_data['job_type'])

        if self.cleaned_data['q']:
            q = Q()
            for x in (
                'title',
                'location',
                'description',
                'tags__title',
                'user__profile__name',
            ):
                q |= Q(**{'{}__icontains'.format(x): self.cleaned_data['q']})

            qs = qs.filter(q)

        return qs

    def has_data(self):
        return any(self.cleaned_data.values())
