# libs/connector_factory.py

from libs.csv_connector import CSVConnector
from libs.postgres_connector import PostgresConnector

class ConnectorFactory:
    """
    A factory class for creating data connectors.

    This class provides a static method `get_connector` that creates and returns a data connector based on the provided configuration.

    The configuration should be a dictionary that contains a 'type' key, which specifies the type of connector to create ('csv' or 'postgres'), and other keys that provide the necessary information for creating the connector.

    If the 'type' key is 'csv', the configuration should also contain a 'location' key that specifies the location of the CSV file.

    If the 'type' key is 'postgres', the configuration should also contain a 'connection' key that is a dictionary with the following keys: 'host', 'password', 'port', 'dbname', and 'query'.
    """

    @staticmethod
    def get_connector(config):
        """
        Creates and returns a data connector based on the provided configuration.

        Parameters:
        config (dict): The configuration for creating the data connector.

        Returns:
        DataConnector: The created data connector.

        Raises:
        ValueError: If the 'type' key in the configuration is not 'csv' or 'postgres'.
        """
        connector_type = config['type']

        if connector_type == 'csv':
            return CSVConnector(config['location'])
        elif connector_type == 'postgres':
            return PostgresConnector(config['connection']['host'],
                                     config['connection']['password'],
                                     config['connection']['host'],
                                     config['connection']['port'],
                                     config['connection']['dbname'],
                                     config['connection']['query'])
        else:
            raise ValueError(f"Unsupported connector type: {connector_type}")