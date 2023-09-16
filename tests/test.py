from logng.shared import info, warn
from logng.logger import Logger, LogConfig
from logng.outputs import VirtualAttyStdout, FileOutput

lg = Logger(
    LogConfig(stdouts=(VirtualAttyStdout, FileOutput("latest.log")), shared=True)
)


info("start")

lg.auto_newline(False)

for i in range(11):
    lg.goto_start_atty()
    if i != 10:
        lg.info_atty(True, i)
    else:
        warn("crash in", i)
        break
    lg.flush()

lg.newline()
lg.auto_newline(True)
info("hello")
