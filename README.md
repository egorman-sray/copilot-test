# Entity Resolver

A CLI tool for resolving company entity identifiers using the ESGBook resolve API service.

## Overview

This Python application provides a command-line interface to resolve company entity identifiers (such as ISIN, LEI, CUSIP, ticker symbols) through the ESGBook resolve API service. It follows the arabesque-sray organization's Python best practices for project structure, logging, and configuration management.

## Features

- 🚀 Simple CLI interface for entity resolution
- 🔧 Configurable via environment variables or command-line options
- 📊 GCP-compatible structured JSON logging with structlog
- ✅ Comprehensive test coverage (94%)
- 🏗️ Hexagonal architecture with clear separation of concerns
- 🔐 Auth0 authentication support

## Project Structure

The project follows the organization's standard Python directory structure:

```
entity-resolver/
├── entity_resolver/          # Main package
│   ├── entity/              # Domain entities with identifier types
│   ├── service/             # Application services (resolve API client)
│   ├── cli/                 # Command-line interface
│   ├── config/              # Configuration and logging setup
│   └── main.py              # Application entry point
├── test/                    # Test suite (mirrors package structure)
├── pyproject.toml           # Project metadata and dependencies
├── Makefile                 # Common commands
└── .env.example             # Environment variable template
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip

### Install Dependencies

```bash
# Install production dependencies
make install

# Or install with development dependencies
make dev
```

## Configuration

The application uses environment variables for configuration. Copy the example file and customize:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Entity Resolver API Configuration
RESOLVE_SERVICE__API_URL=https://staging.app.dev.esgbook.com/api
RESOLVE_SERVICE__API_PATH=entities/lookup
RESOLVE_SERVICE__TIMEOUT=30

# Auth0 Configuration
AUTH0_TOKEN=your-auth0-token-here

# Logging Configuration
LOG_LEVEL=INFO
```

### Supported Identifier Types

The application supports the following entity identifier types:

- `CUSIP` - Committee on Uniform Securities Identification Procedures
- `ISIN` - International Securities Identification Number
- `SEDOL` - Stock Exchange Daily Official List
- `SRAY_ENTITY_ID` - S-Ray internal entity identifier
- `ASSET_ID` - Asset identifier
- `FS_ENTITY_ID` - FactSet entity identifier
- `ENTITY_ID` - Generic entity identifier
- `FIGI` - Financial Instrument Global Identifier
- `TICKER_EXCHANGE` - Ticker symbol with exchange
- `LEI` - Legal Entity Identifier
- `SERIES_ID` - Series identifier

## Usage

### Basic Usage

Resolve a company entity identifier:

```bash
entity-resolver US0378331005
```

### With Identifier Type

Specify the type of identifier:

```bash
entity-resolver US0378331005 --type ISIN
```

### Override API Configuration

Override the API URL or Auth0 token via command-line options:

```bash
entity-resolver US0378331005 --api-url https://custom.api.com/entities/lookup --auth0-token your-token
```

### Using Environment Variables

You can also set configuration via environment variables:

```bash
export RESOLVE_SERVICE__API_URL=https://staging.app.dev.esgbook.com/api
export AUTH0_TOKEN=your-auth0-token
entity-resolver US0378331005
```

## Output

Successful resolution:

```
✓ Successfully resolved identifier:
  Original:   US0378331005
  Resolved:   AAPL
  Type:       EQUITY
```

Failed resolution:

```
✗ Failed to resolve identifier
```

## Development

### Running Tests

```bash
# Run all tests with coverage
make test
```

### Linting and Type Checking

```bash
# Run linting and type checking
make lint
```

### Code Formatting

```bash
# Format code with ruff
make format
```

### Clean Build Artifacts

```bash
# Remove generated files
make clean
```

## Architecture

This application follows hexagonal architecture principles:

- **Entity Layer** (`entity/`): Domain models (EntityIdentifier, ResolvedEntity)
- **Service Layer** (`service/`): Business logic (ResolveService)
- **CLI Layer** (`cli/`): User interface (Click-based CLI)
- **Config Layer** (`config/`): Configuration and logging setup

### Best Practices Applied

This project follows the organization's Python best practices:

1. **Directory Structure**: Flat layout with hexagonal architecture
2. **Data Modeling**: Uses standard dataclasses for simple internal entities with enum for identifier types
3. **Configuration**: Uses Pydantic BaseSettings with nested config for resolve service
4. **Logging**: Uses esgbook-py logging setup with GCP-compatible JSON output (includes severity field)
5. **Testing**: Comprehensive test suite with pytest (94% coverage)
6. **Authentication**: Auth0 token-based authentication

## API Contract

The resolver service expects the following API contract:

### Request

```json
POST /entities/lookup
Authorization: Bearer <auth0-token>
Content-Type: application/json

{
  "identifier": "US0378331005",
  "type": "ISIN"
}
```

### Response

```json
{
  "resolved_identifier": "AAPL",
  "entity_type": "EQUITY"
}
```

## Error Handling

The application handles various error scenarios:

- **HTTP Errors**: Logs status code and error details
- **Request Errors**: Logs connection/timeout issues
- **Unexpected Errors**: Logs full exception with stack trace

All errors result in a non-zero exit code for proper shell integration.

## Logging

The application uses structured logging with GCP-compatible JSON output:

```json
{
  "message": "Resolving identifier",
  "identifier": "US0378331005",
  "timestamp": "2026-02-13T14:30:00.123456Z",
  "logger": "entity_resolver.service.resolve_service",
  "level": "info",
  "level_number": 20,
  "severity": "INFO"
}
```

Log level can be controlled via the `LOG_LEVEL` environment variable.

## Contributing

When contributing to this project, please ensure:

1. Tests pass: `make test`
2. Code is formatted: `make format`
3. Code passes linting: `make lint`
4. Follow the organization's Python best practices

## License

Copyright © 2026 Arabesque S-Ray
