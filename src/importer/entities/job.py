import xml.etree.ElementTree as ET

from entities.company import Company

class Job:

    def __init__(self, name: str):
        Job.counter += 1
        self._id = Job.counter
        self._name = name
        self._companies = []

    def add_company(self, company: Company):
        self._companies.append(company)

    def to_xml(self):
        el = ET.Element("Job")
        el.set("id", str(self._id))
        el.set("name", self._name)

        companies_el = ET.Element("Companies")
        for company in self._companies:
            companies_el.append(company.to_xml())

        el.append(companies_el)

        return el

    def __str__(self):
        return f"{self._name} ({self._id})"


Job.counter = 0
