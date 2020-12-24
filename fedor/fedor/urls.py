from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_fedor.urls')),
    path('auto/', include('auto_matching.urls')),
    #path('admin/', include('admin_panel.urls')),
    path('matching/', include('manual_matching.urls')),
    path('directory/', include('directory.urls')),
    path('analytic/', include('analytic.urls')),
    path('change-style-interface/', change_style_interface),
    re_path(r'^', index)
]
