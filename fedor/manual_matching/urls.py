from django.urls import path
from .views import *

urlpatterns = [
    path('manual-matching/page/', show_manual_matching_page, name='show_manual_matching_page'),  # Рендер страницы
    path('manual-matching/page/get/sku/', get_sku, name='get_sku'),  # Выгрузка клиентской номенклатуры
    path('manual-matching/page/get/eas/', get_eas, name='get_eas'),  # Выгрузка ЕАС номенклатуры
    path('manual-matching/match/', match_eas_sku, name='match_eas_sku'),  # Ручной Мэтчинг
    path('final-matching/page/get/', get_final_matching, name='get_final_matching'),  # Выгрузка данных финальной таблицы
    path('final-matching/edit-match/', edit_match, name='edit_match'),  # Изменение статуса мэтчинга финальной таблицы
    path('filters-matching/', filter_matching, name='edit_match'),  # Фильтры
]
