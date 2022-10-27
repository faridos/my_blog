"""
here we define any call for external services , prepare the response for the caller
"""
# import urljoin in case needed
import requests
import json
from django.conf import settings
from datetime import date, timedelta
from .utils import create_query_params

TODAY = date.today()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()


def get_data_ms(plant_id, from_date=None, to_date=None):
    if from_date and to_date:
        query_params = create_query_params(plant_id, from_date=from_date, to_date=to_date)
    else:
        query_params = create_query_params(plant_id, from_date=YESTERDAY, to_date=TODAY)
    res_raw = requests.get(settings.MONITORING_SERVICE_URL + query_params)
    res = json.loads(res_raw.content)  # always there is a response ok 200, hmmm intresting
    return res
