from Downloader import Donwloader
from Database import Database
from tqdm import tqdm
import os, glob, csv
import matplotlib.pyplot as plt

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

    def __insert_into_database_dht(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            line_count = 0
            dht_rows = []
            for row in reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    dht_rows.append((row[5], row[6], row[7]))
                    # print(f'\t{row[6]} --- {row[7]} --- {row[5]}')
                    line_count += 1
            self.db.insert_dht(dht_rows)
                
        return line_count
                        
    def __insert_into_database_sds(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            line_count = 0
            sds_rows = []
            for row in reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}', len(row))
                    line_count += 1
                else:
                    sds_rows.append((row[5], row[6], row[9]))
                    # print(f'\t{row[6]} --- {row[9]} --- {row[5]}')
                    line_count += 1

            self.db.insert_sds(sds_rows)

        return line_count


    def start_evaluation(self, start_date, end_date):
        stemp_min = self.db.minimum_of_temperature(start_date, end_date)
        stemp_avg = self.db.average_of_temperature(start_date, end_date)
        stemp_max = self.db.maximum_of_temperature(start_date, end_date)
        temps_min, tdates_min = self.db.minimum_of_temperature_per_day(start_date, end_date)
        temps_avg, tdates_avg = self.db.average_of_temperature_per_day(start_date, end_date)
        temps_max, tdates_max = self.db.maximum_of_temperature_per_day(start_date, end_date)        
        
        ###
        
        shumi_min = self.db.minimum_of_humidity(start_date, end_date)
        shumi_avg = self.db.average_of_humidity(start_date, end_date)
        shumi_max = self.db.maximum_of_humidity(start_date, end_date)
        humis_min, hdates_min = self.db.minimum_of_humidity_per_day(start_date, end_date)
        humis_avg, hdates_avg = self.db.average_of_humidity_per_day(start_date, end_date)
        humis_max, hdates_max = self.db.maximum_of_humidity_per_day(start_date, end_date)
        
        ###
        
        sp1_min = self.db.minimum_of_particle1(start_date, end_date)
        sp1_avg = self.db.average_of_particle1(start_date, end_date)
        sp1_max = self.db.maximum_of_particle1(start_date, end_date)
        p1_min, p1dates_min = self.db.minimum_of_particle1_per_day(start_date, end_date)
        p1_avg, p1dates_avg = self.db.average_of_particle1_per_day(start_date, end_date)
        p1_max, p1dates_max = self.db.maximum_of_particle1_per_day(start_date, end_date)
        
        ###
        
        sp2_min = self.db.minimum_of_particle2(start_date, end_date)
        sp2_avg = self.db.average_of_particle2(start_date, end_date)
        sp2_max = self.db.maximum_of_particle2(start_date, end_date)
        p2_min, p2dates_min = self.db.minimum_of_particle2_per_day(start_date, end_date)
        p2_avg, p2dates_avg = self.db.average_of_particle2_per_day(start_date, end_date)
        p2_max, p2dates_max = self.db.maximum_of_particle2_per_day(start_date, end_date)
        
#########################################################################################################

        figure, axis = plt.subplots(4, 2) 
        
        axis[0,0].bar([10], [stemp_min], color="r", label="Min")
        axis[0,0].bar([20], [stemp_max], color="g", label="Max")
        axis[0,0].bar([30], [stemp_avg], color="b", label="Avg")
        axis[0,0].set_title("Combined Temperature over time")
        axis[0,0].legend()
        
        axis[1,0].plot(tdates_min, temps_min, color="r", label="Min")
        axis[1,0].plot(tdates_max, temps_max, color="g", label="Max")
        axis[1,0].plot(tdates_avg, temps_avg, color="b", label="Avg")
        axis[1,0].set_title("Temperature over time")      
        axis[1,0].legend()
        
        ###
        
        axis[0,1].bar([10], [shumi_min], color="r", label="Min")
        axis[0,1].bar([20], [shumi_max], color="g", label="Max")
        axis[0,1].bar([30], [shumi_avg], color="b", label="Avg")
        axis[0,1].set_title("Combined Humidity over time")
        axis[0,1].legend()
        
        axis[1,1].plot(hdates_min, humis_min, color="r", label="Min")
        axis[1,1].plot(hdates_max, humis_max, color="g", label="Max")
        axis[1,1].plot(hdates_avg, humis_avg, color="b", label="Avg")
        axis[1,1].set_title("Humidity over time")
        axis[1,1].legend()
        
        ###
        
        axis[2,0].bar([10], [sp1_min], color="r", label="Min")
        axis[2,0].bar([20], [sp1_max], color="g", label="Max")
        axis[2,0].bar([30], [sp1_avg], color="b", label="Avg")
        axis[2,0].set_title("Combined Particle 1 over time")
        axis[2,0].legend()
        
        axis[3,0].plot(p1dates_min, p1_min, color="r", label="Min")
        axis[3,0].plot(p1dates_max, p1_max, color="g", label="Max")
        axis[3,0].plot(p1dates_avg, p1_avg, color="b", label="Avg")
        axis[3,0].set_title("Particle 1 over time")
        axis[3,0].legend()
        
        ###
        
        axis[2,1].bar([10], [sp2_min], color="r", label="Min")
        axis[2,1].bar([20], [sp2_max], color="g", label="Max")
        axis[2,1].bar([30], [sp2_avg], color="b", label="Avg")
        axis[2,1].set_title("Combined Particle 2 over time")
        axis[2,1].legend()
        
        axis[3,1].plot(p2dates_min, p2_min, color="r", label="Min")
        axis[3,1].plot(p2dates_max, p2_max, color="g", label="Max")
        axis[3,1].plot(p2dates_avg, p2_avg, color="b", label="Avg")
        axis[3,1].set_title("Particle 2 over time")
        axis[3,1].legend()
        
        # axis[1].xlabel("Date") 
        # axis[1].ylabel("Temperature") 
        
        plt.autoscale()
        
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        
        plt.tight_layout()
        plt.show()
        
