from logng.shared import info, set_logger, warn
from logng.logger import Logger, LogConfig
from logng.utils import VirtualAttyStdout

lg = Logger(LogConfig(stdouts=(VirtualAttyStdout,)))
lg.info("hello info")


set_logger(Logger(LogConfig(locate_back=1, stdouts=(VirtualAttyStdout,))))
info("hello")
warn("hello")
