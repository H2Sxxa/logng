from logng.shared import info, set_logger, warn
from logng.logger import Logger, LogConfig

lg = Logger()
lg.info("hello info")


set_logger(Logger(LogConfig(locate_back=1)))
info("hello")
warn("hello")