from logng.shared import info, warn
from logng.logger import Logger, LogConfig
from logng.outputs import VirtualAttyStdout, FileOutput

lg = Logger(
    LogConfig(stdouts=(VirtualAttyStdout, FileOutput("latest.log")), shared=True)
)
lg.info("hello info")
info("hello")
warn("hello")
