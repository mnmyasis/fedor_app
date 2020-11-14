from django.urls import path
from .views import *

app_name = 'auth_fedor'
urlpatterns = [
    path('login/', show_login_page, name="login_page"),
    path('login/on/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout')
]
