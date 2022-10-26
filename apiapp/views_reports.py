from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .serializers import PlantSerializer, DataPointSerializer
from .models import Plant, DataPoint
from .utils import *
from .services import get_data_ms
from .tasks import create_data_points_task


class MonthlyReportsCreateView(generics.CreateAPIView):
    """
     API to get the reports of high consuming energy plants in the last x months,  grouped by months

    """
    serializer_class = DataPointSerializer
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        plant_ins = get_object_or_404(Plant, id=kwargs["plant_id"])

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


