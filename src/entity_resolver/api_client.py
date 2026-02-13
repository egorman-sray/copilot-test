"""API client for resolving company entity identifiers."""

import os
import requests
from typing import Optional


class ResolveAPIError(Exception):
    """Exception raised when the resolve API request fails."""
    pass


class ResolveAPIClient:
    """Client for the entity resolve API service."""

    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize the API client.

        Args:
            api_url: The URL of the resolve API service. If not provided,
                    uses RESOLVE_API_URL environment variable or default.
        """
        self.api_url = api_url or os.environ.get(
            "RESOLVE_API_URL", "http://localhost:8080/api/resolve"
        )

    def resolve(self, identifier: str) -> dict:
        """
        Resolve a company entity identifier.

        Args:
            identifier: The company entity identifier to resolve.

        Returns:
            A dictionary containing the resolved identifier information.

        Raises:
            ResolveAPIError: If the API request fails.
        """
        try:
            response = requests.post(
                self.api_url,
                json={"identifier": identifier},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ResolveAPIError(f"Failed to resolve identifier: {e}") from e
