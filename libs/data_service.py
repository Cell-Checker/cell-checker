from libs.data_connector import *


class DataService:

    def __init__(self, connector: DataConnector):
        self.connector = connector

    def process_data(self):
        self.connector.connect()
        dataframe: object = self.connector.fetch_data()
        self.connector.close()
        return dataframe