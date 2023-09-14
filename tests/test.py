from logng.shared import info, set_logger, warn
from logng.logger import Logger, LogConfig


lg = Logger(LogConfig(allow_noatty_color=True))
lg.info("hello info")


set_logger(Logger(LogConfig(locate_back=1, allow_noatty_color=True)))
info("hello")
warn("hello")
