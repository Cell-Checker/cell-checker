import pandas as pd
from libs.data_connector import *


class CSVConnector(DataConnector):

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def connect(self):
        print(f"Opening CSV file: {self.file_path}")

    def fetch_data(self):
        self.data = pd.read_csv(self.file_path)
        return self.data

    def close(self):
        print(f"Closing CSV file: {self.file_path}")
        self.data = None
