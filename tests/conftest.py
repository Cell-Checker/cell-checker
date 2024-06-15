import pytest
from durable.lang import get_host

@pytest.fixture
def rule_engine_state():
    # Fixture to provide a fresh state for each test
    host = get_host()
    host.delete_state('comparison_rules')  # Manually clear the state
    return host
