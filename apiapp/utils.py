from django.conf import settings
import datetime
from apiapp.models import DataPoint
import requests
import json
TODAY = datetime.date.today()


def get_data_ms(url, plant_id):
    query_params = create_query_params(plant_id)
    res_raw = requests.get(url + query_params)
    res = json.loads(res_raw.content)
    return res


def create_query_params(plant_id):
    thirty_days_ago = TODAY - datetime.timedelta(30)
    query_params = f"?plant-id={plant_id}&from={thirty_days_ago}&to={TODAY}"
    return query_params


def get_it_splitted(data_datetime):
    # TODO data format from monitoring service: "2019-01-01T00:00:00", what if  format got changed??
    data_date = data_datetime.split('T')[0]
    data_hour = data_datetime.split('T')[1].split(":")[0]
    return {'data_date': data_date, 'data_hour': data_hour}


def get_organized_data(plant_id, ms_data=None):
    """
     organise data of a specific plant
    :param ms_data: a list : [
      {
        "datetime": "2019-01-01T00:00:00",
        "expected": {
          "energy": 87.55317774223157,
          "irradiation": 98.19878838432548
        },
        "observed": {
          "energy": 90.78559770167864,
          "irradiation": 30.085498370965905
        }
        },...]
    :return: new_data : a list of dictionaries of object like this :
                          {'date': 20.12.2022, 'hour': 01,
                          'irradiation_expected': 123, 'irradiation_observed': 321,
                          'energy_expected': 123, 'energy_observed': 321
                          }
    """
    if ms_data is None:
        ms_data = []
    new_data = []
    # assuming we know the structure of the MS response,
    # TODO needs refactoring when fields mapping is needed
    for data_row in ms_data:

        data_obj = {}
        date_time_dict = get_it_splitted(data_row['datetime'])
        data_obj['energy_expected'] = data_row['expected']['energy']
        data_obj['energy_observed'] = data_row['observed']['energy']
        data_obj['irradiation_expected'] = data_row['expected']['irradiation']
        data_obj['irradiation_observed'] = data_row['observed']['irradiation']
        data_obj.update(date_time_dict)
        new_data.append(data_obj)
    return new_data


def get_update_create_data_to_save(organized_data=None):
    if organized_data is None:
        organized_data = []
    records = [
        {
            "id": DataPoint.objects.filter(
                plant=record.get("plant"),
                data_date=record.get("data_date"),
                data_hour=record.get("data_hour")
            )
                .first()
                .id
            if DataPoint.objects.filter(
                plant=record.get("plant"),
                data_date=record.get("data_date"),
                data_hour=record.get("data_hour")
            ).first()
               is not None
            else None,
            **record,
        }
        for record in organized_data
    ]
    records_to_update = []
    records_to_create = []

    [
        records_to_update.append(record)
        if record["id"] is not None
        else records_to_create.append(record)
        for record in records
    ]

    [record.pop("id") for record in records_to_create]

    return records_to_create, records_to_update
