import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from libs.connector_factory import ConnectorFactory
from libs.data_service import DataService
from libs.process_data import *  # Replace with your actual module name


@pytest.fixture
def mock_csv_connector():
    # Mock CSV connector
    mock_connector = MagicMock()
    mock_connector.fetch_data.return_value = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie']
    })
    return mock_connector


@pytest.fixture
def mock_postgres_connector():
    # Mock PostgreSQL connector
    mock_connector = MagicMock()
    mock_connector.fetch_data.return_value = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie']
    })
    return mock_connector


def test_process_data_with_csv(mock_csv_connector):
    # Mock ConnectorFactory to return mock_csv_connector for both source and target
    with patch.object(ConnectorFactory, 'get_connector', return_value=mock_csv_connector):
        test_case = {
            'test': {
                'source': {'type': 'csv', 'location': '/path/to/source.csv'},
                'target': {'type': 'csv', 'location': '/path/to/target.csv'}
            }
        }
        source_df, target_df = process_data(test_case)

        assert isinstance(source_df, pd.DataFrame)
        assert isinstance(target_df, pd.DataFrame)
        assert not source_df.empty
        assert not target_df.empty
        # Add more assertions based on expected data frame content


def test_process_data_with_postgres(mock_postgres_connector):
    # Mock ConnectorFactory to return mock_postgres_connector for both source and target
    with patch.object(ConnectorFactory, 'get_connector', return_value=mock_postgres_connector):
        test_case = {
            'test': {
                'source': {'type': 'postgres', 'connection': {...}},
                'target': {'type': 'postgres', 'connection': {...}}
            }
        }
        source_df, target_df = process_data(test_case)

        assert isinstance(source_df, pd.DataFrame)
        assert isinstance(target_df, pd.DataFrame)
        assert not source_df.empty
        assert not target_df.empty
        # Add more assertions based on expected data frame content

# Add more test cases as needed for different scenarios (e.g., mixed CSV and PostgreSQL sources)
