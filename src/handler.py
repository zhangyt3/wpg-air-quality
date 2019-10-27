import logging
import json
import jinja2

from model.MeasurementModel import MeasurementModel
from model.LocationModel import LocationModel

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
    templateLoader = jinja2.FileSystemLoader(searchpath="src/templates/")
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        autoescape=jinja2.select_autoescape(['html'])
    )
    template = templateEnv.get_template("default.html")

    markers = []
    measurements = get_measurements()
    for m in measurements:
        name = m['location']
        value = m['measurement']
        latitude, longitude = get_coordinates(name)

        markers.append(f'{latitude},{longitude},{name},{value}')

    page = template.render(markers=markers)
    log.info(page)

    return page

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

