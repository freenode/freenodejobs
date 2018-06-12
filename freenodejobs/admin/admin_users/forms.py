from django import forms
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
