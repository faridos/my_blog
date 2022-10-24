from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
import random
from apiapp.models import Plant
import datetime
import json
import requests
# PULL_DATA_URL = reverse('apiapp:pull_data_ms')
MONITORING_SERVICE_URL = settings.MONITORING_SERVICE_URL
TODAY = datetime.date.today()


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


def create_dummy_query_params(plant_id):
    thirty_days_ago = TODAY - datetime.timedelta(30)
    query_params = f"?plant-id={plant_id}&from={thirty_days_ago}&to={TODAY}"
    return query_params


class DataPointApiTests(TestCase):
    """test all Datapoint Apis"""

    def setUp(self):
        self.client = APIClient()

    def test_needed_params(self):
        """Test Monitoring service response """

        plant_ins = Plant.objects.get_or_create(id=2, defaults=dummy_plant())
        query_params = create_dummy_query_params(plant_ins[0].id)
        print(MONITORING_SERVICE_URL + query_params)
        # res = self.client.get(MONITORING_SERVICE_URL + query_params)
        res = requests.get('http://monitoring_service:5000/?plant-id=2&from=2022-09-24&to=2022-10-22')
2        # print(json.loads(res).content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
