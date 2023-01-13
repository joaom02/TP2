import uuid
from datetime import datetime


class City:
    def __init__(self, name, id, latitude, longitude, created_on=None, updated_on=None):
        self.id = id or uuid.uuid4()
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()
