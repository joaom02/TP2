import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from utils.reader import CSVReader
from entities.city import City
from entities.job import Job
from entities.company import Company


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
        jobs = self._reader.read_entities(
            attr="Name",
            builder=lambda row: Job(row["Name"])
        )

        # read companies

        def after_creating_company(company, row):
            # add the player to the appropriate team
            jobs[row["Name"]].add_company(company)

        self._reader.read_entities(
            attr="Company",
            builder=lambda row: Company(
                name=row["Company"],
                city=cities[row["City"]],
                summary=row["Summary"]
            ),
            after_create=after_creating_company
        )

        # generate the final xml
        root_el = ET.Element("JobDataset")

        jobs_el = ET.Element("Jobs")
        for job in jobs.values():
            jobs_el.append(job.to_xml())

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
        root_el.append(jobs_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

