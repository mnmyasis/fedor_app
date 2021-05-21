from django.urls import path
from .views import *

app_name = 'manual_matching'
urlpatterns = [
    path('manual-matching/page/', show_manual_matching_page, name='show_manual_matching_page'),  # Рендер страницы
    path('manual-matching/page/get/sku/', get_sku, name='get_sku'),  # Выгрузка клиентской номенклатуры
    path('manual-matching/page/get/eas/', get_eas, name='get_eas'),  # Выгрузка ЕАС номенклатуры
    path('manual-matching/match/', match_eas_sku, name='match_eas_sku'),  # Ручной Мэтчинг
    path('final-matching/page/get/', get_final_matching, name='get_final_matching'),  # Выгрузка данных финальной таблицы
    path('final-matching/delete/', delete_match, name='delete_match'),  # Удалить результат мэтчинга и отправить в необработанные
    path('filters-matching/', filter_matching, name='filter_matching'),  # Фильтры ручного мэтчинга
    path('filters-matching/sku/', filter_for_sku_list, name='filter_for_sku_list'),  # Фильтр по СКУ
    path('final-filters/', final_table_filter, name='final_table_filter'),  # Фильтры по таблице
    path('final/all-result-matching/', all_result_matching, name='all_result_matching'),  # Все результаты мэтчинга
    path('filters-by-tn_fv/', re_match_filter, name='re_match_filter'),  # Фильтр в модальном окне ремэтч

]
