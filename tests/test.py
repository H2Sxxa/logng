from logng.logger import get_or_create_logger, LogConfig
from sys import stdout

logf = open("latest.log", "w")
logger = get_or_create_logger(config=LogConfig(stdouts=[stdout, logf], maxcount=1))


async def async_main():
    for i in range(1000):
        logger.info("hello info", i)
    logger.warn("warn,finish")

from asyncio import run as run_async

run_async(async_main())
