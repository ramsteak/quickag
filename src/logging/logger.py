import logging
from sys import stdout
from typing import Iterable, TypeAlias

fname: TypeAlias = str

LOG_LEVELS = (
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
)
LOG_CODENAMES = ("DBG", "INF", "WARN", "ERR", "CRT")


def getlogger(
    name: str,
    outputs: Iterable[fname | logging._StreamT],
    level: int = logging.INFO,
    codenames: Iterable[str] = LOG_CODENAMES,
) -> logging.Logger:
    for type, name in zip(LOG_LEVELS, codenames):
        logging.addLevelName(type, name)

    log = logging.getLogger(name)
    log.setLevel(level)

    logformatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s %(name)s : %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    for out in outputs:
        if isinstance(out, str):
            filehandler = logging.FileHandler(out, "a+")
            filehandler.setFormatter(logformatter)
            filehandler.setLevel(logging.DEBUG)
            log.addHandler(filehandler)
        else:
            printhandler = logging.StreamHandler(stdout)
            printhandler.setFormatter(logformatter)
            printhandler.setLevel(logging.DEBUG)
            log.addHandler(printhandler)

    return log
