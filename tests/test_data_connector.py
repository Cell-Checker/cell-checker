import pytest
from libs.data_connector import DataConnector

def test_data_connector_cannot_be_instantiated():
    with pytest.raises(TypeError, match="Can't instantiate abstract class DataConnector with abstract methods close, connect, fetch_data"):
        DataConnector()

def test_partial_implementation_cannot_be_instantiated():
    class IncompleteConnector(DataConnector):
        def connect(self):
            pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteConnector with abstract methods close, fetch_data"):
        IncompleteConnector()

def test_complete_implementation_can_be_instantiated():
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
