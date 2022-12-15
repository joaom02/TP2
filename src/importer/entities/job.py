import xml.etree.ElementTree as ET


class Job:

    def __init__(self, name, city, summary):
        Job.counter += 1
        self._id = Job.counter
        self._name = name
        self._city = city
        self._summary = summary

    def to_xml(self):
        el = ET.Element("Job")
        el1 = ET.Element("Summary")
        el2 = ET.Element("Name")
        el3 = ET.Element("City")
        el.set("id", str(self._id))
        el2.text = self._name
        el3.set("ref",str(self._city.get_id()))

        el1.text = self._summary
        el.append(el2)
        el.append(el3)
        el.append(el1)

        return el

    def __str__(self):
        return f"{self._name}, country:{self._city}"


Job.counter = 0
