from concurrent.futures import ThreadPoolExecutor
import os
from tqdm import tqdm
import requests
from calendar import monthrange
import gzip
import shutil

BASE_URL = "http://archive.sensor.community/"

class Downloader:
    def __init__(self, year:int = 2023, month:int = 1, day:int = 1, increment:bool = True, amount:int = 10) -> None:
        self.year = year
        self.increment = increment
        self.imonth = month
        self.iday = day
        self.amount = amount
        self.smonth = ""
        self.sday = ""
        self.leading_year = ""
        if (year < 2023):
            self.leading_year = str(year)+"/"
        # Checks for leading zero
        if self.imonth < 10:
            self.smonth = "0"+str(self.imonth)
        else:
            self.smonth = str(self.imonth)
        if self.iday < 10:
            self.sday = "0"+str(self.iday)
        else:
            self.sday = str(self.iday)
        self.date = str(self.year)+"-"+str(self.smonth)+"-"+str(self.sday)
        self.dates:list[tuple[str,str]] = []
        # if not self.increment or self.amount <= 0 and self.increment:
        #     self.amount = 1
        for _ in range(self.amount+1):
            self.dates.append((self.date, self.leading_year))
            self.__increase_day()
        self.__start_download()
        self.zip_endding = ".gz"

    def __start_download(self):    
        os.mkdir(os.path.join(os.path.dirname(__file__),"tmp"))
        os.mkdir(os.path.join(os.path.dirname(__file__),"tmp","dht"))
        os.mkdir(os.path.join(os.path.dirname(__file__),"tmp","sds"))
        with ThreadPoolExecutor() as executor:
            list(
                tqdm(
                executor.map(self.__save_files_dht, self.dates),
                total=len(self.dates),
                unit=" files",
                desc="DHT Files download"
                ))
            list(
                tqdm(
                executor.map(self.__save_files_sds, self.dates),
                total=len(self.dates),
                unit=" files",
                desc="SDS Files download"
                ))
        shutil.rmtree(os.path.join(os.path.dirname(__file__),"tmp"))
        # print(response.text) # formated
        # print(response.content) # basicaly unformated
    
    def __save_files_dht(self, date):
        if date[1] != "":
            self.__save_dht_gz_files(BASE_URL+date[1]+date[0]+"/"+date[0]+"_dht22_sensor_3660.csv.gz", date[0])
        response_dht = requests.get(BASE_URL+date[1]+date[0]+"/"+date[0]+"_dht22_sensor_3660.csv")
        if response_dht.ok:
            with open(os.path.join(os.path.dirname(__file__),"files","dht",date[0]+"_dht22_sensor_3660.csv"), "w+") as f:
                f.write(response_dht.text)
        return os.path.join(os.path.dirname(__file__),"files","dht",date[0]+"_dht22_sensor_3660.csv")
    
    def __save_files_sds(self, date):
        if date[1] != "":
            self.__save_sds_gz_files(BASE_URL+date[1]+date[0]+"/"+date[0]+"_sds011_sensor_3659.csv.gz", date[0])
        response_sds = requests.get(BASE_URL+date[1]+date[0]+"/"+date[0]+"_sds011_sensor_3659.csv")
        if response_sds.ok:
            with open(os.path.join(os.path.dirname(__file__),"files","sds",date[0]+"_sds011_sensor_3659.csv"), "w+") as f:
                f.write(response_sds.text)
        return os.path.join(os.path.dirname(__file__),"files","sds",date[0]+"_sds011_sensor_3659.csv")

    def __save_dht_gz_files(self, url, date):

        response_dht_gz = requests.get(url)
        if response_dht_gz.ok:
            with open(os.path.join(os.path.dirname(__file__),"tmp","dht",date+"_dht22_sensor_3660.csv.gz"), "wb") as f:
                f.write(response_dht_gz.content)
                # print(response_dht_gz.text)
            self.__unzip_gz(True, date)

    def __save_sds_gz_files(self, url, date):

        response_sds_gz = requests.get(url)
        if response_sds_gz.ok:
            with open(os.path.join(os.path.dirname(__file__),"tmp","sds",date+"_sds011_sensor_3659.csv.gz"), "wb") as f:
                f.write(response_sds_gz.content)
                # print(response_dht_gz.text)
            self.__unzip_gz(False, date)

    def __unzip_gz(self, is_dhp: bool, date):
        if is_dhp:
            with gzip.open(os.path.join(os.path.dirname(__file__),"tmp","dht",date+"_dht22_sensor_3660.csv.gz"), "rb") as g:
                with open(os.path.join(os.path.dirname(__file__),"files","dht",date+"_dht22_sensor_3660.csv"), "w+") as f:
                    for line in g:
                        f.write(line.decode("utf-8"))
        else:
            with gzip.open(os.path.join(os.path.dirname(__file__),"tmp","sds",date+"_sds011_sensor_3659.csv.gz"), "rb") as g:
                with open(os.path.join(os.path.dirname(__file__),"files","sds",date+"_sds011_sensor_3659.csv"), "w+") as f:
                    for line in g:
                        f.write(line.decode("utf-8"))
                        

    def __increase_day(self):
        if self.increment:
            self.iday+=1
            # Check if the day is in the next month and if it is if the month is in the next year
            weekday, day_amount = monthrange(self.year, self.imonth)
            if self.iday > day_amount:
                self.iday = 1
                self.imonth+=1
                if self.imonth > 12:
                    self.year+=1
                    self.imonth = 1
                    if self.year > 2022:
                        self.leading_year = ""
                
            if self.imonth < 10:
                self.smonth = "0"+str(self.imonth)
            else:
                self.smonth = str(self.imonth)
            if self.iday < 10:
                self.sday = "0"+str(self.iday)
            else:
                self.sday = str(self.iday)
            self.date = str(self.year)+"-"+str(self.smonth)+"-"+str(self.sday)

if __name__ == "__main__":
    # downloader = Downloader(amount=2)
    downloader = Downloader(2022,1,1)
    # downloader.save_files()
    # downloader.save_files()
    

