from django import forms
from directory.models import GroupChangeTable


class GroupChangeForm(forms.ModelForm):
    class Meta:
        model = GroupChangeTable
        fields = '__all__'

    def save(self, pk):
        result, create = GroupChangeTable.objects.update_or_create(
            pk=pk,
            defaults={
                'change': self.cleaned_data['change'],
                'search': self.cleaned_data['search'],
            }
        )
        return create
