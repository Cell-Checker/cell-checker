import pytest
import pandas as pd
from libs.data_service import DataService
from libs.data_connector import DataConnector


class MockDataConnector(DataConnector):
    def connect(self):
        pass

    def fetch_data(self):
        return pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie']
        })

    def close(self):
        pass


def test_data_service_process_data(mocker):
    # Create a mock connector using pytest-mock
    mock_connector = mocker.Mock(spec=DataConnector)

    # Define the behavior of the mock's methods
    mock_connector.fetch_data.return_value = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie']
    })

    # Initialize DataService with the mock connector
    data_service = DataService(mock_connector)

    # Call process_data
    result = data_service.process_data()

    # Verify the connector methods are called correctly
    mock_connector.connect.assert_called_once()
    mock_connector.fetch_data.assert_called_once()
    mock_connector.close.assert_called_once()

    # Assert the result is as expected
    expected_data = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie']
    })
    pd.testing.assert_frame_equal(result, expected_data)
