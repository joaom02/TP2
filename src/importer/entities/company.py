import xml.etree.ElementTree as ET


class Company:

    def __init__(self, name, city):
        Company.counter += 1
        self._id = Company.counter
        self._name = name
        self._city = city

    def to_xml(self):
        el = ET.Element("Company")
        el.set("name", self._name)
        el.set("city_ref", str(self._city.get_id()))
        return el

    def __str__(self):
        return f"{self._name}, country:{self._country}"


Company.counter = 0
