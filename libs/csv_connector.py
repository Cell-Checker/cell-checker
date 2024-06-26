import pandas as pd
from libs.data_connector import *

class CSVConnector(DataConnector):
    """
    A class used to represent a CSV Data Connector.

    This class is responsible for connecting to a CSV file, fetching data from it, and closing the connection.

    Attributes:
    file_path (str): The path to the CSV file.
    data (DataFrame): The data fetched from the CSV file.

    Methods:
    connect(): Opens the CSV file and prints a message.
    fetch_data(): Reads the CSV file into a DataFrame and returns it.
    close(): Closes the CSV file and prints a message.
    """

    def __init__(self, file_path):
        """
        Constructs all the necessary attributes for the CSVConnector object.

        Parameters:
        file_path (str): The path to the CSV file.
        """
        self.file_path = file_path
        self.data = None

    def connect(self):
        """
        Opens the CSV file and prints a message.

        Prints a message indicating that the CSV file is being opened.
        """
        print(f"Opening CSV file: {self.file_path}")

    def fetch_data(self):
        """
        Reads the CSV file into a DataFrame and returns it.

        Returns:
        DataFrame: The data fetched from the CSV file.
        """
        self.data = pd.read_csv(self.file_path)
        return self.data

    def close(self):
        """
        Closes the CSV file and prints a message.

        Prints a message indicating that the CSV file is being closed and sets the data attribute to None.
        """
        print(f"Closing CSV file: {self.file_path}")
        self.data = None