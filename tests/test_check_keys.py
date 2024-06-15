import sys
import os

# Add the parent directory to sys.path to ensure modules can be imported correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs.check_keys import check_keys_in_list

def test_valid_file():
    """
    Test case where all required keys are present.

    This test case checks if the function `check_keys_in_list` correctly identifies when all required keys are present in a dictionary.

    The dictionary `test_case` contains all the required keys. The function `check_keys_in_list` is expected to return True and None, indicating that all required keys are present and no keys are missing.
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

    This test case checks if the function `check_keys_in_list` correctly identifies when some required keys are missing from a dictionary.

    The dictionary `test_case` is missing the key 'name'. The function `check_keys_in_list` is expected to return False and the set {'name'}, indicating that not all required keys are present and the key 'name' is missing.
    """
    # Example test case missing some keys
    test_case = {'source': {'type': 'csv', 'location': './data.csv'},
                 'target': {'type': 'csv', 'location': './data.csv'},
                 'comparison_rules': {'row_count': 'equal', 'exact_match': 'exact'}}

    required_keys = {'name', 'target', 'source', 'comparison_rules'}

    result, missing_keys = check_keys_in_list(test_case, required_keys)

    assert result == False
    assert missing_keys == {'name'}