"""Consistent project logging without leaking runtime configuration."""

from __future__ import annotations

import logging
import os


def configure_logging(name: str = "newsbot") -> logging.Logger:
    """Return a configured logger, avoiding duplicate handlers on repeated imports."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(os.getenv("NEWSBOT_LOG_LEVEL", "INFO").upper())
        logger.propagate = False
    return logger
