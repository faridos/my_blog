from django.urls import path

app_name= 'apiapp'
from . import  views
urlpatterns = [
    path('pull', views.pull_data_ms, name='pull_data_ms')
]
