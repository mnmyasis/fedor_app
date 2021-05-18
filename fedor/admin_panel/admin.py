from django.contrib import admin
from .models import *

# Register your models here.

#admin.site.register(Tasks)

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'name', 'status', 'result', 'user')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_level', 'competitor')

@admin.register(AccessLevel)
class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'level_name')

@admin.register(FedorLog)
class FedorLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'sku_id', 'eas_id', 'action', 'create_date')
    list_filter = ('user', 'action', 'create_date')