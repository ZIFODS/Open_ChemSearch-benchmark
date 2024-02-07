import logging
from pathlib import Path

import structlog
from structlog._config import BoundLoggerLazyProxy


def get_logger(filepath: Path) -> BoundLoggerLazyProxy:
    """Get logger for app.

    Returns:
        BoundLoggerLazyProxy: Logger.
    """
    logger_name = str(filepath)
    logger = logging.getLogger(logger_name)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(filepath)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger(
        logger_name,
    )

    return logger
