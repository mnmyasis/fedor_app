from django.urls import path
from .views import *

urlpatterns = [
    path('matching/page/', show_auto_joint_page, name='show_auto_joint_page'),
    path('matching/algoritm/', algoritm_mathing, name='algoritm_mathing'),
    path('matching/client_directory/data/get/', search_client_directory_data, name='search_client_directory_data'),
    path('matching/client_directory/data/post/', joint_element),
    path('matching/base_directory/inject', inject_base_directory),
    path('matching/client_directory/inject/', inject_client_directory)
]