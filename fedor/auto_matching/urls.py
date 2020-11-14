from django.urls import path
from .views import *

urlpatterns = [
    path('matching/page/', auto_matching_page, name='show_auto_matching_page'),
    path('matching/algoritm/', algoritm_mathing, name='algoritm_mathing'),
    path('matching/client_directory/data/get/', search_client_directory_data, name='search_client_directory_data'),
    path('matching/base_directory/inject/', inject_base_directory),
    path('matching/client_directory/inject/', inject_client_directory)
]