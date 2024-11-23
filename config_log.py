"""Main logging configuration."""

import logging
import logging.config
import sys

LOG_CONF: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | "
            "%(filename)s | %(lineno)d | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "main",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": "log/log.log",
            "maxBytes": 1024 * 1024,  # 1 MB
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "main",
        },
    },
    "loggers": {
        "file": {
            "level": "INFO",
            "handlers": ["file"],
        },
        "console": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
        },
    },
}


def get_logger(name: str) -> logging.Logger:
    """Configure logger."""
    logger = logging.getLogger(name)
    logging.config.dictConfig(LOG_CONF)

    return logger
