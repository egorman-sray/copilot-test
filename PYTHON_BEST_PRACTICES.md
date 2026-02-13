# Python Best Practices for Arabesque S-Ray Organisation

This document provides a comprehensive guide to Python development best practices within the arabesque-sray organisation. These practices are sourced from the official documentation in the `arabesque-sray/ops` repository and the custom libraries in `arabesque-sray/esgbook-py`.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Code Style](#code-style)
3. [Project Structure](#project-structure)
4. [Data Modeling Patterns](#data-modeling-patterns)
5. [Logging Patterns](#logging-patterns)
6. [Custom Libraries (esgbook-py)](#custom-libraries-esgbook-py)
7. [Development Tools](#development-tools)
8. [Environment Configuration](#environment-configuration)
9. [Testing](#testing)
10. [Quick Reference Guide](#quick-reference-guide)

---

## Core Principles

The arabesque-sray organisation follows these fundamental principles for Python development:

1. **Flat Layout with Hexagonal Architecture** - Package directory at project root with clear separation of domain, use cases, adapters, and infrastructure
2. **Modern Package Management** - Use `uv` for fast, modern dependency management (10-100x faster than pip)
3. **Structured Logging** - Use `structlog` for all logging with JSON output for GCP
4. **Type Safety** - Enable `mypy` and use type hints throughout
5. **Configuration as Code** - Use Pydantic `BaseSettings` for configuration management
6. **Dependency Inversion** - Depend on interfaces, not implementations
7. **Separation of Concerns** - Clear architectural layers with single responsibilities

---

## Code Style

### Line Length

**Recommended line length: 100 characters**

This provides a good balance between readability and efficient use of modern monitors.

### Directory Naming Convention

**Use singular directory names** (`entity/`, `use_case/`, `service/`, `repository/`, `test/`)

**Rationale:**
- Consistency with Go codebase conventions
- Directories represent architectural concepts (singular), not collections of assets
- For asset collections like `resource/images/`, plural may be appropriate

---

## Project Structure

### Standard Directory Layout

```text
my-project/
├── .gitignore
├── README.md
├── Makefile                     # Common commands and shortcuts
├── pyproject.toml               # Project metadata, dependencies, tool configs
├── uv.lock                      # Dependency lockfile (commit to git)
├── .env.example                 # Environment variable template (commit)
├── .env                         # Actual secrets (DO NOT commit)
│
├── my_project/                  # Main package (flat layout)
│   ├── __init__.py
│   │
│   ├── entity/                  # Domain entities and data models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   │
│   ├── use_case/                # Application use cases
│   │   ├── __init__.py
│   │   ├── create_order.py
│   │   └── get_user.py
│   │
│   ├── service/                 # Application services
│   │   ├── __init__.py
│   │   ├── order_service.py
│   │   └── prediction_service.py
│   │
│   ├── repository/              # Repository interfaces and implementations
│   │   ├── __init__.py
│   │   ├── base.py              # Base repository interface
│   │   ├── user.py              # User repository interface
│   │   ├── psql/                # PostgreSQL implementations
│   │   ├── inmemory/            # In-memory implementations (for testing)
│   │   └── fs/                  # File system implementations
│   │
│   ├── cli/                     # Command-line interface
│   │   ├── __init__.py
│   │   └── cli.py
│   │
│   ├── api/                     # API endpoints (if web service)
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── routes/
│   │
│   ├── config/                  # Application configuration
│   │   ├── __init__.py
│   │   ├── config.py            # Main Settings class (BaseSettings)
│   │   ├── database.py          # DatabaseConfig (BaseModel)
│   │   └── cache.py             # CacheConfig (BaseModel)
│   │
│   ├── resource/                # Static data files
│   │   ├── prompts/
│   │   ├── templates/
│   │   └── data/
│   │
│   └── main.py                  # Application entry point
│
├── test/                        # Test suite (mirrors package structure)
│   ├── __init__.py
│   ├── conftest.py              # Shared test fixtures
│   ├── entity/
│   ├── use_case/
│   ├── repository/
│   └── service/
│
├── scripts/                     # Utility scripts
└── docs/                        # Documentation (optional)
```

### Layer Responsibilities

| Layer | Purpose | Characteristics |
|-------|---------|-----------------|
| **entity/** | Domain logic | Pure data models, no I/O, no external dependencies |
| **use_case/** | Application logic | Business workflows, orchestrates repositories and services |
| **service/** | Application services | Cross-cutting functionality, service orchestration |
| **repository/** | Data access | Interfaces + implementations by backend type |
| **config/** | Configuration | Component configs (BaseModel) + Settings (BaseSettings) |
| **resource/** | Static files | JSON prompts, templates, reference data |
| **cli/** | CLI interface | Command-line commands |
| **api/** | HTTP interface | API routes and endpoints |

### Repository Organization

Organize repository implementations by backend type:

- **Storage backends:** `psql/`, `inmemory/`, `fs/`
- **API/Service providers:** `gemini/`, `openai/`, `anthropic/`

**Benefits:**
- Clear separation by technology or provider
- Easy to locate implementations for specific backends
- Simple to add new backends
- Clean testing with mock/in-memory implementations
- Dependency inversion principle

---

## Data Modeling Patterns

### Quick Decision Guide

| Scenario | Use | Why |
|----------|-----|-----|
| Internal objects (no validation) | Standard `dataclass` | Performance, simplicity |
| Internal objects (light validation) | Pydantic `dataclass` | Type safety, validation |
| App config with env vars | `BaseSettings` | Auto env loading, validation |
| API request/response | `BaseModel` | Runtime validation, JSON serialization |
| Untrusted external data | `BaseModel` | Type safety, validation, coercion |

### Standard Dataclass (Internal Objects, No Validation)

```python
from dataclasses import dataclass

@dataclass
class ServerConfig:
    host: str
    port: int
    timeout: float = 30.0
```

**Use when:**
- Internal domain objects
- Data already validated or trusted
- No validation needed
- Performance matters

### Pydantic Dataclass (Internal Objects, Light Validation)

```python
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class ServerConfig:
    host: str
    port: int = Field(gt=0, le=65535)
    timeout: float = Field(default=30.0, gt=0)
```

**Use when:**
- Internal domain objects that need validation
- Need lightweight validation with dataclass simplicity
- Want type safety and automatic validation

### Pydantic BaseModel (External, Untrusted Data)

```python
from pydantic import BaseModel, Field, field_validator

class UserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    age: int = Field(gt=0, lt=150)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
```

**Use when:**
- External API data
- User input validation
- Need type coercion
- Complex validation rules

### Application Settings with BaseSettings

```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# Nested configs use BaseModel
class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432
    username: str
    password: str

class Settings(BaseSettings):
    database: DatabaseConfig
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        extra='ignore'  # Ignore extra fields in .env
    )

# Automatically loads from environment:
# DATABASE__HOST=localhost
# DATABASE__PORT=5432
settings = Settings()
```

### Function Parameter Design

**1-3 parameters:** Use individual args for clarity

```python
def send_email(recipient: str, subject: str, body: str) -> None:
    pass
```

**4+ parameters:** Use parameter object (but first consider splitting the function)

```python
from pydantic.dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    pool_size: int = 10

def create_connection(config: DatabaseConfig) -> Connection:
    pass
```

---

## Logging Patterns

### Core Principles

1. **Log to stdout** - All logs go to stdout, GCP captures them
2. **JSON format** - GCP requires JSON for proper parsing
3. **structlog everywhere** - Use structlog in all Python code (except quick scripts)
4. **Context binding** - Use `bound_contextvars()` context manager for automatic context propagation
5. **Logger declaration** - Always declare logger at top of file: `logger = structlog.get_logger(__name__)`

### Log Levels

- **Development:** debug+
- **Production:** info+

### Logger Declaration

```python
import structlog

logger = structlog.get_logger(__name__)
```

### Context Binding (Recommended Pattern)

Use context manager for automatic cleanup:

```python
from structlog.contextvars import bound_contextvars

def worker(extraction_id):
    logger = structlog.get_logger(__name__)

    # Context only exists within this block
    with bound_contextvars(extraction_id=extraction_id):
        logger.info("processing", status="started")
        other_processor()  # Also has extraction_id automatically
    
    # Context cleared after exiting with block
    logger.info("done")  # no extraction_id here
```

### Logging Best Practices

1. **Use structlog consistently** - Use in all Python code for alignment
2. **Prefer context managers** - Use `with bound_contextvars(var=...):` for context propagation
3. **Declare logger at module level** - Always at top of file after imports
4. **Log detailed information** - Encourage logging more details, filter later
5. **Use appropriate levels:**
   - `debug` - Detailed diagnostic information
   - `info` - General operational messages
   - `warning` - Issues with workarounds
   - `error` - Failures requiring attention (use `exception` for detailed exception info)

---

## Custom Libraries (esgbook-py)

The `arabesque-sray/esgbook-py` repository provides custom libraries maintained by the organisation.

### Available Modules

#### 1. Logging Setup (`esgbook_py.logging.setup`)

Provides structured logging configuration for GCP compatibility:

```python
from esgbook_py.logging import setup
import logging

# Setup logging with GCP-compatible JSON formatting
setup(level=logging.INFO)
```

**Features:**
- GCP Cloud Logging compatible JSON formatter
- Integrates with structlog
- Automatic context variable merging
- ISO timestamps
- Proper severity mapping for GCP

#### 2. Retry Settings (`esgbook_py.entity.retry`)

Provides configuration for retry operations:

```python
from esgbook_py.entity.retry import RetrySettings

retry_config = RetrySettings(
    max_attempts=3,
    constant_delay_seconds=0.1,
    exponential_multiplier=0.0,
    jitter_seconds=0.0
)
```

**Features:**
- Fixed/exponential backoff support
- Jitter configuration
- Configurable max attempts
- Pydantic-based validation

#### 3. Storage Utilities

The library includes storage utilities for:
- Database operations (`esgbook_py.storage.db`)
- Google Cloud Storage (`esgbook_py.storage.gcs`)

**Usage:** Check the library documentation for specific implementations.

### Using esgbook-py in Your Project

Add to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "esgbook-py @ git+https://github.com/arabesque-sray/esgbook-py.git",
]
```

Or with uv:

```bash
uv add git+https://github.com/arabesque-sray/esgbook-py.git
```

---

## Development Tools

### Package Manager: uv

**Use `uv` for all projects** - 10-100x faster than pip

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init my-project
cd my-project

# Create virtual environment
uv venv --python 3.11

# Activate virtual environment
source .venv/bin/activate

# Add dependencies
uv add pydantic pydantic-settings

# Install dependencies
uv sync
```

### pyproject.toml Configuration

Single source of truth for project metadata and tool configurations:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "structlog>=23.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

### Linting and Formatting

**ruff** - Fast linter and formatter

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Fix issues automatically
uv run ruff check --fix .
```

### Type Checking

**mypy** - Static type checker

```bash
# Run type checking
uv run mypy my_project/
```

---

## Environment Configuration

### .env Files

**DO NOT commit `.env`** - Add to `.gitignore`

**DO commit `.env.example`** - Template for required variables

### .env.example

```bash
# Database Configuration
DATABASE__HOST=localhost
DATABASE__PORT=5432
DATABASE__DATABASE=myapp_dev
DATABASE__USERNAME=postgres
DATABASE__PASSWORD=your-password

# Cache Configuration
CACHE__REDIS_URL=redis://localhost:6379
CACHE__TTL=300

# Application Settings
ENVIRONMENT=development
DEBUG=false
```

### Configuration Pattern

```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432
    database: str
    username: str
    password: str

class Settings(BaseSettings):
    database: DatabaseConfig
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        extra='ignore'
    )
```

### Source Priority (Highest to Lowest)

1. Explicit initialization arguments
2. Environment variables
3. .env files
4. Default values

---

## Testing

### Test Structure

Mirror the main package structure:

```text
test/
├── __init__.py
├── conftest.py              # Shared test fixtures
├── entity/
│   └── test_user.py
├── use_case/
│   └── test_create_order.py
└── repository/
    └── test_user_repository.py
```

### Test Configuration (conftest.py)

```python
import pytest
from my_project.config import Settings

@pytest.fixture
def test_settings():
    return Settings(
        database=DatabaseConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test",
            password="test"
        ),
        debug=True
    )
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest test/use_case/test_create_order.py

# Run with coverage
uv run pytest --cov=my_project --cov-report=html
```

---

## Quick Reference Guide

### When to Use What

| Use Case | Tool/Pattern |
|----------|--------------|
| Package management | `uv` |
| Project structure | Flat layout with hexagonal architecture |
| Internal objects (no validation) | Standard `dataclass` |
| Internal objects (with validation) | Pydantic `dataclass` |
| External data validation | Pydantic `BaseModel` |
| Application configuration | Pydantic `BaseSettings` |
| Logging | `structlog` with JSON output |
| Logging context | `bound_contextvars()` context manager |
| Type checking | `mypy` |
| Linting/formatting | `ruff` |
| Testing | `pytest` |
| Line length | 100 characters |
| Directory naming | Singular (entity/, use_case/, etc.) |

### Essential Commands

```bash
# Project setup
uv init my-project && cd my-project
uv venv --python 3.11
source .venv/bin/activate

# Add dependencies
uv add pydantic pydantic-settings structlog

# Development
uv run ruff format .
uv run ruff check --fix .
uv run mypy my_project/
uv run pytest

# Run application
uv run python -m my_project.main
```

### Key Principles Summary

1. **Validate at boundaries** - Use Pydantic for external data
2. **Static typing everywhere** - Enable mypy, use type hints
3. **Fail fast** - Validate config at startup
4. **Separate concerns** - Split config by domain
5. **Only pass what's needed** - Avoid passing entire config objects
6. **Explicit dependencies** - Inject config, avoid globals
7. **Log to stdout** - JSON format for GCP
8. **Use context managers** - For logging context propagation
9. **Mirror test structure** - Tests mirror package structure
10. **Singular naming** - For architectural layers

---

## Additional Resources

### Official Documentation

- **ops repository:** `arabesque-sray/ops/docs/tech-office/best-practices/python/`
  - Line Length: `line-length.md`
  - Logging Patterns: `python-logging.md`
  - Data Modeling: `python-data-modeling-patterns.md`
  - Directory Structure: `directory-structure.md`

- **esgbook-py library:** `arabesque-sray/esgbook-py`
  - Logging utilities
  - Retry configurations
  - Storage utilities

### External References

- **uv Documentation:** https://docs.astral.sh/uv/
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **structlog Documentation:** https://www.structlog.org/
- **pytest Documentation:** https://docs.pytest.org/
- **ruff Documentation:** https://docs.astral.sh/ruff/
- **mypy Documentation:** https://mypy.readthedocs.io/

---

## Summary

Working with Python in the arabesque-sray organisation means:

1. **Use modern tools**: `uv` for package management, `ruff` for linting, `mypy` for type checking
2. **Follow hexagonal architecture**: Clear separation of domain, use cases, services, and repositories
3. **Use Pydantic**: For data validation and configuration management
4. **Use structlog**: For structured logging with JSON output to GCP
5. **Leverage esgbook-py**: Utilise organisation-maintained libraries
6. **Keep it clean**: 100 character lines, singular directory names, flat layout
7. **Test well**: Mirror package structure, use fixtures, aim for coverage
8. **Configure properly**: Use `BaseSettings` with `.env` files, never commit secrets
9. **Type everything**: Enable strict mypy, use type hints throughout
10. **Document**: Keep README updated, use docstrings, follow conventions

These practices ensure consistency, maintainability, and quality across all Python projects in the organisation.
