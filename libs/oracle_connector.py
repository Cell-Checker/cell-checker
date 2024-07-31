from sqlalchemy import create_engine
from sqlalchemy import text
import oracledb as oracledb
oracledb.init_oracle_client(lib_dir=r"C:\instantclient_21_14")


import pandas as pd
from libs.data_connector import DataConnector
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv(override=True)


class OracleConnector(DataConnector):
    """
    A class used to represent a OracleSQL Data Connector.

    This class is responsible for connecting to a OracleSQL database, fetching data from it, and closing the connection.

    Attributes:
    connection_string (str): The connection string for the OracleSQL database.
    engine (Engine): The SQLAlchemy engine for the OracleSQL database.
    connection (Connection): The SQLAlchemy connection to the OracleSQL database.
    query (str): The SQL query to execute on the OracleSQL database.

    Methods:
    connect(): Opens the connection to the OracleSQL database.
    fetch_data(): Executes the SQL query on the OracleSQL database, fetches the result into a DataFrame, and returns it.
    close(): Closes the connection to the OracleSQL database.
    """

    query: object
    # access environment variables
    username = os.getenv('ORACLE_USERNAME')
    password = os.getenv('ORACLE_PASSWORD')
    host = os.getenv('ORACLE_HOST')
    port = os.getenv('ORACLE_PORT')
    sid = os.getenv('ORACLE_SID')
    query = os.getenv('QUERY')

    def __init__(self, username, password, host, port, sid, query):
        """
        Constructs all the necessary attributes for the OracleConnector object.

        Parameters:
        username (str): The username for the OracleSQL database.
        password (str): The password for the OracleSQL database.
        host (str): The host of the OracleSQL database.
        port (str): The port of the OracleSQL database.
        sid (str): The sid of the OracleSQL database.
        query (str): The SQL query to execute on the OracleSQL database.
        """

        self.connection_string = f'oracle+oracledb://{os.getenv("ORACLE_USERNAME")}:{os.getenv("ORACLE_PASSWORD")}@{os.getenv("ORACLE_HOST")}:{os.getenv("ORACLE_PORT")}/{os.getenv("ORACLE_SID")}'
        print(self.connection_string)
        self.engine = create_engine(self.connection_string)
        self.connection = None
        self.query = os.getenv("QUERY")

    def connect(self):
        """
        Opens the connection to the OracleSQL database.

        Prints a message indicating that the connection to the OracleSQL database is being opened.
        """
        self.connection = self.engine.connect()


    def fetch_data(self):
        """
        Executes the SQL query on the OracleSQL database, fetches the result into a DataFrame, and returns it.

        Returns:
        DataFrame: The result of the SQL query.

        Raises:
        Exception: If the connection to the OracleSQL database is not open.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() method first.")
        result = self.connection.execute(text(self.query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    def close(self):
        """
        Closes the connection to the OracleSQL database.

        Prints a message indicating that the connection to the OracleSQL database is being closed and sets the connection attribute to None.
        """
        if self.connection:
            self.connection.close()