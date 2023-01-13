import uuid
from datetime import datetime


class Job:
    def __init__(self, name, id, summary, created_on=None, updated_on=None):
        self.id = id or uuid.uuid4()
        self.name = name
        self.summary = summary
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()