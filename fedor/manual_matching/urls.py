from django.urls import path
from .views import *

urlpatterns = [
    path('manual-matching/page/', show_manual_matching_page, name='show_manual_matching_page'),
    path('manual-matching/page/get/', get_sku, name='get_sku')
]
