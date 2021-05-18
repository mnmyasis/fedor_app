from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(ManualMatchingData)
class ManualMatchingDataAdmin(admin.ModelAdmin):
    list_display = ('sku_dict', 'eas_dict', 'name_eas', 'name_sku', 'lvl', 'lvl2', 'perc_num', 'matching_status',
                    'number_competitor', 'user', 'create_date', 'update_date')
    list_filter = ('number_competitor', 'user', 'create_date', 'update_date', 'lvl', 'lvl2')


@admin.register(FinalMatching)

class FinalMatchingAdmin(admin.ModelAdmin):
    list_display = ('sku_dict', 'eas_dict', 'type_binding', 'name_binding', 'user', 'number_competitor',
                    'create_date', 'update_date')
    list_filter = ('name_binding', 'user', 'number_competitor', 'create_date', 'update_date', 'type_binding')