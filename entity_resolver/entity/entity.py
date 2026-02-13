"""Entity models for the entity resolver."""

from dataclasses import dataclass


@dataclass
class EntityIdentifier:
    """Represents a company entity identifier to be resolved."""

    value: str
    type: str = "unknown"


@dataclass
class ResolvedEntity:
    """Represents a resolved company entity."""

    original_identifier: str
    resolved_identifier: str
    entity_type: str
    confidence: float = 1.0
