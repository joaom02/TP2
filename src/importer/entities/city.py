import xml.etree.ElementTree as ET

nomes = []
class City:

    def __init__(self, name):
        self._name = name
        if self._name not in nomes:
            City.counter += 1
            nomes.append(self._name)
        self._id = City.counter

    def to_xml(self):
        el = ET.Element("City")
        el.set("id", str(self._id))
        el.set("name", self._name)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"


City.counter = 0
