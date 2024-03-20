

class DatabaseDownloderConnector:
    def __init__(self) -> None:
        self.db = Database()


    def download_files(self, year:int, monty:int, day:int, amount:int, increment:bool):
        Donwloader(year, monty, day, increment, amount)

    def delete_files(self):
        pass

    def insert_files_into_database(self):
        pass

    def start_evaluation(self):
        pass
