# libs/connector_factory.py

from libs.csv_connector import CSVConnector
from libs.postgres_connector import PostgresConnector

class ConnectorFactory:
    @staticmethod
    def get_connector(config):
        print(config)
        connector_type = config['type']

        if connector_type == 'csv':
            return CSVConnector(config['location'])
        elif connector_type == 'postgres':
            return PostgresConnector(config['connection']['host'],
                                     config['connection']['password'],
                                     config['connection']['host'],
                                     config['connection']['port'],
                                     config['connection']['dbname'],
                                     config['query'])
        else:
            raise ValueError(f"Unsupported connector type: {connector_type}")
