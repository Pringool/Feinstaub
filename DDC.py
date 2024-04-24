from Downloader import Donwloader
from Database import Database
from tqdm import tqdm
import os, glob, csv


class DatabaseDownloderConnector:
    def __init__(self) -> None:
        self.db = Database()
        self.dht_filenames: list[str] = []
        self.sds_filenames: list[str] = []

    def download_files(self, year:int, monty:int, day:int, amount:int, increment:bool):
        Donwloader(year, monty, day, increment, amount)
        for filename in glob.glob(os.path.join(os.getcwd(),"files","dht","*.csv")):
            self.dht_filenames.append(filename)        
            
        for filename in glob.glob(os.path.join(os.getcwd(),"files","sds","*.csv")):
            self.sds_filenames.append(filename)

    def delete_files(self):
        if len(self.dht_filenames) <= 0:
            for filename in glob.glob(os.path.join(os.getcwd(),"files","dht","*.csv")):
                self.dht_filenames.append(filename)        

        if len(self.sds_filenames) <= 0:
            for filename in glob.glob(os.path.join(os.getcwd(),"files","sds","*.csv")):
                self.sds_filenames.append(filename)
            
            
        for file in self.dht_filenames:
            if os.path.exists(file):
                os.remove(file)
        for file in self.sds_filenames:
            if os.path.exists(file):
                os.remove(file)     

    def insert_files_into_database(self):
        if len(self.dht_filenames) <= 0:
            for filename in glob.glob(os.path.join(os.getcwd(),"files","dht","*.csv")):
                self.dht_filenames.append(filename)        

        if len(self.sds_filenames) <= 0:
            for filename in glob.glob(os.path.join(os.getcwd(),"files","sds","*.csv")):
                self.sds_filenames.append(filename)
        list(
            tqdm(
            map(self.__insert_into_database_dht, self.dht_filenames),
            total=len(self.dht_filenames),
            unit=" Files",
            desc="DHT Insert",
            colour="green"
            ))
        list(
            tqdm(
            map(self.__insert_into_database_sds, self.sds_filenames),
            total=len(self.sds_filenames),
            unit=" Files",
            desc="SDS Insert",
            colour="blue"
            ))     
        

    def start_evaluation(self):
        pass
