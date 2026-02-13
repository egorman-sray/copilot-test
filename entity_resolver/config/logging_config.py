"""Logging configuration using esgbook-py setup."""

import logging
import sys
from typing import Any, TextIO

import structlog
from pythonjsonlogger import json


class GCPJsonFormatter(json.JsonFormatter):
    """JSON formatter compatible with GCP Cloud Logging structured logging."""

    def add_fields(
        self, log_record: dict[str, Any], record: logging.LogRecord, message_dict: dict[str, Any]
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["severity"] = record.levelname


def configure_logging(log_level: str = "INFO", stream: TextIO = sys.stdout) -> None:
    """Configure structlog for JSON logging to stdout using esgbook-py setup.

    Args:
        log_level: The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        stream: The stream to output to (default: stdout)
    """
    level = getattr(logging, log_level.upper())

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_log_level_number,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.render_to_log_kwargs,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )

    handler = logging.StreamHandler(stream=stream)
    handler.setFormatter(GCPJsonFormatter())

    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
