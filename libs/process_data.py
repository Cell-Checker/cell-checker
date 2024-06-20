import numpy as np
from libs.connector_factory import ConnectorFactory
from libs.data_service import *

def process_data(test_case):
    """
    This function processes the data based on the source and target specified in the test case.

    Parameters:
    test_case (dict): The test case dictionary containing 'source' and 'target' keys.

    Returns:
    tuple: A tuple containing two data frames - source_df and target_df.
    """
    source_connector = ConnectorFactory.get_connector(test_case['test']['source'])
    target_connector = ConnectorFactory.get_connector(test_case['test']['target'])
    source_df = DataService(source_connector).process_data()
    target_df = DataService(target_connector).process_data()
    return source_df, target_df