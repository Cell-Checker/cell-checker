import pytest
from libs.connector_factory import ConnectorFactory

def test_get_csv_connector(mocker):
    # Mock the CSVConnector class
    MockCSVConnector = mocker.patch('libs.connector_factory.CSVConnector')
    config = {
        'type': 'csv',
        'location': 'path/to/csv/file.csv'
    }

    # Create an instance of the mock
    instance = MockCSVConnector.return_value

    # Call the factory method
    connector = ConnectorFactory.get_connector(config)

    # Verify that the CSVConnector was called with the correct arguments
    MockCSVConnector.assert_called_once_with('path/to/csv/file.csv')

    # Assert that the factory method returns the mock instance
    assert connector == instance

def test_get_postgres_connector(mocker):
    # Mock the PostgresConnector class
    MockPostgresConnector = mocker.patch('libs.connector_factory.PostgresConnector')
    config = {
        'type': 'postgres',
        'connection': {
            'host': 'localhost',
            'password': 'password',
            'user': 'user',
            'port': 5432,
            'dbname': 'database',
            'query': 'SELECT * FROM table'
        }
    }

    # Create an instance of the mock
    instance = MockPostgresConnector.return_value

    # Call the factory method
    connector = ConnectorFactory.get_connector(config)

    # Verify that the PostgresConnector was called with the correct arguments
    MockPostgresConnector.assert_called_once_with(
        'localhost', 'password', 'localhost', 5432, 'database', 'SELECT * FROM table'
    )

    # Assert that the factory method returns the mock instance
    assert connector == instance

def test_get_connector_invalid_type():
    config = {
        'type': 'invalid_type'
    }

    with pytest.raises(ValueError, match="Unsupported connector type: invalid_type"):
        ConnectorFactory.get_connector(config)
