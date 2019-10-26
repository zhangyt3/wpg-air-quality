from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class LocationModel(Model):
    """
    A location: name, latitude, longitude.
    """
    class Meta:
        table_name = "Measurements"
    
    location = UnicodeAttribute(hash_key=True)
    # sk always set to "LOCATION"
    sk = UnicodeAttribute(range_key=True) 
    latitude = NumberAttribute()
    longitude = NumberAttribute()
