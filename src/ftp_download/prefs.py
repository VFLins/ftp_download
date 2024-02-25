import asyncio
import logging
from os.path import join, expanduser, exists, split
from os import makedirs


class GlobalConfigDefaults:
    def __init__(self):
        self.verbose: bool = True
        """Should event messages be printed do `stdout`? This does not affect logging""" # noqa

        self.timeout: int = 10
        """Time to wait for request responses in seconds (unused yet)"""

        self.retry: int = 5
        """Maximum amount of attempts for every request (unused yet)"""

        self.raise_if_invalid: bool = True
        """Shoud stop if an invalid path is provided? If `False` it will just print a message""" # noqa

        self.use_async: bool = False
        """Should send asynchronous download requests? If `True` your program might run faster, due to not waiting for downloads to finish. Might be incompatible with Jupyter Notebooks and some implementations of GUI applications that runs on event loops.""" # noqa

        self.download_folder: str = join(
            expanduser("~"), "Downloads", "ftp_download"
        )
        """Standard destination path for all downloads"""

    def __repr__(self):
        return (
            "FTP_DOWLOAD SETTINGS: \n" +
            f"verbose = {self.verbose}; \n" +
            f"raise_if_invalid = {self.raise_if_invalid};  \n" +
            f"use_async = {self.use_async}; \n" +
            f"download_folder = {self.download_folder}"
        )


Conf = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences""" # noqa

LOG_FILE = join(Conf.download_folder, ".logs")
"""Full path to the logfile"""

LOG_FMT = "[%(asctime)s] - %(levelname)s::%(name)s - %(message)s"
"""Format string used by the logger"""

LOG_LVL = logging.DEBUG
"""`int` specifying the log level for the `logging` library"""


class LocalLogger():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(
            filename=LOG_FILE
        )
        self.formatter = logging.Formatter(
            fmt=LOG_FMT
        )

        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False

    def debug(self, message):
        self.logger.debug(msg=message)

    def info(self, message):
        self.logger.info(msg=message)

    def warn(self, message):
        self.logger.warn(msg=message)

    def error(self, message):
        self.logger.error(msg=message)

    def critical(self, message):
        self.logger.critical(msg=message)


def set_log_configs():
    global log

    makedirs(split(LOG_FILE)[0], exist_ok=True)
    if not exists(LOG_FILE):
        f = open(LOG_FILE, "x")
        f.close()

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        format=LOG_FMT,
        level=LOG_LVL,
        handlers=[logging.FileHandler(filename=LOG_FILE)]
    )

    log = logging.getLogger()
    log.propagate = False


set_log_configs()
