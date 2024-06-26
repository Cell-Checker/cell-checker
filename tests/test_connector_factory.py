import pytest
from libs.connector_factory import ConnectorFactory

def test_get_csv_connector(mocker):
    """
    Test case for getting a CSV connector.

    This test case checks if the factory method correctly creates a CSV connector when given a configuration for a CSV connector.

    The configuration specifies that the connector type is 'csv' and provides the location of the CSV file.

    The CSVConnector class is mocked to verify that it is called with the correct arguments and to control its behavior for the test.

    The factory method is expected to return the mock CSVConnector instance.
    """
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
    """
    Test case for getting a PostgreSQL connector.

    This test case checks if the factory method correctly creates a PostgreSQL connector when given a configuration for a PostgreSQL connector.

    The configuration specifies that the connector type is 'postgres' and provides the connection details for the PostgreSQL database.

    The PostgresConnector class is mocked to verify that it is called with the correct arguments and to control its behavior for the test.

    The factory method is expected to return the mock PostgresConnector instance.
    """
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
    """
    Test case for getting a connector with an invalid type.

    This test case checks if the factory method correctly raises a ValueError when given a configuration for an unsupported connector type.

    The configuration specifies that the connector type is 'invalid_type', which is not a supported connector type.

    The factory method is expected to raise a ValueError with a message indicating that the connector type is unsupported.
    """
    config = {
        'type': 'invalid_type'
    }

    with pytest.raises(ValueError, match="Unsupported connector type: invalid_type"):
        ConnectorFactory.get_connector(config)