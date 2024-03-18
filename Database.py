import os
import sqlite3

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
 
