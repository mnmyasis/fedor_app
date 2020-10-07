from django.urls import path
from .views import *

urlpatterns = [
    path('joint/page/', show_auto_joint_page, name='show_auto_joint_page'),
    path('joint/client_directory/data/get/', search_client_directory_data, name='search_client_directory_data'),
    path('joint/client_directory/data/post/', joint_element),
    path('joint/base_directory/inject', inject_base_directory),
    path('joint/client_directory/inject/', inject_client_directory)
]