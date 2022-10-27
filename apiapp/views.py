from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.conf import settings
from rest_framework import status
from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .serializers import PlantSerializer, DataPointSerializer, DataPointRawSerializer
from .models import Plant, DataPoint
from .utils import *
from .services import get_data_ms
from .tasks import create_data_points_task

MONITORING_SERVICE_URL = settings.MONITORING_SERVICE_URL


class DataPointCreateView(generics.CreateAPIView):
    """
    API for pulling and saving data from monitoring service
    1. get MS data using get_data_ms service
    2. reorganize the data in order to save it in Backend DB
    3. send the data ( assumed to be a lot to process) to a celery task
    4. send task_id if result is not ready and fetch the result using another api , otherwise send task_result

    """
    serializer_class = DataPointRawSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        plant_ins = get_object_or_404(Plant, id=kwargs["plant_id"])
        res = get_data_ms(plant_ins.id, from_date=kwargs["from_date"], to_date=kwargs["to_date"])
        if isinstance(res, dict) and "error" in res:
            return JsonResponse(res)
        data_list = get_organized_data(plant_ins.id, res)
        # do the job in queries
        res = create_data_points_task.delay(plant_ins.id, data_list)
        # if pulled data are created and ready , i return it,
        # otherwise just return the task_id and result will be fetched via another api : check_result_task
        new_data = res.get() if res.ready() else None
        res_context = (
            {"task_result": DataPointSerializer(new_data, many=True).data, }
            if new_data is not None
            else {"task_id": res.task_id, "message": "data will be available soon"}
        )
        return JsonResponse(res_context, status=status.HTTP_200_OK)


class PlantViewSet(viewsets.ModelViewSet):
    """
    APIs for CRUD a Solar plant; the simplest way  to use is a viewset, no complications here
    """
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()


@api_view(['GET', ])
def check_result_task(request, task_id):
    """
    API For checking on a specfic task to get its result : created DataPoints records
    :param request:
    :param task_id:

    """
    task = AsyncResult(task_id)  # TODO test & check  me
    if task.ready() and not task.get()["success"]:
        return JsonResponse({"task_result": None})
    return JsonResponse({"task_result": DataPointSerializer(task.get(), many=True).data if task.ready() else None})
