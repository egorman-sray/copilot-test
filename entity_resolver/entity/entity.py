"""Entity models for the entity resolver."""

from dataclasses import dataclass
from enum import Enum


class IdentifierType(str, Enum):
    """Valid entity identifier types."""

    CUSIP = "CUSIP"
    ISIN = "ISIN"
    SEDOL = "SEDOL"
    SRAY_ENTITY_ID = "SRAY_ENTITY_ID"
    ASSET_ID = "ASSET_ID"
    FS_ENTITY_ID = "FS_ENTITY_ID"
    ENTITY_ID = "ENTITY_ID"
    FIGI = "FIGI"
    TICKER_EXCHANGE = "TICKER_EXCHANGE"
    LEI = "LEI"
    SERIES_ID = "SERIES_ID"


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
