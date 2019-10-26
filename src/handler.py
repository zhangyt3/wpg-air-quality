import json

from model.MeasurementModel import MeasurementModel


LOCATIONS = ["River East", "St. Boniface #2", "St. James East", "Transcona #2"]

def air_quality(event, context):
    """
    Just queries the database for the latest measurements and returns them.
    """
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

    body = {
        'measurements': measurements
    }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

