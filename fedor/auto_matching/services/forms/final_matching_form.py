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
        result, create = FinalMatching.objects.get_or_create(
            id_sku_dict=self.cleaned_data['id_sku_dict'],
            defaults={
                'id_sku_dict': self.cleaned_data['id_sku_dict'],
                'id_eas_dict': self.cleaned_data['id_eas_dict'],
                'type_binding': self.cleaned_data['type_binding'],
                'name_binding': self.cleaned_data['name_binding'],
                'old_type_binding': self.cleaned_data['old_type_binding'],
                'number_competitor': self.cleaned_data['number_competitor'],
                'user': self.cleaned_data['user']
            }
        )
        return result

    #def matching_status_edit(self, ids_dict):
    #   manual_matching = ManualMatchingData.objects.filter(id_sku_dict=ids_dict['id_sku_dict']).update(matching_status_status=True)

    #def sku_status_edit(self, id_sku_dict):
    #    sku = ClientDirectory.objects.get(id=id_sku_dict).update(matching_status=True)
