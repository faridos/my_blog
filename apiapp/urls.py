from django.urls import path

app_name= 'apiapp'
from . import  views
urlpatterns = [
    path('pull/<str:plant_id>/<str:from>/<str:to>', views.PullDataFromMS.as_view(), name='pull_data_ms')
]
