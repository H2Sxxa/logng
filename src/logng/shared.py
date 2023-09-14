from functools import partial
from typing import Callable
from logng.base.enums import LogLevel
from logng.base.intfs import ILogger

__shared_logger: ILogger = None


def set_logger(logger: ILogger) -> ILogger:
    global __shared_logger
    __shared_logger = logger
    return __shared_logger


get_or_default: Callable[[ILogger], ILogger] = (
    lambda default: __shared_logger if __shared_logger is not None else default
)
log = __shared_logger.log
set_log_level = __shared_logger.set_log_level
info = partial(log, LogLevel.INFO)
warn = partial(log, LogLevel.WARN)
error = partial(log, LogLevel.ERROR)
debug = partial(log, LogLevel.DEBUG)
trace = partial(log, LogLevel.TRACE)
