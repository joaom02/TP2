import xml.etree.ElementTree as ET

from entities.job import Job

class Company:

    def __init__(self, name: str, rating: str):
        Company.counter += 1
        self._id = Company.counter
        self._name = name
        self._jobs = []
        self._rating = rating

    def add_job(self, job: Job):
        self._jobs.append(job)


    def to_xml(self):
        el = ET.Element("Company")
        el2 = ET.Element("Name")
        el1 = ET.Element("Rating")
        el.set("id", str(self._id))
        el2.text = self._name
        el1.text = self._rating
        el.append(el2)
        el.append(el1)

        jobs_el = ET.Element("Jobs")
        for job in self._jobs:
            jobs_el.append(job.to_xml())

        el.append(jobs_el)

        return el

    def __str__(self):
        return f"{self._name} ({self._id})"


Company.counter = 0
