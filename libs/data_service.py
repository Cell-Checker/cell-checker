from libs.data_connector import *

class DataService:
    """
    A class used to represent a Data Service.

    This class is responsible for processing data from a data connector.

    Attributes:
    connector (DataConnector): The data connector to fetch data from.

    Methods:
    process_data(): Connects to the data source, fetches data from it, closes the connection, and returns the fetched data.
    """

    def __init__(self, connector: DataConnector):
        """
        Constructs all the necessary attributes for the DataService object.

        Parameters:
        connector (DataConnector): The data connector to fetch data from.
        """
        self.connector = connector

    def process_data(self):
        """
        Connects to the data source, fetches data from it, closes the connection, and returns the fetched data.

        Returns:
        DataFrame: The data fetched from the data source.
        """
        self.connector.connect()
        dataframe: object = self.connector.fetch_data()
        self.connector.close()
        return dataframe