import os
from dicttoxml import dicttoxml
from Database import Database
from xml.dom.minidom import parseString

db = Database()

sds_xml_list = []
dht_xml_list = []
class Database_Export:
    def __init__(self) -> None:
        self.sds: dict = {}
        self.dht: dict = {}

    class SDS_011:
        def __init__(self, date, p1, p2) -> None:
            self.date = date
            self.p1 = p1
            self.p2 = p2

    class DHT_22:
        def __init__(self, date, temperature, humidity) -> None:
            self.date = date
            self.temperature = temperature
            self.humidity = humidity


sds_data = db.get_all_data_from_sds()

dht_data = db.get_all_data_from_dht()

db_export = Database_Export()

for sds in sds_data:
    db_export.sds[sds[3]] = vars(Database_Export.SDS_011(sds[0], sds[1], sds[2]))

for dht in dht_data:
    db_export.dht[dht[3]] = vars(Database_Export.DHT_22(dht[0],dht[1],dht[2]))

dic = vars(db_export)

xml = dicttoxml(dic, attr_type = False, custom_root = "Database")

dom = parseString(xml)
xml = dom.toprettyxml()
if not os.path.exists(os.path.join(os.path.dirname(__file__), "export")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "export"))
# os.mkdir("./export")
if os.path.exists(os.path.join(os.path.dirname(__file__), "export", "export.xml")):
    os.remove(os.path.join(os.path.dirname(__file__), "export", "export.xml"))
with open(os.path.join(os.path.dirname(__file__), "export", "export.xml"), "w+") as file:
    file.write(xml)
print(xml)
