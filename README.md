# Company Entity Identifier Resolver

A Python CLI tool to resolve company entity identifiers using a resolve API service.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Resolve a company entity identifier
resolve-entity <identifier>

# Example
resolve-entity COMPANY123
```

## Configuration

The API endpoint can be configured via environment variable:
- `RESOLVE_API_URL`: The URL of the resolve API service (default: http://localhost:8080/api/resolve)

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

## Testing with Mock API

A mock API server is provided for testing:

```bash
# Terminal 1 - Start the mock API server
pip install flask
python examples/mock_api_server.py

# Terminal 2 - Test the CLI
resolve-entity COMPANY123
resolve-entity TEST456
resolve-entity INACTIVE999
```

Available test identifiers in the mock API:
- `COMPANY123` - Example Corporation (active)
- `TEST456` - Test Limited (active)
- `INACTIVE999` - Inactive Company (inactive)
