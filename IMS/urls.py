'''from django.urls import include, path
from django.contrib import admin

from IMS.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('sopeoims.urls')),
]'''
# ims_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sopeoims.urls')),
]
