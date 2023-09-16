from functools import partialmethod
from types import FrameType
from logng.base.enums import LogBlock, LogLevel, WrapStr
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, List, TextIO, Tuple
from colorama import Fore, Style
from time import strftime, localtime
import sys, inspect

from logng.base.intfs import ILogger


if TYPE_CHECKING:

    class _CallLog:
        def __call__(self, *msg: Any) -> None:
            return msg


@dataclass
class LogConfig:
    """
    each property of this cls has a default, just modify as your requirement
    """

    stdouts: Tuple[TextIO] = (sys.stdout,)
    maxcount: int = None
    timeformat: str = "%D %T"
    level_color: Callable[[LogLevel], str] = (
        lambda level: Fore.LIGHTGREEN_EX
        if level == LogLevel.INFO
        else Fore.LIGHTYELLOW_EX
        if level == LogLevel.WARN
        else Fore.LIGHTRED_EX
        if level == LogLevel.ERROR
        else Fore.LIGHTMAGENTA_EX
        if level == LogLevel.TRACE
        else Fore.LIGHTCYAN_EX
    )
    loglevel: LogLevel = LogLevel.INFO
    logblocks: Tuple[LogBlock] = (
        LogBlock.LEVEL_COLOR,
        LogBlock.TIME,
        LogBlock.LEVEL,
        LogBlock.TARGET,
        " ",
        LogBlock.MSG,
        LogBlock.RESET_COLOR,
    )
    logblockwrap: Tuple[str, str] = (
        "[",
        "]",
    )
    shared: bool = False
    auto_newline: bool = True


current_logger = None


class Logger(ILogger):
    config: LogConfig
    isatty: List[bool]

    def __init__(self, config: LogConfig = LogConfig()) -> None:
        """
        the more complex config, the lower the output speed, just enable what's u need
        """
        super().__init__()
        self.config = config
        self.isatty = [std.isatty() for std in self.config.stdouts]
        global current_logger
        current_logger = self
        if self.config.shared:
            from .shared import set_logger

            set_logger(self)

    def log(self, level: LogLevel, *msg: Any) -> None:
        if level.value < self.config.loglevel.value:
            return
        for index, std in enumerate(self.config.stdouts):
            for lb in self.config.logblocks:
                if isinstance(lb, str):
                    std.write(
                        lb
                        if not isinstance(lb, WrapStr)
                        else self.config.logblockwrap[0]
                        + lb.to_str()
                        + self.config.logblockwrap[1]
                    )
                elif not lb.value[1]:
                    std.write(
                        (
                            " ".join(map(str, msg))
                            if lb == LogBlock.MSG
                            else self.config.level_color(level)
                            if self.isatty[index] and lb == LogBlock.LEVEL_COLOR
                            else Style.RESET_ALL
                            if self.isatty[index] and lb == LogBlock.RESET_COLOR
                            else ""
                        )
                    )
                else:
                    std.write(
                        self.config.logblockwrap[0]
                        + (
                            strftime(self.config.timeformat, localtime())
                            if lb == LogBlock.TIME
                            else level.name
                            if lb == LogBlock.LEVEL
                            else self.__locate_stack()
                            if lb == LogBlock.TARGET
                            else ""
                        )
                        + self.config.logblockwrap[1]
                    )
            if self.config.auto_newline:
                std.write("\n")
        return super().log(level, *msg)

    def __locate_stack(self) -> str:
        fr = inspect.getmodule(inspect.stack()[-1][0])
        return fr.__name__ if fr is not None else "__unknown__"

    def flush(self):
        for stdo in self.config.stdouts:
            stdo.flush()
        return super().flush()

    def auto_newline(self, __b: bool = False) -> None:
        self.config.auto_newline = __b

    def _write_to(self, __s: str) -> None:
        for st in self.config.stdouts:
            st.write(__s)

    def _write_to_atty(self, __s: str, __atty: bool = True) -> None:
        for i, s in enumerate(self.config.stdouts):
            if self.isatty[i] and __atty:
                s.write(__s)
            elif not __atty and not self.isatty[i]:
                s.write(__s)

    goto_start = partialmethod(_write_to, "\r")
    goto_start_atty = partialmethod(_write_to_atty, "\r")
    newline = partialmethod(_write_to, "\n")
    newline_atty = partialmethod(_write_to_atty, "\n")
    info: "_CallLog" = partialmethod(log, LogLevel.INFO)
    warn: "_CallLog" = partialmethod(log, LogLevel.WARN)
    error: "_CallLog" = partialmethod(log, LogLevel.ERROR)
    trace: "_CallLog" = partialmethod(log, LogLevel.TRACE)
    debug: "_CallLog" = partialmethod(log, LogLevel.DEBUG)

    def set_log_level(self, level: LogLevel) -> None:
        self.config.loglevel = level
        return super().set_log_level(level)


def get_or_create_logger(config: LogConfig = LogConfig()) -> Logger:
    return current_logger if current_logger is not None else Logger(config)
