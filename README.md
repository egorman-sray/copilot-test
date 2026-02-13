# Entity Resolver

A CLI tool for resolving company entity identifiers using a REST API service.

## Overview

This Python application provides a command-line interface to resolve company entity identifiers (such as ISIN, LEI, ticker symbols) through a resolve API service. It follows the arabesque-sray organization's Python best practices for project structure, logging, and configuration management.

## Features

- 🚀 Simple CLI interface for entity resolution
- 🔧 Configurable via environment variables or command-line options
- 📊 Structured JSON logging with structlog
- ✅ Comprehensive test coverage
- 🏗️ Hexagonal architecture with clear separation of concerns
- 🔐 Secure API key authentication

## Project Structure

The project follows the organization's standard Python directory structure:

```
entity-resolver/
├── entity_resolver/          # Main package
│   ├── entity/              # Domain entities
│   ├── service/             # Application services
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
RESOLVE_API_URL=https://api.example.com/resolve
RESOLVE_API_KEY=your-api-key-here
RESOLVE_API_TIMEOUT=30

# Logging Configuration
LOG_LEVEL=INFO
```

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

Override the API URL or key via command-line options:

```bash
entity-resolver US0378331005 --api-url https://custom.api.com/resolve --api-key your-key
```

### Using Environment Variables

You can also set configuration via environment variables:

```bash
export RESOLVE_API_URL=https://api.example.com/resolve
export RESOLVE_API_KEY=your-api-key
entity-resolver US0378331005
```

## Output

Successful resolution:

```
✓ Successfully resolved identifier:
  Original:   US0378331005
  Resolved:   AAPL
  Type:       EQUITY
  Confidence: 95.00%
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
2. **Data Modeling**: Uses standard dataclasses for simple internal entities
3. **Configuration**: Uses Pydantic BaseSettings for environment-based config
4. **Logging**: Uses structlog with JSON output for GCP compatibility
5. **Testing**: Comprehensive test suite with pytest

## API Contract

The resolver service expects the following API contract:

### Request

```json
POST /resolve
Authorization: Bearer <api-key>
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
  "entity_type": "EQUITY",
  "confidence": 0.95
}
```

## Error Handling

The application handles various error scenarios:

- **HTTP Errors**: Logs status code and error details
- **Request Errors**: Logs connection/timeout issues
- **Unexpected Errors**: Logs full exception with stack trace

All errors result in a non-zero exit code for proper shell integration.

## Logging

The application uses structured logging with JSON output:

```json
{
  "event": "Resolving identifier",
  "identifier": "US0378331005",
  "timestamp": "2026-02-13T14:30:00.123456Z",
  "level": "info"
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
