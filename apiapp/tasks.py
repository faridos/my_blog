import time
from datetime import timedelta, date
from django.conf import settings
from django.db import transaction

from .models import Plant, DataPoint, MonthlyReport, YearlyReport
from coreapp.celery_app import app as celery_app
import logging
from .utils import *
from .serializers import DataPointSerializer
from .services import get_data_ms
import datetime
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)
TODAY = datetime.date.today()


@celery_app.task
def do_some_queries():
    time.sleep(10)
    return Plant.objects.count()


@celery_app.task
def query_ms_every_day_test():
    """
    every day this script run, it is enabled through settings Key: CELERY_BEAT_SCHEDULE
    """
    plants = Plant.objects.filter(id=1)
    print(plants[0])
    # for plant in plants:
    res = get_data_ms(plants[0].id)
    if isinstance(res, list):
        data_list = get_organized_data(plants[0].id, res)
        return data_list
    else:
        return {'error': "Grand mama is angry!"}


@celery_app.task
def query_ms_every_day():
    """
    every day this script run, it is enabled through settings Key: CELERY_BEAT_SCHEDULE
    """
    plants = Plant.objects.all()
    for plant in plants:
        res = get_data_ms(plant.id)
        if isinstance(res, list):
            data_list = get_organized_data(plant.id, res)
            res = create_data_points_task(plant.id, data_list)
            return res
        else:
            return {"is_data": False}  # if no data, nothing to do


@celery_app.task
def create_data_points_task(plant_id, data_list=None):
    if data_list is None:
        data_list = []
    with transaction.atomic():
        try:
            plant_ins = Plant.objects.get(id=plant_id)
            create_list, update_list = get_update_create_data_to_save(plant_id, data_list)
            list__create_objs = [DataPoint(plant=plant_ins, **values) for values in create_list]
            # 5. apply bulk_create & bulk_update
            created_records = DataPoint.objects.bulk_create(
                list__create_objs, batch_size=1000
            )

            DataPoint.objects.bulk_update(
                [
                    DataPoint(pk=values.get("id"),  # bulk_update works with pk, not id.
                              energy_expected=values.get("energy_expected"),
                              energy_observed=values.get("energy_observed"),
                              irradiation_expected=values.get("irradiation_expected"),
                              irradiation_observed=values.get("irradiation_observed"),
                              )
                    for values in update_list
                ],
                ["energy_expected", "energy_observed", "irradiation_expected", "irradiation_observed"],
                batch_size=1000
            )
            return {"success": DataPointSerializer(created_records, many=True).data}
        except:
            # just finish the task with failure result
            return {"error": "something weird happened when collecting data for this plant id: %s" % plant_id}


CONCERNED_FIELDS = {'energy_expected': 0, 'energy_observed': 0, 'irradiation_expected': 0, 'irradiation_observed': 0}


@celery_app.task
def run_monthly_report_generator():
    """
    this periodic task runs first of the month , se we query data of previous month
    collect sum of all CONCERNED_FIELDS in Datapoint for each solar plant
    """
    plants = Plant.objects.all()
    list_objs = []

    date_previous_month = date.today() - timedelta(1 * 365 / 12)
    for plant in plants:
        queryset = DataPoint.objects.filter(
            Q(plant=plant, data_date__year=date_previous_month.year, data_date__month=date_previous_month.month))
        # if no queryset, we must fill it with default 0 values
        if not queryset:
            list_objs.append(MonthlyReport(
                **{'plant': plant, 'data_month': date_previous_month.month, 'data_year': date_previous_month.year,
                   **CONCERNED_FIELDS}))
            continue
        sum_data = queryset.aggregate(energy_expected=Sum('energy_expected'),
                                      energy_observed=Sum('energy_observed'),
                                      irradiation_expected=Sum('irradiation_expected'),
                                      irradiation_observed=Sum('irradiation_observed'))
        list_objs.append(MonthlyReport(
            **{'plant': plant, 'data_month': date_previous_month.month, 'data_year': date_previous_month.year,
               **sum_data}))
    MonthlyReport.objects.bulk_create(
        list_objs, batch_size=1000
    )


@celery_app.task
def run_yearly_report_generator():
    """
        this periodic task runs first of the year , se we query data of previous year
        collect sum of all CONCERNED_FIELDS in MonthlyReport for each solar plant
        """
    last_year = (datetime.datetime.now() - relativedelta(years=1)).date().year

    plants = Plant.objects.all()
    list_objs = []
    for plant in plants: # TODO better not do this brute solution, make query on every iteration :/
        queryset = MonthlyReport.objects.filter(Q(plant=plant, data_year=last_year))
        # if no queryset, we must fill it with default 0 values
        if not queryset:
            list_objs.append(MonthlyReport(
                **{'plant': plant, 'data_year': TODAY.year,
                   **CONCERNED_FIELDS}))
            continue

        sum_data = queryset.aggregate(energy_expected=Sum('energy_expected'),
                                      energy_observed=Sum('energy_observed'),
                                      irradiation_expected=Sum('irradiation_expected'),
                                      irradiation_observed=Sum('irradiation_observed'))
        list_objs.append(MonthlyReport(**{'plant': plant, 'data_year': TODAY.year, **sum_data}))
    YearlyReport.objects.bulk_create(
        list_objs, batch_size=1000
    )


@celery_app.task
def run_monthly_report_generator_pdf(pdf_file_name):
    pass


@celery_app.task
def run_yearly_report_generator_pdf(pdf_file_name):
    pass
