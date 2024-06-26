import pytest
from durable.lang import post, get_host

# Import the rules to ensure they are loaded
import libs.comparison_rules  # Ensure this import correctly references your rules module

def test_matched_rows():
    """
    Test case for comparing rows where the source and target have matched rows.

    This test case checks if the rule 'rows_match' correctly identifies when the source and target have matched rows.

    The source and target both have 1 row with the same data. The rule 'rows_match' is expected to return True, indicating that the source and target have matched rows.
    """
    session_id = 'test_matched_rows'
    source = [{'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'}]
    target = [{'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'}]
    dfs = dict(rule='rows_match', source=source, target=target, sid=session_id)

    # Post the fact to the ruleset
    post('comparison_rules', dfs)

    # Retrieve the updated state from the ruleset
    state = get_host().get_state('comparison_rules', session_id)

    # Assert that the result is set correctly in the state
    assert state.get('result') == True

def test_unmatched_rows():
    """
    Test case for comparing rows where the source and target have unmatched rows.

    This test case checks if the rule 'rows_match' correctly identifies when the source and target have unmatched rows.

    The source and target both have 1 row but with different data. The rule 'rows_match' is expected to return False, indicating that the source and target have unmatched rows.
    """
    session_id = 'test_matched_rows'
    source = [{'id': 1, 'key': 'ecoatm-mobile', 'name': 'ECOATM APP - IOS'}]
    target = [{'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'}]
    dfs = dict(rule='rows_match', source=source, target=target, sid=session_id)

    # Post the fact to the ruleset
    post('comparison_rules', dfs)

    # Retrieve the updated state from the ruleset
    state = get_host().get_state('comparison_rules', session_id)

    # Assert that the result is set correctly in the state
    assert state.get('result') == False


def test_is_not_null():
    """
    Test case for checking if the key is not null in the target.

    This test case checks if the rule 'not_null' correctly identifies when the key is not null in the target.

    The target has 1 row with the key not being null. The rule 'not_null' is expected to return True, indicating that the key is not null in the target.
    """
    session_id = 'test_is_not_null'
    source = [{'id': 1, 'key': 'ecoatm-mobile', 'name': 'ECOATM APP - IOS'}]
    target = [{'id': 1, 'key': 'ecoatm-mobile-ios', 'name': 'ECOATM APP - IOS'}]
    dfs = dict(rule='not_null', source=source, target=target, sid=session_id)

    # Post the fact to the ruleset
    post('comparison_rules', dfs)

    # Retrieve the updated state from the ruleset
    state = get_host().get_state('comparison_rules', session_id)

    # Assert that the result is set correctly in the state
    assert state.get('result') == True

def test_is_null():
    """
    Test case for checking if the key is null in the target.

    This test case checks if the rule 'not_null' correctly identifies when the key is null in the target.

    The target has 1 row with the key being null. The rule 'not_null' is expected to return False, indicating that the key is null in the target.
    """
    session_id = 'test_is_not_null'
    source = [{'id': 1, 'key': 'ecoatm-mobile', 'name': 'ECOATM APP - IOS'}]
    target = [{'id': 1, 'key': None, 'name': 'ECOATM APP - IOS'}]
    dfs = dict(rule='not_null', source=source, target=target, sid=session_id)

    # Post the fact to the ruleset
    post('comparison_rules', dfs)

    # Retrieve the updated state from the ruleset
    state = get_host().get_state('comparison_rules', session_id)

    # Assert that the result is set correctly in the state
    assert state.get('result') == False