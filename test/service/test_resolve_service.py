"""Tests for ResolveService."""

from unittest.mock import Mock, patch

import httpx

from entity_resolver.entity.entity import EntityIdentifier
from entity_resolver.service.resolve_service import ResolveService


def test_resolve_service_initialization() -> None:
    """Test ResolveService initialization."""
    service = ResolveService(
        api_url="https://api.example.com/resolve",
        api_key="test-key",
        timeout=30,
    )
    assert service.api_url == "https://api.example.com/resolve"
    assert service.api_key == "test-key"
    assert service.timeout == 30


def test_resolve_service_strips_trailing_slash() -> None:
    """Test that ResolveService strips trailing slash from URL."""
    service = ResolveService(
        api_url="https://api.example.com/resolve/",
        api_key="test-key",
    )
    assert service.api_url == "https://api.example.com/resolve"


@patch("entity_resolver.service.resolve_service.httpx.Client")
def test_resolve_success(mock_client_class: Mock) -> None:
    """Test successful identifier resolution."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "resolved_identifier": "AAPL",
        "entity_type": "EQUITY",
        "confidence": 0.95,
    }
    mock_response.raise_for_status = Mock()

    mock_client = Mock()
    mock_client.post.return_value = mock_response
    mock_client.__enter__ = Mock(return_value=mock_client)
    mock_client.__exit__ = Mock(return_value=None)
    mock_client_class.return_value = mock_client

    service = ResolveService(
        api_url="https://api.example.com/resolve",
        api_key="test-key",
    )
    identifier = EntityIdentifier(value="US0378331005", type="ISIN")
    resolved = service.resolve(identifier)

    assert resolved is not None
    assert resolved.original_identifier == "US0378331005"
    assert resolved.resolved_identifier == "AAPL"
    assert resolved.entity_type == "EQUITY"
    assert resolved.confidence == 0.95


@patch("entity_resolver.service.resolve_service.httpx.Client")
def test_resolve_http_error(mock_client_class: Mock) -> None:
    """Test resolution with HTTP error."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not Found", request=Mock(), response=mock_response
    )

    mock_client = Mock()
    mock_client.post.return_value = mock_response
    mock_client.__enter__ = Mock(return_value=mock_client)
    mock_client.__exit__ = Mock(return_value=None)
    mock_client_class.return_value = mock_client

    service = ResolveService(
        api_url="https://api.example.com/resolve",
        api_key="test-key",
    )
    identifier = EntityIdentifier(value="INVALID", type="ISIN")
    resolved = service.resolve(identifier)

    assert resolved is None


@patch("entity_resolver.service.resolve_service.httpx.Client")
def test_resolve_request_error(mock_client_class: Mock) -> None:
    """Test resolution with request error."""
    mock_client = Mock()
    mock_client.post.side_effect = httpx.RequestError("Connection failed")
    mock_client.__enter__ = Mock(return_value=mock_client)
    mock_client.__exit__ = Mock(return_value=None)
    mock_client_class.return_value = mock_client

    service = ResolveService(
        api_url="https://api.example.com/resolve",
        api_key="test-key",
    )
    identifier = EntityIdentifier(value="US0378331005", type="ISIN")
    resolved = service.resolve(identifier)

    assert resolved is None


@patch("entity_resolver.service.resolve_service.httpx.Client")
def test_resolve_with_api_key_in_headers(mock_client_class: Mock) -> None:
    """Test that API key is included in request headers."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "resolved_identifier": "AAPL",
        "entity_type": "EQUITY",
    }
    mock_response.raise_for_status = Mock()

    mock_client = Mock()
    mock_client.post.return_value = mock_response
    mock_client.__enter__ = Mock(return_value=mock_client)
    mock_client.__exit__ = Mock(return_value=None)
    mock_client_class.return_value = mock_client

    service = ResolveService(
        api_url="https://api.example.com/resolve",
        api_key="test-key-123",
    )
    identifier = EntityIdentifier(value="US0378331005", type="ISIN")
    service.resolve(identifier)

    mock_client.post.assert_called_once()
    call_kwargs = mock_client.post.call_args[1]
    assert "headers" in call_kwargs
    assert call_kwargs["headers"]["Authorization"] == "Bearer test-key-123"
