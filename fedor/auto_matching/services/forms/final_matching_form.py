from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Max
from manual_matching.models import *
from directory.models import ClientDirectory


class FinalMatchingForm(forms.ModelForm):
    class Meta:
        model = FinalMatching
        fields = '__all__'

    def save(self):
        result, create = FinalMatching.objects.update_or_create(
            sku_dict=self.cleaned_data['sku_dict'],
            defaults={
                'sku_dict': self.cleaned_data['sku_dict'],
                'eas_dict': self.cleaned_data['eas_dict'],
                'type_binding': self.cleaned_data['type_binding'],
                'name_binding': self.cleaned_data['name_binding'],
                'old_type_binding': self.cleaned_data['old_type_binding'],
                'number_competitor': self.cleaned_data['number_competitor'],
                'user': self.cleaned_data['user']
            }
        )
        return create

