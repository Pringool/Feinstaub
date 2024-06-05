import os
import sqlite3
import datetime

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


class Database:
    def __init__(self) -> None:
        self.__con = sqlite3.connect(os.path.join(os.getcwd(), "Database/feinstaubstation.sqlite3"), detect_types=sqlite3.PARSE_DECLTYPES)
        self.__cur = self.__con.cursor()
        self.__create_database()
    
    def __create_database(self):
        self.__cur.execute(CREATE_SDS)
        self.__cur.execute(CREATE_DHT)
        self.__con.commit()
 
    def insert_sds(self, sqltuple:list[tuple[str, float, float]]):
        self.__cur.executemany("INSERT INTO sds011(date, p1, p2) VALUES(?,?,?)",sqltuple) 
        self.__con.commit()
        
    def insert_dht(self, sqltuple:list[tuple[str, float, float]]):
        self.__cur.executemany("INSERT INTO dht22(date, temperature, humidity) VALUES(?,?,?)",sqltuple)
        self.__con.commit()

    def get_all_data_from_sds(self) -> list:
        self.__cur.execute("SELECT date, p1, p2, entry_id FROM sds011;")
        return self.__cur.fetchall()

    def get_all_data_from_dht(self) -> list:
        self.__cur.execute("SELECT date, temperature, humidity, entry_id FROM dht22;")
        return self.__cur.fetchall()

    def minimum_of_temperature(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MIN(temperature),2) FROM dht22 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def average_of_temperature(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(AVG(temperature),2) FROM dht22 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def maximum_of_temperature(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MAX(temperature),2) FROM dht22 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]   
 
    def minimum_of_humidity(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MIN(humidity),2) FROM dht22 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def average_of_humidity(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(AVG(humidity),2) FROM dht22 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def maximum_of_humidity(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MAX(humidity),2) FROM dht22 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0] 
      
    def minimum_of_particle1(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MIN(p1),2) FROM sds011 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def average_of_particle1(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(AVG(p1),2) FROM sds011 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def maximum_of_particle1(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MAX(p1),2) FROM sds011 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0] 

    def minimum_of_particle2(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MIN(p2),2) FROM sds011 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def average_of_particle2(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(AVG(p2),2) FROM sds011 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0]
        
    def maximum_of_particle2(self, start_date:datetime.date, end_date:datetime.date):
        self.__cur.execute("SELECT ROUND(MAX(p2),2) FROM sds011 WHERE date BETWEEN ? AND ?", (start_date, end_date))
        results = self.__cur.fetchone()
        return results[0] 
    
########## Per day #############

    def minimum_of_temperature_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MIN(temperature),2) FROM dht22 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def average_of_temperature_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(AVG(temperature),2) FROM dht22 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def maximum_of_temperature_per_day(self, start_date:datetime.date, end_date:datetime.date):#
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MAX(temperature),2) FROM dht22 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
    
    def minimum_of_humidity_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MIN(humidity),2) FROM dht22 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def average_of_humidity_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(AVG(humidity),2) FROM dht22 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def maximum_of_humidity_per_day(self, start_date:datetime.date, end_date:datetime.date):#
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MAX(humidity),2) FROM dht22 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
    
    def minimum_of_particle1_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MIN(p1),2) FROM sds011 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def average_of_particle1_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(AVG(p1),2) FROM sds011 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def maximum_of_particle1_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MAX(p1),2) FROM sds011 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
  
    def minimum_of_particle2_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MIN(p2),2) FROM sds011 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def average_of_particle2_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(AVG(p2),2) FROM sds011 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates
        
    def maximum_of_particle2_per_day(self, start_date:datetime.date, end_date:datetime.date):
        current_date = start_date
        current_end_date = current_date + datetime.timedelta(days=1)
        results = []
        dates = []
        for _ in range(abs((end_date - start_date).days)):
            self.__cur.execute("SELECT ROUND(MAX(p2),2) FROM sds011 WHERE date BETWEEN ? AND ?", (current_date, current_end_date))
            result = self.__cur.fetchone()
            results.append(result[0])
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
            current_end_date += datetime.timedelta(days=1)
        return results, dates

