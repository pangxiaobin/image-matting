import sys
import os
from loguru import logger

from conf.setting import settings
from pathlib import Path

LOG = settings.LOG
# Add log storage file  添加日志存储路径
SERVER_PATH = settings.BASE_DIR
LOG_PATH = SERVER_PATH / "logs"
LOG_SIZE = LOG.get("max_log_size")
LOG_BACKUP_COUNT = LOG.get("backup_count")

USE_COLOR = settings.DEBUG


def init_logging(log_name="app", log_level="DEBUG"):
    """
    Initializes the Loguru logger with custom settings.

    Args:
        log_name (str, optional): The base name for log files. Defaults to "app".
        log_level (str, optional): The minimum logging level. Defaults to "DEBUG".
    """

    _format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</> | "
        "<lvl>{level}</> | <cyan>{file}:{line}</> - <lvl>{function}: {message}</> "
    )

    logger.remove()  # Remove default handler

    logger.add(
        sys.stderr,
        level=log_level,
        colorize=USE_COLOR,
        format=_format,
    )

    params = {
        "rotation": LOG_SIZE,
        "retention": LOG_BACKUP_COUNT,
        "compression": "zip",
        "encoding": "utf8",
        "format": _format,
    }

    if not LOG_PATH.exists():
        LOG_PATH.mkdir(parents=True, exist_ok=True)

    logger.add(LOG_PATH / f"{log_name}_debug.log", level="DEBUG", **params)
    logger.add(LOG_PATH / f"{log_name}_info.log", level="INFO", **params)
    logger.add(LOG_PATH / f"{log_name}_error.log", level="ERROR", **params)
