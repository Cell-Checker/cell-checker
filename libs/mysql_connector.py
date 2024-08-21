from sqlalchemy import create_engine
from sqlalchemy import text

import pandas as pd
from libs.data_connector import DataConnector


class MySQLConnector(DataConnector):
    """
    A class used to represent a Mysql Data Connector.

    This class is responsible for connecting to a Mysql database, fetching data from it, and closing the connection.

    Attributes:
    connection_string (str): The connection string for the Mysql database.
    engine (Engine): The SQLAlchemy engine for the Mysql database.
    connection (Connection): The SQLAlchemy connection to the Mysql database.
    query (str): The SQL query to execute on the Mysql database.

    Methods:
    connect(): Opens the connection to the Mysql database.
    fetch_data(): Executes the SQL query on the Mysql database, fetches the result into a DataFrame, and returns it.
    close(): Closes the connection to the Mysql database.
    """

    query: object

    def __init__(self, host, port, username, password, dbname, query):
        """
        Constructs all the necessary attributes for the PostgresConnector object.

        Parameters:
        username (str): The username for the Mysql database.
        password (str): The password for the Mysql database.
        host (str): The host of the Mysql database.
        port (str): The port of the Mysql database.
        dbname (str): The name of the Mysql database.
        query (str): The SQL query to execute on the Mysql database.
        """
        DATABASE_TYPE = 'mysql'
        DBAPI = 'mysqlconnector'  # Use 'pymysql' if using PyMySQL


        self.connection_string = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{dbname}')
        print(self.connection_string)
        self.engine = create_engine(self.connection_string)
        self.connection = None
        self.query = query

    def connect(self):
        """
        Opens the connection to the Mysql database.

        Prints a message indicating that the connection to the Mysql database is being opened.
        """
        self.connection = self.engine.connect()

    def fetch_data(self):
        """
        Executes the SQL query on the Mysql database, fetches the result into a DataFrame, and returns it.

        Returns:
        DataFrame: The result of the SQL query.

        Raises:
        Exception: If the connection to the Mysql database is not open.
        """
        if not self.connection:
            raise Exception("Connection is not established. Call connect() method first.")
        result = self.connection.execute(text(self.query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    def close(self):
        """
        Closes the connection to the Mysql database.

        Prints a message indicating that the connection to the Mysql database is being closed and sets the connection attribute to None.
        """
        if self.connection:
            self.connection.close()