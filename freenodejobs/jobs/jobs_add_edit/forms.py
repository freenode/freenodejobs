from django import forms

from freenodejobs.jobs.enums import StateEnum

from ..models import Job
from ..jobs_tags.models import Tag


class AddEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'title',
            'job_type',
            'location',
            'apply_url',
            'description',
            'tags',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].choices = [
            (x.pk, x.title) for x in Tag.objects.all()
        ]

        # Remove empty label
        self.fields['job_type'].choices.pop(0)

    def save(self, user):
        instance = super().save(commit=False)
        instance.user = user
        instance.save()

        # Ensure newly-unselected tags are removed
        for x in instance.job_tags.all():
            if x.tag not in self.cleaned_data['tags']:
                x.delete()

        # Ensure selected tags are selected
        for x in self.cleaned_data['tags']:
            instance.job_tags.get_or_create(tag=x, defaults={'user': user})

        if instance.state == StateEnum.LIVE and self.changed_data:
            txt = "Edited whilst live."
            instance.set_state(StateEnum.WAITING_FOR_APPROVAL, user, txt)
            instance.save()

        return instance


class SubmitForApprovalForm(forms.Form):
    def __init__(self, job, *args, **kwargs):
        self.job = job

        super().__init__(*args, **kwargs)

    def clean(self):
        if self.job.state != StateEnum.NEW:
            raise forms.ValidationError("Job is not currently new.")

        return self.cleaned_data

    def save(self, user):
        txt = "Submitted for approval."

        self.job.set_state(StateEnum.WAITING_FOR_APPROVAL, user, txt)
        self.job.save()

        return self.job


class RemoveForm(forms.Form):
    reason = forms.CharField()

    def __init__(self, job, *args, **kwargs):
        self.job = job

        super().__init__(*args, **kwargs)

    def save(self, user):
        self.job.set_state(
            StateEnum.REMOVED,
            user,
            self.cleaned_data['reason'],
        )

        self.job.save()

        return self.job
