import xml.etree.ElementTree as ET


class Company:

    def __init__(self, name, city, summary):
        Company.counter += 1
        self._id = Company.counter
        self._name = name
        self._city = city
        self._summary = summary

    def to_xml(self):
        el = ET.Element("Company")
        el.set("id", self._id)
        el.set("name", self._name)
        el.set("city_ref", str(self._city.get_id()))
        el.set("summary", self._summary)
        return el

    def __str__(self):
        return f"{self._name}, country:{self._city}"


Company.counter = 0
