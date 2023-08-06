import os
import logging
from typing import Union, Optional

try:
    import colorlog

    IS_COLORLOG_INSTALLED = True
except ImportError:
    IS_COLORLOG_INSTALLED = False


__all__ = [
    "omlet_logger",
    "initialize_omlet_logging",
    "set_logging_level",
    "get_logging_level",
    "create_logging_file_handler",
]


# custom debugging level that's higher than usual to distinguish from
# debug logs from other applications
DEBUG2 = logging.DEBUG + 2
logging.DEBUG2 = DEBUG2

# custom info level that's lower than usual to enable more verbosity
INFOV = logging.INFO - 1
INFOVV = logging.INFO - 2
INFOVVV = logging.INFO - 3
logging.INFOV = INFOV
logging.INFOVV = INFOVV
logging.INFOVVV = INFOVVV

# https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
logging.addLevelName(DEBUG2, "DEBUG2")
logging.addLevelName(INFOV, "INFOV")
logging.addLevelName(INFOVV, "INFOVV")
logging.addLevelName(INFOVVV, "INFOVVV")


_DATEFMT = "%m-%d-%y %H:%M:%S"


def _gen_logging_function(level):
    def _log_func(self, message, *args, **kws):
        if self.isEnabledFor(level):
            # Yes, logger takes its '*args' as 'args'.
            self._log(level, message, args, **kws)

    return _log_func


logging.Logger.debug2 = _gen_logging_function(DEBUG2)
logging.Logger.infov = _gen_logging_function(INFOV)
logging.Logger.infovv = _gen_logging_function(INFOVV)
logging.Logger.infovvv = _gen_logging_function(INFOVVV)


omlet_logger = logging.getLogger("omlet")


def initialize_omlet_logging(
    file_path=None,
    level=None,
    replace_all_stream_handlers: bool = True,
    enable: bool = True,
):
    """
    Directly manipulate root logger

    Args
        file_path: log file path
        replace_all_stream_handlers: replace StreamHandler of all existing loggers
    """
    if not enable:
        return
    color_handler = create_colorlog_handler()
    root = logging.getLogger()
    root.handlers = []
    if color_handler is not None:
        root.handlers.append(color_handler)
    if file_path:
        root.handlers.append(create_logging_file_handler(file_path))
    set_logging_level(level)

    if replace_all_stream_handlers:
        for name, logger in all_loggers().items():
            if not hasattr(logger, "handlers"):
                continue
            for handler in logger.handlers.copy():
                # we still keep file streaming for other apps
                if isinstance(handler, logging.StreamHandler) and not isinstance(
                    handler, logging.FileHandler
                ):
                    # print(name, 'HANDLER STREAM REMOVED')
                    logger.removeHandler(handler)


def create_colorlog_handler():
    if IS_COLORLOG_INSTALLED:
        # https://pypi.org/project/colorlog/
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "[%(cyan)s%(asctime)s%(reset)s][%(blue)s%(name)s%(reset)s][%(log_color)s%(levelname)s%(reset)s] %(message)s",
                # available color prefixes: bold_, thin_, bg_, fg_
                # colors: black, red, green, yellow, blue, purple, cyan and white
                log_colors={
                    "DEBUG": "purple",
                    "DEBUG2": "purple,bg_yellow",
                    "INFOV": "thin_green",
                    "INFOVV": "thin_green",
                    "INFOVVV": "thin_green",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "bold_red",
                    "CRITICAL": "red,bg_white",
                },
                datefmt=_DATEFMT,
            )
        )
        return handler
    else:
        return None


def all_loggers():
    return logging.Logger.manager.loggerDict


def create_logging_file_handler(file_path):
    file_path = os.path.expanduser(file_path)
    handler = logging.FileHandler(file_path)
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s][%(name)s][%(levelname)s] %(message)s", datefmt=_DATEFMT
        )
    )
    return handler


def get_logging_level(name=None):
    return logging.getLogger(name).getEffectiveLevel()


def set_logging_level(level: Optional[Union[int, str]] = "info", name=None):
    if level is None:
        return
    if isinstance(level, str):
        level = level.upper()
    logging.getLogger(name).setLevel(level)
