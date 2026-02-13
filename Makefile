PYTHON_MODULE_NAME = entity_resolver
SERVICE_NAME = entity-resolver

.PHONY: help
help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install production dependencies
	pip install -e .

.PHONY: dev
dev: ## Install development dependencies
	pip install -e ".[dev]"

.PHONY: test
test: ## Run tests with coverage
	pytest --cov=$(PYTHON_MODULE_NAME) --cov-report=term-missing

.PHONY: lint
lint: ## Run linting checks
	ruff check .
	mypy .

.PHONY: format
format: ## Format code with ruff
	ruff check --fix .
	ruff format .

.PHONY: clean
clean: ## Remove generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov

.PHONY: run
run: ## Run the application
	python -m $(PYTHON_MODULE_NAME).main
