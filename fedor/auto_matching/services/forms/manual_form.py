from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Max
from manual_matching.models import *
from directory.models import ClientDirectory


class ManualMatchingForm(forms.ModelForm):
    class Meta:
        model = ManualMatchingData
        fields = '__all__'

    #def matching_status_sku_edit(self, id_sku_dict):
    #    sku = ClientDirectory.objects.get(id=id_sku_dict)
    #    sku.matching_status = True
    #    sku.save()
