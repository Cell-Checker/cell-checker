from sqlalchemy import create_engine
from sqlalchemy import text

import pandas as pd
from libs.data_connector import *

class PostgresConnector(DataConnector):

    query: object

    def __init__(self, username, password, host, port, dbname, query):
        self.connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}'
        print(self.connection_string)
        self.engine = create_engine(self.connection_string)
        self.connection = None
        self.query = query

    def connect(self):
        self.connection = self.engine.connect()

    def fetch_data(self):
        if not self.connection:
            raise Exception("Connection is not established. Call connect() method first.")
        result = self.connection.execute(text(self.query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    def close(self):
        if self.connection:
            self.connection.close()
