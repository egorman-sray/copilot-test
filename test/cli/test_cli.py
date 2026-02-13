"""Tests for CLI interface."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from entity_resolver.cli.cli import resolve
from entity_resolver.entity.entity import ResolvedEntity


def test_cli_resolve_success() -> None:
    """Test successful CLI resolution."""
    runner = CliRunner()

    with patch("entity_resolver.cli.cli.ResolveService") as mock_service_class:
        mock_service = Mock()
        mock_resolved = ResolvedEntity(
            original_identifier="US0378331005",
            resolved_identifier="AAPL",
            entity_type="EQUITY",
        )
        mock_service.resolve.return_value = mock_resolved
        mock_service_class.return_value = mock_service

        result = runner.invoke(resolve, ["US0378331005"])

        assert result.exit_code == 0
        assert "Successfully resolved identifier" in result.output
        assert "US0378331005" in result.output
        assert "AAPL" in result.output
        assert "EQUITY" in result.output


def test_cli_resolve_failure() -> None:
    """Test CLI resolution failure."""
    runner = CliRunner()

    with patch("entity_resolver.cli.cli.ResolveService") as mock_service_class:
        mock_service = Mock()
        mock_service.resolve.return_value = None
        mock_service_class.return_value = mock_service

        result = runner.invoke(resolve, ["INVALID"])

        assert result.exit_code == 1
        assert "Failed to resolve identifier" in result.output


def test_cli_with_type_option() -> None:
    """Test CLI with identifier type option."""
    runner = CliRunner()

    with patch("entity_resolver.cli.cli.ResolveService") as mock_service_class:
        mock_service = Mock()
        mock_resolved = ResolvedEntity(
            original_identifier="US0378331005",
            resolved_identifier="AAPL",
            entity_type="EQUITY",
        )
        mock_service.resolve.return_value = mock_resolved
        mock_service_class.return_value = mock_service

        result = runner.invoke(resolve, ["US0378331005", "--type", "ISIN"])

        assert result.exit_code == 0
        assert "Successfully resolved identifier" in result.output


def test_cli_with_api_url_override() -> None:
    """Test CLI with API URL override."""
    runner = CliRunner()

    with patch("entity_resolver.cli.cli.ResolveService") as mock_service_class:
        mock_service = Mock()
        mock_resolved = ResolvedEntity(
            original_identifier="US0378331005",
            resolved_identifier="AAPL",
            entity_type="EQUITY",
        )
        mock_service.resolve.return_value = mock_resolved
        mock_service_class.return_value = mock_service

        result = runner.invoke(
            resolve,
            ["US0378331005", "--api-url", "https://custom.api.com/resolve"],
        )

        assert result.exit_code == 0
        mock_service_class.assert_called_once()
        call_kwargs = mock_service_class.call_args[1]
        assert call_kwargs["api_url"] == "https://custom.api.com/resolve"
