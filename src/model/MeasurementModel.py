from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class MeasurementModel(Model):
    """
    A single measurement.
    """
    class Meta:
        table_name = "Measurements"

    location = UnicodeAttribute(hash_key=True)
    # sk set to current time
    sk = UnicodeAttribute(range_key=True)
    value = NumberAttribute()
    unit = UnicodeAttribute()
