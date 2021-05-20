from django.urls import path
from .views import *

urlpatterns = [
    path('matching/page/', auto_matching_page, name='show_auto_matching_page'),  # Страница АВТО-МЭТЧИНГ
    path('matching/algoritm/', algoritm_mathing, name='algoritm_mathing'),  # Запуск алгоритма DEV
    path('matching/create-work-algoritm/', create_work_algoritm, name='create_work_algoritm'),  # Запуск алгоритма
]
