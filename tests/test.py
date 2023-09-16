from logng.shared import info, error
from logng.logger import Logger, LogConfig
from logng.outputs import VirtualAttyStdout, FileOutput

lg = Logger(
    LogConfig(stdouts=(VirtualAttyStdout, FileOutput("latest.log")), shared=True)
)

lg.auto_newline()


for i in range(1002):
    lg.goto_start()
    if i != 1000:
        info(i)
    else:
        error("crash in", i)
        break
    lg.flush()

lg.newline()
lg.auto_newline(True)
info("hello")
