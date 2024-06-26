import pytest
from libs.data_connector import DataConnector

def test_data_connector_cannot_be_instantiated():
    """
    Test case for attempting to instantiate the abstract DataConnector class.

    This test case checks if a TypeError is raised when attempting to instantiate the abstract DataConnector class, which should not be possible.

    The expected error message is "Can't instantiate abstract class DataConnector with abstract methods close, connect, fetch_data".
    """
    with pytest.raises(TypeError, match="Can't instantiate abstract class DataConnector with abstract methods close, connect, fetch_data"):
        DataConnector()

def test_partial_implementation_cannot_be_instantiated():
    """
    Test case for attempting to instantiate a class that partially implements the DataConnector interface.

    This test case checks if a TypeError is raised when attempting to instantiate a class that only partially implements the DataConnector interface, which should not be possible.

    The expected error message is "Can't instantiate abstract class IncompleteConnector with abstract methods close, fetch_data".
    """
    class IncompleteConnector(DataConnector):
        def connect(self):
            pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteConnector with abstract methods close, fetch_data"):
        IncompleteConnector()

def test_complete_implementation_can_be_instantiated():
    """
    Test case for attempting to instantiate a class that fully implements the DataConnector interface.

    This test case checks if a class that fully implements the DataConnector interface can be instantiated, which should be possible.

    The class CompleteConnector is defined to implement all abstract methods of the DataConnector interface. An instance of CompleteConnector is created and the methods are called to verify that they work as expected.
    """
    class CompleteConnector(DataConnector):
        def connect(self):
            pass

        def fetch_data(self):
            return "data"

        def close(self):
            pass

    connector = CompleteConnector()
    assert connector.connect() is None
    assert connector.fetch_data() == "data"
    assert connector.close() is None