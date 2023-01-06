from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import permissions
from .views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView, name='power_is_power'),

]

