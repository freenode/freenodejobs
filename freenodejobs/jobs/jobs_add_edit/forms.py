from django import forms

from freenodejobs.jobs.enums import StateEnum

from ..models import Job


class AddEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'title',
            'job_type',
            'location',
            'apply_url',
            'description',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove empty label
        self.fields['job_type'].choices.pop(0)

    def save(self, user):
        instance = super().save(commit=False)
        instance.user = user
        instance.save()

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
