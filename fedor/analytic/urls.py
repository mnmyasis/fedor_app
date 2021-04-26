from django.urls import path
from .views import *

urlpatterns = [
    path('page/', analytic_page, name='analytic_page'),  # Страница аналитики
    path('status-matchings/', status_matchings, name='status_matchings'),  # Накопления по статусам мэтчинга
    path('status-changes/', status_changes, name='status_changes'),  # Виды изменения статусов
    path('user-status-changes/', user_status_changes, name='user_status_changes'),  # Измененные статусы пользователем
    path('user-rating/', user_rating, name='user_rating'),  # Рейтинг пользователей
    path('raw-sku-all-number-competitor/', raw_sku, name='raw_sku')  # Необработанные
]