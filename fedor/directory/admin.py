from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SyncEAS)


# admin.site.register(Competitors)

@admin.register(Competitors)
class CompetitorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'pharmacy_id', 'firm_id')

@admin.register(SyncSKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ('sku_id', 'nnt', 'name', 'matching_status', 'number_competitor', 'create_date', 'update_date')
