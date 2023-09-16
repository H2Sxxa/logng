from logng.shared import info, set_logger, warn
from logng.logger import Logger, LogConfig
from logng.outputs import VirtualAttyStdout,FileOutput

lg = Logger(LogConfig(stdouts=(VirtualAttyStdout,)))
lg.info("hello info")


set_logger(Logger(LogConfig(stdouts=(VirtualAttyStdout,FileOutput("latest.log")))))
info("hello")
warn("hello")
