from django.urls import path
from .views import *

urlpatterns = [
    path('number-competitor-list/', number_competitor_list, name='number_competitor_list'),  # Получить список клиентских справочников
    path('new-sku/', get_new_sku, name='new_sku'),
    path('group_changes/', group_change, name='group_change'),  # Массовые подмены
    path('group_changes/list/', group_changes_list, name='group_change_list'),  # Список подмен для исключения
    path('group_changes/filter/', group_changes_filter, name='group_changes_filter'),
    path('group_changes/edit-list/', group_changes_edit_list, name='group_changes_edit_list'),  # Подмены для редактирования
]
