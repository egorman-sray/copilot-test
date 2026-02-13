"""Command-line interface for entity resolver."""

import sys

import click
import structlog

from entity_resolver.config.config import Settings
from entity_resolver.config.logging_config import configure_logging
from entity_resolver.entity.entity import EntityIdentifier
from entity_resolver.service.resolve_service import ResolveService

logger = structlog.get_logger(__name__)


@click.command()
@click.argument("identifier")
@click.option(
    "--type",
    "identifier_type",
    default="unknown",
    help="Type of the identifier (e.g., ISIN, LEI, ticker)",
)
@click.option(
    "--api-url",
    envvar="RESOLVE_API_URL",
    help="Override the resolve API URL",
)
@click.option(
    "--api-key",
    envvar="RESOLVE_API_KEY",
    help="Override the API key",
)
def resolve(
    identifier: str,
    identifier_type: str,
    api_url: str | None,
    api_key: str | None,
) -> None:
    """Resolve a company entity identifier.

    IDENTIFIER: The company entity identifier to resolve
    """
    settings = Settings()
    configure_logging(settings.log_level)

    logger.info("Starting entity resolution", identifier=identifier, type=identifier_type)

    entity_id = EntityIdentifier(value=identifier, type=identifier_type)

    service = ResolveService(
        api_url=api_url or settings.resolve_api_url,
        api_key=api_key or settings.resolve_api_key,
        timeout=settings.resolve_api_timeout,
    )

    resolved = service.resolve(entity_id)

    if resolved:
        click.echo("\n✓ Successfully resolved identifier:")
        click.echo(f"  Original:   {resolved.original_identifier}")
        click.echo(f"  Resolved:   {resolved.resolved_identifier}")
        click.echo(f"  Type:       {resolved.entity_type}")
        click.echo(f"  Confidence: {resolved.confidence:.2%}\n")
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
