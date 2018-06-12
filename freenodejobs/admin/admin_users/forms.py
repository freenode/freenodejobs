from django import forms
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()


class FilterForm(forms.Form):
    order_by = forms.ChoiceField(choices=(
        ('-date_joined', "Date joined (most recent first)"),
        ('date_joined', "Date joined (oldest first)"),
        ('email', "Email (ascending)"),
        ('-email', "Email (descending)"),
    ), required=False)

    only_admins = forms.BooleanField(required=False)

    def apply_filter(self, qs):
        self.full_clean()

        if self.cleaned_data['only_admins']:
            qs = qs.filter(is_staff=True)

        qs = qs.order_by(self.cleaned_data['order_by'], 'pk')

        return qs

    def clean_order_by(self):
        val = self.cleaned_data['order_by']

        return val or self.fields['order_by'].choices[0][0]


class UserForm(forms.ModelForm):
    email_validated = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'is_active',
            'is_staff',
        )

    def save(self):
        instance = super().save(commit=False)

        if self.cleaned_data['email_validated']:
            # Was unset before; set to "now".
            if instance.email_validated is None:
                instance.email_validated = timezone.now()
        else:
            # Clear the validation
            instance.email_validated = None

        instance.save()

        return instance
