from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
import random

PULL_DATA_URL = reverse('apiapp:pull_data_ms')
MONITORING_SERVICE_URL = settings.MONITORING_SERVICE_URL


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

    def setUp(self):
        self.client = APIClient()

    def test_needed_params(self):
        """Test Monitoring service response  if it's  list of json objects/dictio"""

        plant_ins = Plant.objects.get_or_create(id=1, defaults=dummy_plant())
        res = self.client.get(PULL_DATA_URL)
        print(type(res))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(type(res), dict)
