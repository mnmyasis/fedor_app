from django.urls import path
from .views import *

urlpatterns = [
    path('page/', analytic_page, name='analytic_page'),
    path('status-matchings/', status_matchings, name='status_matchings'),
    path('status-changes/', status_changes, name='status_changes'),
    path('user-status-changes/', user_status_changes, name='user_status_changes')
]