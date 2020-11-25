from django.urls import path
from .views import *

urlpatterns = [
    path('number-competitor-list/', number_competitor_list, name='number_competitor_list'),  # Получить список клиентских справочников
]
