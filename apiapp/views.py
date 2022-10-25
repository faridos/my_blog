from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlantSerializer, DataPointSerializer
from .models import Plant, DataPoint
from .utils import *
from .tasks import create_data_points_task

MONITORING_SERVICE_URL = settings.MONITORING_SERVICE_URL


class DataPointCreateView(generics.CreateAPIView):
    """
    API for pulling and saving data from monitoring service

    """
    serializer_class = DataPointSerializer
    permission_classes = ()

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            kwargs["many"] = True

        return super(DataPointCreateView, self).get_serializer(self.request.data, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        plant_ins = get_object_or_404(Plant, id=kwargs["plant_id"])
        res = get_data_ms(MONITORING_SERVICE_URL, plant_ins.id)
        if isinstance(res, dict) and "error" in res:
            return res
        data_list = get_organized_data(plant_ins.id, res)
        create_data_points_task.delay(plant_ins.id, data_list)
        return Response({"data will be available soon", }, status=status.HTTP_200_OK)


class PlantViewSet(viewsets.ModelViewSet):
    """
    APIs for CRUD a Solar plant; the si,plest zqw is to use q viewset
    """
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()
