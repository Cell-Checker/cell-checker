import pytest
import pandas as pd
from libs.csv_connector import CSVConnector

def test_csv_connector_connect(capsys):
    """
    Test case for CSVConnector's connect method.

    This test case checks if the connect method correctly prints a message indicating that the CSV file is being opened.

    The CSVConnector is initialized with a dummy file path and the connect method is called.

    The printed message is captured and verified to match the expected output.
    """
    # Initialize the CSVConnector with a dummy file path
    connector = CSVConnector('dummy/path/to/file.csv')

    # Call the connect method
    connector.connect()

    # Capture the print output
    captured = capsys.readouterr()

    # Verify the printed message
    assert captured.out == "Opening CSV file: dummy/path/to/file.csv\n"

def test_csv_connector_fetch_data(mocker):
    """
    Test case for CSVConnector's fetch_data method.

    This test case checks if the fetch_data method correctly reads data from a CSV file.

    The pd.read_csv function is mocked to return sample data.

    The CSVConnector is initialized with a dummy file path and the fetch_data method is called.

    The result is verified to match the sample data.
    """
    # Sample data to be returned by the mock
    sample_data = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie']
    })

    # Mock the pd.read_csv function to return the sample data
    mock_read_csv = mocker.patch('pandas.read_csv', return_value=sample_data)

    # Initialize the CSVConnector with a dummy file path
    connector = CSVConnector('dummy/path/to/file.csv')

    # Call the fetch_data method
    result = connector.fetch_data()

    # Verify that pd.read_csv was called with the correct file path
    mock_read_csv.assert_called_once_with('dummy/path/to/file.csv')

    # Assert that the result matches the sample data
    pd.testing.assert_frame_equal(result, sample_data)

def test_csv_connector_close(capsys):
    """
    Test case for CSVConnector's close method.

    This test case checks if the close method correctly prints a message indicating that the CSV file is being closed and sets the data attribute to None.

    The CSVConnector is initialized with a dummy file path and the close method is called.

    The printed message is captured and verified to match the expected output.

    The data attribute is verified to be None.
    """
    # Initialize the CSVConnector with a dummy file path
    connector = CSVConnector('dummy/path/to/file.csv')

    # Call the close method
    connector.close()

    # Capture the print output
    captured = capsys.readouterr()

    # Verify the printed message
    assert captured.out == "Closing CSV file: dummy/path/to/file.csv\n"

    # Verify that the data attribute is set to None
    assert connector.data is None