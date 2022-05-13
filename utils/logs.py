import logging
import sys
from loguru import logger


# import matplotlib.pyplot as plt
# plt.set_loglevel('WARNING')

# 日志模块

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def setting():
    # logging configuration
    LOGGING_LEVEL = logging.DEBUG
    logging.basicConfig(
        handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
    )
    logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
