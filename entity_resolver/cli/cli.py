"""Command-line interface for entity resolver."""

import logging
import sys

import click
import structlog
from esgbook_py.logging.setup import setup as setup_logging

from entity_resolver.config.config import Settings
from entity_resolver.entity.entity import EntityIdentifier
from entity_resolver.service.resolve_service import ResolveService

logger = structlog.get_logger(__name__)


@click.command()
@click.argument("identifier")
@click.option(
    "--type",
    "identifier_type",
    default="unknown",
    help="Type of the identifier (e.g., ISIN, LEI, CUSIP)",
)
@click.option(
    "--api-url",
    envvar="RESOLVE_SERVICE__API_URL",
    help="Override the resolve API URL",
)
@click.option(
    "--auth0-token",
    envvar="AUTH0_TOKEN",
    help="Auth0 token for authentication",
)
def resolve(
    identifier: str,
    identifier_type: str,
    api_url: str | None,
    auth0_token: str | None,
) -> None:
    """Resolve a company entity identifier.

    IDENTIFIER: The company entity identifier to resolve
    """
    settings = Settings()
    setup_logging(level=getattr(logging, settings.log_level.upper()))

    logger.info("Starting entity resolution", identifier=identifier, type=identifier_type)

    entity_id = EntityIdentifier(value=identifier, type=identifier_type)

    service = ResolveService(
        api_url=api_url or settings.resolve_service.full_url,
        auth0_token=auth0_token or "",
        timeout=settings.resolve_service.timeout,
    )

    resolved = service.resolve(entity_id)

    if resolved:
        click.echo("\n✓ Successfully resolved identifier:")
        click.echo(f"  Original:   {resolved.original_identifier}")
        click.echo(f"  Resolved:   {resolved.resolved_identifier}")
        click.echo(f"  Type:       {resolved.entity_type}\n")
        sys.exit(0)
    else:
        click.echo("\n✗ Failed to resolve identifier\n", err=True)
        logger.error("Resolution failed", identifier=identifier)
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI application."""
    resolve()


if __name__ == "__main__":
    main()
