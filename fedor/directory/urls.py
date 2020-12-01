from django.urls import path
from .views import *

urlpatterns = [
    path('number-competitor-list/', number_competitor_list, name='number_competitor_list'),  # Получить список клиентских справочников
    path('new-sku/', get_new_sku, name='new_sku'),
]
