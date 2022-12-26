import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from utils.reader import CSVReader
from entities.city import City
from entities.company import Company
from entities.job import Job


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        # read cities
        cities = self._reader.read_entities(
            attr="City",
            builder=lambda row: City(str(row["City"]).split(",")[0])
        )

        # read jobs
        companies = self._reader.read_entities(
            attr="Company",
            builder=lambda row: Company(
                name=row["Company"],
                rating=row["Ratings"]
                ),
        )

        # read companies

        def after_creating_job(job, row):
            # add the player to the appropriate team
            companies[row["Company"]].add_job(job)

        self._reader.read_entities(
            attr="Name",
            builder=lambda row: Job(
                name=row["Name"],
                city=cities[row["City"]],
                summary=row["Summary"]
            ),
            after_create=after_creating_job
        )

        # generate the final xml
        root_el = ET.Element("JobDataset")

        companies_el = ET.Element("Companies")
        for company in companies.values():
            companies_el.append(company.to_xml())

        cities_el = ET.Element("Cities")
        citycheck = []
        for city in cities.values():
            cd = city
            cd = str(cd).split(",")
            cd = cd[0]
            if cd not in citycheck:
                cities_el.append(city.to_xml())
                citycheck.append(cd)

        root_el.append(cities_el)
        root_el.append(companies_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

