"""Tests for the API client."""

import pytest
import responses
from entity_resolver.api_client import ResolveAPIClient


class TestResolveAPIClient:
    """Test cases for ResolveAPIClient."""

    def test_init_with_custom_url(self):
        """Test initialization with custom API URL."""
        client = ResolveAPIClient(api_url="https://example.com/api")
        assert client.api_url == "https://example.com/api"

    def test_init_with_default_url(self):
        """Test initialization with default API URL."""
        client = ResolveAPIClient()
        assert client.api_url == "http://localhost:8080/api/resolve"

    @responses.activate
    def test_resolve_success(self):
        """Test successful identifier resolution."""
        responses.add(
            responses.POST,
            "http://localhost:8080/api/resolve",
            json={
                "resolved_identifier": "RESOLVED123",
                "company_name": "Test Company",
                "status": "active"
            },
            status=200
        )

        client = ResolveAPIClient()
        result = client.resolve("COMPANY123")

        assert result["resolved_identifier"] == "RESOLVED123"
        assert result["company_name"] == "Test Company"
        assert result["status"] == "active"

    @responses.activate
    def test_resolve_api_error(self):
        """Test handling of API errors."""
        responses.add(
            responses.POST,
            "http://localhost:8080/api/resolve",
            json={"error": "Not found"},
            status=404
        )

        client = ResolveAPIClient()
        with pytest.raises(Exception) as exc_info:
            client.resolve("INVALID123")

        assert "Failed to resolve identifier" in str(exc_info.value)

    @responses.activate
    def test_resolve_with_custom_url(self):
        """Test resolution with custom API URL."""
        responses.add(
            responses.POST,
            "https://custom.example.com/resolve",
            json={"resolved_identifier": "CUSTOM123"},
            status=200
        )

        client = ResolveAPIClient(api_url="https://custom.example.com/resolve")
        result = client.resolve("TEST123")

        assert result["resolved_identifier"] == "CUSTOM123"
