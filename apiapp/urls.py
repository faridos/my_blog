from django.urls import path, include, re_path
app_name = 'apiapp'
from . import views
from apiapp.views import PlantViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')
urlpatterns = [
    path('pull/<str:plant_id>/<str:from>/<str:to>', views.DataPointCreateView.as_view(), name='data_point_create')
]
urlpatterns += router.urls
