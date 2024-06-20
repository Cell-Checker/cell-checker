from sqlalchemy import create_engine
from sqlalchemy import text

import pandas as pd
from libs.data_connector import *

class PostgresConnector(DataConnector):
    """
    A class used to represent a PostgreSQL Data Connector.

    This class is responsible for connecting to a PostgreSQL database, fetching data from it, and closing the connection.

    Attributes:
    connection_string (str): The connection string for the PostgreSQL database.
    engine (Engine): The SQLAlchemy engine for the PostgreSQL database.
    connection (Connection): The SQLAlchemy connection to the PostgreSQL database.
    query (str): The SQL query to execute on the PostgreSQL database.

    Methods:
    connect(): Opens the connection to the PostgreSQL database.
    fetch_data(): Executes the SQL query on the PostgreSQL database, fetches the result into a DataFrame, and returns it.
    close(): Closes the connection to the PostgreSQL database.
    """

    query: object

    def __init__(self, username, password, host, port, dbname, query):
        """
        Constructs all the necessary attributes for the PostgresConnector object.

        Parameters:
        username (str): The username for the PostgreSQL database.
        password (str): The password for the PostgreSQL database.
        host (str): The host of the PostgreSQL database.
        port (str): The port of the PostgreSQL database.
        dbname (str): The name of the PostgreSQL database.
        query (str): The SQL query to execute on the PostgreSQL database.
        """
        self.connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}'
        self.engine = create_engine(self.connection_string)
        self.connection = None
        self.query = query

    def connect(self):
        """
        Opens the connection to the PostgreSQL database.

        Prints a message indicating that the connection to the PostgreSQL database is being opened.
        """
        self.connection = self.engine.connect()

    def fetch_data(self):
        """
        Executes the SQL query on the PostgreSQL database, fetches the result into a DataFrame, and returns it.

        Returns:
        DataFrame: The result of the SQL query.

        Raises:
        Exception: If the connection to the PostgreSQL database is not open.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() method first.")
        result = self.connection.execute(text(self.query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    def close(self):
        """
        Closes the connection to the PostgreSQL database.

        Prints a message indicating that the connection to the PostgreSQL database is being closed and sets the connection attribute to None.
        """
        if self.connection:
            self.connection.close()