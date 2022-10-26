from django.urls import path, include, re_path
app_name = 'apiapp'
from . import views
from apiapp.views import PlantViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')
urlpatterns = [
    path('pull/<str:plant_id>/<str:from_date>/<str:to_date>', views.DataPointCreateView.as_view(), name='data_point_create'),
    path('check/<int:task_id>', views.check_result_task, name='check_result_task')
]
urlpatterns += router.urls
