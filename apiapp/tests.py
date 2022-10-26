from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
import random
import datetime
import json
import requests
from nose.tools import assert_is_not_none
from unittest.mock import Mock, patch

# from unittest.mock import Mock # needed for mocking the external service api response like Monitoring service
from apiapp.utils import (get_organized_data, get_update_create_data_to_save, get_data_ms_for_test)
from apiapp.models import DataPoint, Plant
from .tasks import create_data_points_task, query_ms_every_day
from .services import get_data_ms

# PULL_DATA_URL = reverse('apiapp:pull_data_ms') # TODO error reverse
MONITORING_SERVICE_URL = settings.MONITORING_SERVICE_URL
TODAY = datetime.date.today()
TEST_SIZE = 10000


class MonitoringServiceTests(TestCase):
    """test access to monitoring service"""

    def setUp(self):
        self.client = APIClient()

    def test_ms_available(self):
        """Test that authentication is required"""
        res = self.client.get(MONITORING_SERVICE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


def get_random_int(length):
    ints = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    result_int = ''.join(random.choice(ints) for iii in range(length))
    return result_int


def dummy_plant():
    # expandable list of fields in Plant Models
    return {
        'name': 'plant_' + get_random_int(4)
    }


class DataPointApiTests(TestCase):
    """test all Datapoint Apis"""
    urls = 'coreapp.urls'

    def setUp(self):
        self.client = APIClient()

    def test_monitoring_service(self):
        """Test Monitoring service availability/response """

        plant_ins = Plant.objects.get_or_create(id=2, defaults=dummy_plant())
        res_raw = get_data_ms_for_test(MONITORING_SERVICE_URL, plant_ins[0].id)

        self.assertEqual(res_raw.status_code, status.HTTP_200_OK)

    def test_pull_and_organize_from_ms(self):
        plant_ins = Plant.objects.get_or_create(id=3, defaults=dummy_plant())
        plant_id = plant_ins[0].id
        res_raw = get_data_ms_for_test(MONITORING_SERVICE_URL, plant_id)
        res = json.loads(res_raw.content)
        if isinstance(res, list):
            data_list = get_organized_data(plant_id, res)
            """
            new_data = [{'plant':3, 'date': 20.12.2022, 'hour': 01, 'irradiation_expected': 123, 'irradiation_observed': 321, 'energy_expected': 123, 'energy_observed': 321 },...]
            """
            assert (len(data_list[0].keys()) == 6)

        else:
            assert "error" in res

    # def dummy_test_create_update_datapoints(self):
    #     """
    #     its tricky here , we need to separate create list from update list and run bulk_create and bulk_update separately
    #
    #     it should be using the api url to get expected result, not like this
    #     :return:
    #     """
    #
    #     # 1. get MS data
    #     plant_ins = Plant.objects.get_or_create(id=4, defaults=dummy_plant())
    #     plant_id = plant_ins[0].id
    #     res_raw = get_data_ms_for_test(MONITORING_SERVICE_URL, plant_id)
    #     res = json.loads(res_raw.content)
    #     # 2. check if error dictionary
    #     if isinstance(res, dict):
    #         print("no data.......")
    #         return
    #     # 3. organize data:
    #     data_list = get_organized_data(plant_id, res)
    #
    #     # 4. separate the create ones from the update ones
    #     create_list, update_list = get_update_create_data_to_save(plant_id, data_list)
    #     list__create_objs = [DataPoint(plant=plant_ins[0], **values) for values in create_list]
    #     # 5. apply bulk_create & bulk_update
    #     created_records = DataPoint.objects.bulk_create(
    #         list__create_objs, batch_size=1000
    #     )
    #     print(created_records)
    #
    #     DataPoint.objects.bulk_update(
    #         [
    #             DataPoint(id=values.get("id"),
    #                       energy_expected=values.get("energy_expected"),
    #                       energy_oberved=values.get("energy_oberved"),
    #                       irradiation_expected=values.get("irradiation_expected"),
    #                       irradiation_observed=values.get("irradiation_observed"),
    #                       )
    #             for values in update_list
    #         ],
    #         ["energy_expected", "energy_observed", "irradiation_expected", "irradiation_observed"],
    #         batch_size=1000
    #     )

    def tttttest_create_update_datapoints2(self):

        plant_ins = Plant.objects.create(name="test_me")
        # data_point_create_url = f"http://localhost:8008/api/pull/{plant_ins.id}/2019-01-01/2019-02-01" # container connection issue
        data_point_create_url = reverse("data_point_create",
                                        kwargs={"plant_id": plant_ins.id, "from": "2019-01-01", "to": "2019-02-01"}
                                        )  # TODO FIXME no reverse match :(

        data = [{"plant": xx,
                 "energy_expected": 7.7612510355724815,
                 "energy_observed": 69.30603384703062,
                 "irradiation_expected": 62.872460771577664,
                 "irradiation_observed": 68.90565707149658,
                 "data_date": str(xx) + "-10-24", "data_hour": "09"}
                for xx in range(2022, 2023)
                ]

        headers = {'Content-Type': "application/json"}
        response = requests.post(
            data_point_create_url,
            data=json.dumps(
                data
            ),
            headers=headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.json()) == TEST_SIZE

    def test_tasks(self):
        assert create_data_points_task.run(1)
        assert create_data_points_task.create_task.run(2)
        assert query_ms_every_day.create_task.run(3)

    @patch('apiapp.services.requests.get')
    def test_getting_ma_data(mock_get):
        # Configure the mock
        mock_get.return_value.ok = True
        # Call the  service to get data, which will send a request to the monitoring server.
        plant_ins = Plant.objects.get_or_create(id=4, defaults=dummy_plant())
        response = get_data_ms(plant_ins[0].id)

        # If  request is sent => then I expect a response.
        assert_is_not_none(response)
