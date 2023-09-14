from abc import ABC, abstractmethod

from logng.base.logtype import LogLevel


class ILogger(ABC):
    @abstractmethod
    def log(self, level: LogLevel, *msg: str) -> None:
        """"""

    @abstractmethod
    def flush(self):
        """"""
