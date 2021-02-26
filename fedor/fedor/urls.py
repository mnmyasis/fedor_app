from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('auth/', include('auth_fedor.urls')),
    path('auto/', include('auto_matching.urls')),
    path('admin/', include('admin_panel.urls')),
    path('matching/', include('manual_matching.urls')),
    path('directory/', include('directory.urls')),
    path('analytic/', include('analytic.urls')),
    re_path(r'^', index)
]
