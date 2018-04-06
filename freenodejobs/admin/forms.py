from django import forms

from freenodejobs.jobs.enums import StateEnum


class ApproveForm(forms.Form):
    def __init__(self, job, *args, **kwargs):
        self.job = job

        super().__init__(*args, **kwargs)

    def save(self, user):
        self.job.set_state(StateEnum.LIVE, user, "Approved.")
        self.job.save()

        return self.job


class RejectForm(forms.Form):
    reason = forms.CharField()

    def __init__(self, job, *args, **kwargs):
        self.job = job

        super().__init__(*args, **kwargs)

    def save(self, user):
        self.job.set_state(
            StateEnum.NEW,
            user,
            self.cleaned_data['reason'],
        )

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
