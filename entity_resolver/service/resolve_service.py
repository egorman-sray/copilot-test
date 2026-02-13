"""Service for resolving entity identifiers via API."""

from typing import Optional

import httpx
import structlog

from entity_resolver.entity.entity import EntityIdentifier, ResolvedEntity

logger = structlog.get_logger(__name__)


class ResolveService:
    """Service for resolving company entity identifiers."""

    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        """Initialize the resolve service.

        Args:
            api_url: The base URL of the resolve API
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        logger.info(
            "ResolveService initialized",
            api_url=self.api_url,
            timeout=self.timeout,
        )

    def resolve(self, identifier: EntityIdentifier) -> Optional[ResolvedEntity]:
        """Resolve an entity identifier.

        Args:
            identifier: The entity identifier to resolve

        Returns:
            ResolvedEntity if successful, None otherwise
        """
        logger.info("Resolving identifier", identifier=identifier.value)

        try:
            with httpx.Client(timeout=self.timeout) as client:
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"

                response = client.post(
                    f"{self.api_url}",
                    json={"identifier": identifier.value, "type": identifier.type},
                    headers=headers,
                )

                response.raise_for_status()
                data = response.json()

                resolved = ResolvedEntity(
                    original_identifier=identifier.value,
                    resolved_identifier=data.get("resolved_identifier", ""),
                    entity_type=data.get("entity_type", "unknown"),
                    confidence=data.get("confidence", 1.0),
                )

                logger.info(
                    "Successfully resolved identifier",
                    original=identifier.value,
                    resolved=resolved.resolved_identifier,
                )

                return resolved

        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP error resolving identifier",
                identifier=identifier.value,
                status_code=e.response.status_code,
                error=str(e),
            )
            return None
        except httpx.RequestError as e:
            logger.error(
                "Request error resolving identifier",
                identifier=identifier.value,
                error=str(e),
            )
            return None
        except Exception as e:
            logger.exception(
                "Unexpected error resolving identifier",
                identifier=identifier.value,
                error=str(e),
            )
            return None
