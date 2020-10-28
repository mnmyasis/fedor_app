from django.urls import path
from .views import *

urlpatterns = [
    path('manual-matching/page/', show_manual_matching_page, name='show_manual_matching_page'),
    path('manual-matching/page/get/sku/', get_sku, name='get_sku'),
    path('manual-matching/page/get/eas/', get_eas, name='get_eas'),
    path('manual-matching/match/', match_eas_sku, name='match_eas_sku'),
]
