"""Shared test fixtures."""

import pytest


@pytest.fixture
def sample_identifier() -> str:
    """Fixture providing a sample identifier."""
    return "US0378331005"


@pytest.fixture
def sample_resolved_data() -> dict[str, str]:
    """Fixture providing sample resolved entity data."""
    return {
        "resolved_identifier": "AAPL",
        "entity_type": "EQUITY",
    }
