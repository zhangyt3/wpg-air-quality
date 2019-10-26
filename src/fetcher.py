import logging
import datetime
import json

import requests

from model.MeasurementModel import MeasurementModel
from model.LocationModel import LocationModel


log = logging.getLogger()
log.setLevel(logging.INFO)

BASE = 'https://winnipeg-aq-sta.sensorup.com/v1.0'
LOCATIONS = f'{BASE}/Locations'

def fetch(event, context):
    log.info("Fetching new air quality data")
    response = requests.get(LOCATIONS).json()
 
    locations = []
    for item in response['value']:
        name = item['name']
        latitude = float(item['location']['coordinates'][0])
        longitude = float(item['location']['coordinates'][1])

        datastreams = get_datastreams(item)
        measurement_link, unit = find_pm25_stream(datastreams)

        if not measurement_link:
            log.warn(f"No PM2.5 measurements for {name}")
        else:
            log.info(f"{name} -  Making GET to {measurement_link}")

            value, time = get_measurement(measurement_link)
            if value != None:
                log.info(f"The newest PM2.5 measurement for {name} is {value} {unit}")

                m = MeasurementModel(
                    location=name,
                    sk=time,
                    value=value,
                    unit=unit
                )
                m.save()

                l = LocationModel(
                    location = name,
                    sk="LOCATION",
                    latitude=latitude,
                    longitude=longitude
                )
                l.save()

    return {
        "statusCode": 200,
        "body": json.dumps({})
    }

def get_datastreams(item):
    """
    Make some requests to retrieve the datastreams for a location.
    """
    thing = requests.get(item['Things@iot.navigationLink']).json()
    return requests.get(thing['value'][0]['Datastreams@iot.navigationLink']).json()

def find_pm25_stream(datastreams):
    """
    Scan through datastreams to find the PM2.5 stream.
    """
    for stream in datastreams['value']:
        if stream['name'].split(':')[-1] == 'PM2.5':
            measurement_link = stream['Observations@iot.navigationLink']
            unit = stream['unitOfMeasurement']['symbol']
            return measurement_link, unit
    return None, None

def get_measurement(link: str, cutoff_days: int = 7):
    """
    Retrieve latest measurement, if it is not too old.
    """
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days = cutoff_days)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    log.info(cutoff)
    response = requests.get(
        link,
        params={
            '$filter': f'phenomenonTime ge {cutoff}',
            '$orderby': 'phenomenonTime desc',
            '$top': '1'
        }
    ).json()

    if 'errorId' in response:
        log.warning(f"Code: {response['code']}, Message: {response['message']}")
        return None, None
    elif 'value' not in response or not response['value']:
        log.warning(f"No new measurements in the past {cutoff_days} from {link}")
        return None, None
    
    return int(response['value'][0]['result']), response['value'][0]['phenomenonTime']     
