from django.urls import path
from .views import *

app_name = 'admin_joint'
urlpatterns = [
    path('user/create/page/', show_registration_page, name='show_registration_page'),
    path('user/create/', user_registrations, name='create_user'),
    path('user/update/page/<int:user_id>', show_update_user_profile_page, name='show_update_user_profile_page'),
    path('user/update/<int:user_id>', update_user_profile, name='update_user_profile'),
    path('user/delete/<int:user_id>', update_user_profile, name='delete_user_profile')
]