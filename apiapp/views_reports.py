from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
from .serializers import DataPointSerializer
from .models import Plant, DataPoint
from .utils import *
from .tasks import create_data_points_task


class MonthlyReportsCreateView(generics.CreateAPIView):
    """
     API to get the reports of high consuming energy plants in the last x months,  grouped by months

    """
    serializer_class = DataPointSerializer
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        plant_ins = get_object_or_404(Plant, id=kwargs["plant_id"])
        qs = DataPoint.objects.select_related().filter(plant=plant_ins, data_date__year=kwargs["year"])
        # i am intrested only in these fields
        q = qs.values('data_date', 'plant', 'energy_expected', 'energy_observed', 'irradiation_expected',
                      'irradiation_observed')
        return JsonResponse({"success": True}, status=status.HTTP_200_OK)


class YearlyReportsCreateView(generics.CreateAPIView):
    """
    API to get the reports of high consuming energy plants in the last x years, grouped by the data_year field

    """
    serializer_class = DataPointSerializer
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        plant_ins = get_object_or_404(Plant, id=kwargs["plant_id"])

        return JsonResponse({"success": True}, status=status.HTTP_200_OK)
