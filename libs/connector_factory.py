# libs/connector_factory.py

from libs.csv_connector import CSVConnector


class ConnectorFactory:
    @staticmethod
    def get_connector(config):
        print(config)
        connector_type = config['type']

        if connector_type == 'csv':
            return CSVConnector(config['location'])
        else:
            raise ValueError(f"Unsupported connector type: {connector_type}")
