from django import forms
from manual_matching.models import GroupChangeTable


class GroupChangeForm(forms.ModelForm):
    class Meta:
        model = GroupChangeTable
        fields = '__all__'

    def save(self):
        result, create = GroupChangeTable.objects.update_or_create(
            pk=self.cleaned_data['pk'],
            defaults={
                'change': self.cleaned_data['change'],
                'search': self.cleaned_data['search'],
            }
        )
        return create
