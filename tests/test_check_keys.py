import sys
import os

# Add the parent directory to sys.path to ensure modules can be imported correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs.check_keys import check_keys_in_list


def test_valid_file():
    """
    Test case where all required keys are present.
    """
    # Example test case with all required keys
    test_case = {'name': 'Simple Test',
                 'source': {'type': 'csv', 'location': './data.csv'},
                 'target': {'type': 'csv', 'location': './data.csv'},
                 'comparison_rules': {'row_count': 'equal', 'exact_match': 'exact'}}

    required_keys = {'name', 'target', 'source', 'comparison_rules'}

    result, missing_keys = check_keys_in_list(test_case, required_keys)

    assert result == True
    assert missing_keys is None


def test_missing_keys():
    """
    Test case where some required keys are missing.
    """
    # Example test case missing some keys
    test_case = {'source': {'type': 'csv', 'location': './data.csv'},
                 'target': {'type': 'csv', 'location': './data.csv'},
                 'comparison_rules': {'row_count': 'equal', 'exact_match': 'exact'}}

    required_keys = {'name', 'target', 'source', 'comparison_rules'}

    result, missing_keys = check_keys_in_list(test_case, required_keys)

    assert result == False
    assert missing_keys == {'name'}
