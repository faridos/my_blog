from django.contrib import admin
from django.urls import include, path

from .views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView, name='power_is_power'),
    path('api/', include('apiapp.urls'))
]
