"""Tests for entity models."""

from entity_resolver.entity.entity import EntityIdentifier, ResolvedEntity


def test_entity_identifier_creation() -> None:
    """Test creating an EntityIdentifier."""
    identifier = EntityIdentifier(value="US0378331005", type="ISIN")
    assert identifier.value == "US0378331005"
    assert identifier.type == "ISIN"


def test_entity_identifier_default_type() -> None:
    """Test EntityIdentifier with default type."""
    identifier = EntityIdentifier(value="AAPL")
    assert identifier.value == "AAPL"
    assert identifier.type == "unknown"


def test_resolved_entity_creation() -> None:
    """Test creating a ResolvedEntity."""
    resolved = ResolvedEntity(
        original_identifier="US0378331005",
        resolved_identifier="AAPL",
        entity_type="EQUITY",
        confidence=0.95,
    )
    assert resolved.original_identifier == "US0378331005"
    assert resolved.resolved_identifier == "AAPL"
    assert resolved.entity_type == "EQUITY"
    assert resolved.confidence == 0.95


def test_resolved_entity_default_confidence() -> None:
    """Test ResolvedEntity with default confidence."""
    resolved = ResolvedEntity(
        original_identifier="US0378331005",
        resolved_identifier="AAPL",
        entity_type="EQUITY",
    )
    assert resolved.confidence == 1.0
