from django.urls import path
from .views import *

urlpatterns = [
    path('page/', analytic_page, name='analytic_page'),
    path('status-matchings/', status_matchings, name='status_matchings')
]