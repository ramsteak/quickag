import logging
from typing import Sequence, TypeAlias, TypeVar, Protocol, runtime_checkable

filepath: TypeAlias = str
_T_contra = TypeVar("_T_contra", contravariant=True)


@runtime_checkable
class SupportsWrite(Protocol[_T_contra]):
    def write(self, __s: _T_contra) -> object:
        ...


LOG_LEVELS = (
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
)
LOG_CODENAMES = ("DBG", "INF", "WRN", "ERR", "CRT")


def _gethandler(
    out: filepath | SupportsWrite, level: int, formatter: logging.Formatter
) -> logging.FileHandler | logging.StreamHandler:
    if isinstance(out, str):
        hand = logging.FileHandler(out, "a+")
    else:
        hand = logging.StreamHandler(out)
    hand.setFormatter(formatter)
    hand.setLevel(level)
    return hand


def getlogger(
    loggername: str,
    outputs: Sequence[filepath | SupportsWrite]
    | Sequence[tuple[filepath | SupportsWrite, int | str]]
    | filepath
    | SupportsWrite,
    level: int = logging.INFO,
    codenames: Sequence[str] = LOG_CODENAMES,
) -> logging.Logger:
    for type, name in zip(LOG_LEVELS, codenames):
        logging.addLevelName(type, name)

    log = logging.getLogger(loggername)
    log.setLevel(level)

    logformatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s <%(name)s> : %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    match outputs:
        case str():
            handler = _gethandler(outputs, level, logformatter)
            log.addHandler(handler)
        case SupportsWrite():
            handler = _gethandler(outputs, level, logformatter)
            log.addHandler(handler)
        case [*_]:
            for o in outputs:
                if isinstance(o, tuple):
                    out, lvl = o
                    handler = _gethandler(out, lvl, logformatter)
                else:
                    handler = _gethandler(o, level, logformatter)
                log.addHandler(handler)

    return log
