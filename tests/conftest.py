import pytest
from durable.lang import get_host

@pytest.fixture
def rule_engine_state():
    """
    A pytest fixture that provides a fresh state for each test.

    This fixture creates a new host, deletes any existing state for 'comparison_rules', and returns the host.

    Returns:
    Host: The host with a fresh state.
    """
    # Fixture to provide a fresh state for each test
    host = get_host()
    host.delete_state('comparison_rules')  # Manually clear the state
    return host