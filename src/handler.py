import logging
import json
import jinja2

from model.MeasurementModel import MeasurementModel
from model.LocationModel import LocationModel

from render import render

log = logging.getLogger()
log.setLevel(logging.INFO)


LOCATIONS = ["River East", "St. Boniface #2", "St. James East", "Transcona #2"]

def air_quality_raw(event, context):
    """
    Just queries the database for the latest measurements and returns them as JSON.
    """
    body = {
        'measurements': get_measurements()
    }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

def air_quality_map(event, context):
    """
    Renders latest air quality measurements on a map.
    """
    measurements = get_measurements()
    coordinates = dict()
    for m in measurements:
        name = m['location']
        coordinates[name] = get_coordinates(name)

    return render(measurements, coordinates)

def get_coordinates(place):
    res = LocationModel.get(place, "LOCATION")
    return res.latitude, res.longitude

def get_measurements():
    measurements = []
    for name in LOCATIONS:
        res = MeasurementModel.query(
            name,
            limit=1,
            scan_index_forward=False,
            range_key_condition=MeasurementModel.sk.startswith('2')
        )
        latest = res.next()
        
        res = dict()
        res['location'] = latest.location
        res['measurement'] = latest.value
        res['time'] = latest.sk
        res['unit'] = latest.unit

        measurements.append(res)
    
    return measurements

