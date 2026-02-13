"""Command-line interface for entity resolver."""

import sys
import click
from .api_client import ResolveAPIClient


@click.command()
@click.argument('identifier')
@click.option(
    '--api-url',
    envvar='RESOLVE_API_URL',
    help='URL of the resolve API service'
)
def main(identifier: str, api_url: str = None):
    """
    Resolve a company entity identifier.

    IDENTIFIER: The company entity identifier to resolve.
    """
    try:
        client = ResolveAPIClient(api_url)
        result = client.resolve(identifier)
        
        # Display the resolved identifier
        click.echo(f"Original identifier: {identifier}")
        click.echo(f"Resolved identifier: {result.get('resolved_identifier', 'N/A')}")
        
        # Display any additional information
        if 'company_name' in result:
            click.echo(f"Company name: {result['company_name']}")
        if 'status' in result:
            click.echo(f"Status: {result['status']}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
