from django import forms

from freenodejobs.jobs.enums import StateEnum

from .models import Profile


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = (
            'name',
            'url',
        )

    def clean_image(self):
        val = self.cleaned_data['image']

        if val is None and self.instance._state.adding:
            raise forms.ValidationError("You must specify an image.")

        return val

    def save(self, user):
        created = bool(self.instance._state.adding)

        instance = super().save(commit=False)
        instance.user = user
        instance.save()

        if self.cleaned_data['image']:
            instance.image.save(self.cleaned_data['image'])
            instance.save()

        if self.changed_data:
            for x in user.jobs.live():
                x.set_state(
                    StateEnum.WAITING_FOR_APPROVAL,
                    user,
                    "Updated profile.",
                )
                x.save()

        return instance, created
