from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views
from . import views_reports as views_reports

app_name = 'apiapp'

router = DefaultRouter()
router.register(r'plants', views.PlantViewSet, basename='plant')
urlpatterns = [
    path('pull/<str:plant_id>/<str:from_date>/<str:to_date>', views.DataPointCreateView.as_view(),
         name='data_point_create'),
    path('check/<int:task_id>', views.check_result_task, name='check_result_task'),
    path('simple/monthly/report/<int:plant_id>/<int:x_months>', views_reports.MonthlyReportsCreateView.as_view(),
         name='get_simple_monthly_report'),
    path('simple/yearly/report/<int:plant_id>/<int:year>', views_reports.YearlyReportsCreateView.as_view(),
         name='get_simple_monthly_report'),
]
urlpatterns += router.urls
