import pytest
from durable.lang import post, get_host

# Import the rules to ensure they are loaded
import libs.comparison_rules  # Ensure this import correctly references your rules module

def test_equal_row_count():
    """
    Test case for comparing row counts where the source and target have equal row counts.

    This test case checks if the rule 'equal_row_count' correctly identifies when the source and target have equal row counts.

    The source and target both have 1 row. The rule 'equal_row_count' is expected to return True, indicating that the source and target have equal row counts.
    """
    # Test case for comparing row counts
    session_id = 'test_equal_row_count'
    source = [{'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'}]
    target = [{'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'}]
    dfs = dict(rule='equal_row_count', source=source, target=target, sid=session_id)

    # Post the fact to the ruleset
    post('comparison_rules', dfs)

    # Retrieve the updated state from the ruleset
    state = get_host().get_state('comparison_rules', session_id)

    # Assert that the result is set correctly in the state
    assert state.get('result') == True


def test_unequal_row_count():
    """
    Test case for comparing row counts where the source and target have unequal row counts.

    This test case checks if the rule 'equal_row_count' correctly identifies when the source and target have unequal row counts.

    The source has 1 row and the target has 2 rows. The rule 'equal_row_count' is expected to return False, indicating that the source and target do not have equal row counts.
    """
    # Test case for comparing row counts with unequal lengths
    session_id = 'test_unequal_row_count'
    source = [{'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'}]
    target = [
        {'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'},
        {'id': 2, 'key': 'ecoatm-mobile-android', 'name': 'ECOATM APP - ANDROID'}
    ]
    dfs = dict(rule='equal_row_count', source=source, target=target, sid=session_id)

    # Post the fact to the ruleset
    post('comparison_rules', dfs)

    # Retrieve the updated state from the ruleset
    state = get_host().get_state('comparison_rules', session_id)

    # Assert that the result is set correctly in the state
    assert state.get('result') == False