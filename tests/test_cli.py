"""Tests for the CLI."""

import pytest
from click.testing import CliRunner
import responses
from entity_resolver.cli import main


class TestCLI:
    """Test cases for CLI."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @responses.activate
    def test_resolve_success(self):
        """Test successful CLI execution."""
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

        result = self.runner.invoke(main, ["COMPANY123"])

        assert result.exit_code == 0
        assert "Original identifier: COMPANY123" in result.output
        assert "Resolved identifier: RESOLVED123" in result.output
        assert "Company name: Test Company" in result.output
        assert "Status: active" in result.output

    @responses.activate
    def test_resolve_with_custom_api_url(self):
        """Test CLI with custom API URL."""
        responses.add(
            responses.POST,
            "https://custom.example.com/api",
            json={"resolved_identifier": "CUSTOM123"},
            status=200
        )

        result = self.runner.invoke(
            main, 
            ["TEST123", "--api-url", "https://custom.example.com/api"]
        )

        assert result.exit_code == 0
        assert "Resolved identifier: CUSTOM123" in result.output

    @responses.activate
    def test_resolve_api_error(self):
        """Test CLI handling of API errors."""
        responses.add(
            responses.POST,
            "http://localhost:8080/api/resolve",
            json={"error": "Not found"},
            status=404
        )

        result = self.runner.invoke(main, ["INVALID123"])

        assert result.exit_code == 1
        assert "Error:" in result.output

    def test_no_identifier_provided(self):
        """Test CLI with no identifier provided."""
        result = self.runner.invoke(main, [])

        assert result.exit_code != 0
        assert "Error" in result.output or "Missing argument" in result.output
