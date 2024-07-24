import pandas as pd
from libs.data_service import DataService
from libs.data_connector import DataConnector

# Mock implementation of the DataConnector interface for testing
class MockDataConnector(DataConnector):
    def connect(self):
        """
        Mock implementation of the connect method.
        """
        pass

    def fetch_data(self):
        """
        Mock implementation of the fetch_data method.

        Returns a DataFrame with sample data.
        """
        return pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie']
        })

    def close(self):
        """
        Mock implementation of the close method.
        """
        pass


def test_data_service_process_data(mocker):
    """
    Test case for DataService's process_data method.

    This test case checks if the process_data method correctly processes data from a DataConnector.

    A mock DataConnector is created using pytest-mock. The mock's methods are set to return specific values for testing.

    The DataService is initialized with the mock DataConnector and the process_data method is called.

    The calls to the mock's methods are verified to ensure that they are called correctly.

    The result of the process_data method is verified to match the expected data.
    """
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