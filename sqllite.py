import sqlite3
import requests
import os

import gzip
import shutil

con = sqlite3.connect("data.db")
cur = con.cursor()

CREATE_SDS = """
CREATE TABLE IF NOT EXISTS sds011(
    entry_id INTEGER PRIMARY KEY NOT NULL,
    date DATETIME,
    p1 REAL,
    p2 REAL
)
"""
CREATE_DHT = """
CREATE TABLE IF NOT EXISTS dht22(
    entry_id INTEGER PRIMARY KEY NOT NULL,
    date DATETIME,
    temperature REAL,
    humidity REAL
)
"""

insert_into_SDS = """ 
INSERT INTO sds011(date, p1, p2)  VALUES(?, ?, ?)
"""

insert_into_DHT = """ 
INSERT INTO dht22(date, temperature, humidity)  VALUES(?, ?, ?)
"""

select_SDS = """ 
SELECT date, p1, p2 FROM sds011 ORDER BY date
"""

select_DHT= """ 
SELECT date, temperature, humidity FROM dht22 ORDER BY date
"""

cur.execute(CREATE_SDS)
cur.execute(CREATE_DHT)
con.commit()


data1 = [
    ("2024-03-06 14:20:31.278405", 43, 7.9),
    ("2023-02-05 13:20:31.278405", 53, 7.5),
    ("2022-01-03 12:20:31.278405", 28, 8.0),
]

data2 = [
    ("2024-03-06 14:20:31.278405", 43, 7.9),
    ("2023-02-05 13:20:31.278405", 53, 7.5),
    ("2022-01-03 12:20:31.278405", 28, 8.0),
]

""" cur.executemany(insert_into_SDS, data1)
con.commit()

cur.executemany(insert_into_DHT, data2)
con.commit()
 """
""" for row in cur.execute(select_SDS):
    print(row)
    
for row in cur.execute(select_DHT):
    print(row) """
    
def __save_files_dht():
        response_dht = requests.get("http://archive.sensor.community/2022/2022-01-01/2022-01-01_dht22_sensor_3660.csv.gz")
        if response_dht.ok:
            with open(os.path.join(os.path.dirname(__file__),"files","dht","2022"+"_dht22_sensor_3660.csv.gz"), "w+") as f:
                f.write(response_dht.text)
        return os.path.join(os.path.dirname(__file__),"files","dht","2022"+"_dht22_sensor_3660.csv.gz")    
  
""" def extract(gz_file, extracted_file):
  with gzip.open(gz_file, 'rb') as f_in:
      with open(extracted_file, 'wb') as f_out:
          print(f_in,f_out)
          shutil.copyfileobj(f_in, f_out) """

def __unzip_gz(is_dhp: bool, date):
    if is_dhp:
        with gzip.open(os.path.join(os.path.dirname(__file__),"files","dht",date+"_dht22_sensor_3660.csv.gz"), "rb") as g:
            with open(os.path.join(os.path.dirname(__file__),"files","dht",date+"_dht22_sensor_3660.csv"), "w+") as f:
                for line in g:
                    f.write(line.decode("utf-8"))
    else:
        with gzip.open(os.path.join(os.path.dirname(__file__),"tmp","sds",date+"_sds011_sensor_3659.csv.gz"), "rb") as g:
            with open(os.path.join(os.path.dirname(__file__),"files","sds",date+"_sds011_sensor_3659.csv"), "w+") as f:
                for line in g:
                    f.write(line.decode("utf-8"))

data = __save_files_dht()   

__unzip_gz(True,"2022")

