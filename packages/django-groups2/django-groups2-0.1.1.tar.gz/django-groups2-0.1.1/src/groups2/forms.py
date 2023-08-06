from django import forms
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model


User = get_user_model()


class GroupUsersForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Users',
            is_stacked=False
        )
    )

    class Meta:
        fields = []
        model = Group

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            users = self.instance.user_set.all()
            self['users'].initial = users
        