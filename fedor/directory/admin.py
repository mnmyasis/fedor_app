from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(SyncEAS)


# admin.site.register(Competitors)
@admin.register(SyncEAS)
class EASAdmin(admin.ModelAdmin):
    list_display = ('eas_id', 'status', 'barcode', 'umbrella_brand', 'tn_fv', 'corporation',
                    'manufacturer', 'trade_name_rus', 'pack_key',
                    'dosage', 'volwe',
                    'size', 'create_date', 'update_date')
    list_filter = ('status', 'create_date', 'update_date')


@admin.register(Competitors)
class CompetitorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'pharmacy_id', 'firm_id')

@admin.register(SyncSKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ('sku_id', 'nnt', 'name', 'matching_status', 'number_competitor', 'create_date', 'update_date')
    list_filter = ('matching_status', 'create_date', 'update_date', 'number_competitor')