import time
from datetime import timedelta, date
from .models import Plant, DataPoint
from coreapp.celery_app import app as celery_app
from .utils import *
from django.conf import settings

TODAY = date.today().isoformat()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()


@celery_app.task
def do_some_queries():
    time.sleep(10)
    return Plant.objects.count()


@celery_app.task
def query_ms_every_day():
    """
    every day this script run, it is enabled through settings Key: CELERY_BEAT_SCHEDULE
    """
    plants = Plant.objects.all()
    for plant in plants:
        res_raw = get_data_ms(settings.MONITORING_SERVICE_URL, plant.id)
        res = json.loads(res_raw.content)
        if isinstance(res, list):
            data_list = get_organized_data(plant.id, res)
        else:
            return
        print(data_list)


@celery_app.task
def query_ms_every_day2():
    """
    every day this script run, it is enabled through settings Key: CELERY_BEAT_SCHEDULE
    """
    plants = Plant.objects.all()
    for plant in plants:
        res_raw = get_data_ms(settings.MONITORING_SERVICE_URL, plant.id)
        res = json.loads(res_raw.content)
        if isinstance(res, list):
            data_list = get_organized_data(plant.id, res)
        else:
            return


@celery_app.task
def create_data_points_task(plant_id, data_list=None):
    if data_list is None:
        data_list = []
    try:
        plant_ins = Plant.objects.get(id=plant_id)
    except:
        # just finish the task with failure result
        return {"error": "no solar plant found with this id: %s" % plant_id}
    create_list, update_list = get_update_create_data_to_save(data_list)
    list__create_objs = [DataPoint(plant=plant_ins, **values) for values in create_list]
    # 5. apply bulk_create & bulk_update
    created_records = DataPoint.objects.bulk_create(
        list__create_objs, batch_size=1000
    )

    DataPoint.objects.bulk_update(
        [
            DataPoint(id=values.get("id"),
                      energy_expected=values.get("energy_expected"),
                      energy_oberved=values.get("energy_oberved"),
                      irradiation_expected=values.get("irradiation_expected"),
                      irradiation_observed=values.get("irradiation_observed"),
                      )
            for values in update_list
        ],
        ["energy_expected", "energy_observed", "irradiation_expected", "irradiation_observed"],
        batch_size=1000
    )
