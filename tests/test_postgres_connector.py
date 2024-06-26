import pytest
from unittest.mock import MagicMock, patch
from libs.postgres_connector import PostgresConnector

@pytest.fixture
def mock_postgres_connector():
    """
    Pytest fixture for creating a mock PostgresConnector.

    This fixture creates a PostgresConnector with test parameters and returns it for use in other test cases.
    """
    connector = PostgresConnector(
        username="test_user",
        password="test_pass",
        host="test_host",
        port="5432",
        dbname="test_db",
        query="SELECT * FROM test_table"
    )
    return connector

# def test_postgres_connector_close(mock_postgres_connector):
#     """
#     Test case for PostgresConnector's close method.
#
#     This test case is currently commented out. When uncommented, it checks if the close method correctly sets the connection attribute to None.
#
#     The PostgresConnector is initialized with a mock connection and the connect method is called.
#
#     The close method is then called and the connection attribute is verified to be None.
#     """
#     # Mock the connection and ensure it's set
#     mock_connection = MagicMock()
#     mock_postgres_connector.connection = mock_connection
#
#     # Patch the connect method to avoid actual connection establishment
#     with patch.object(mock_postgres_connector.engine, 'connect', return_value=mock_connection):
#         mock_postgres_connector.connect()
#
#         # Call close() and assert connection is None
#         mock_postgres_connector.close()
#         assert mock_postgres_connector.connection is None