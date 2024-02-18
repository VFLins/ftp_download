import asyncio
import logging
from os.path import join, expanduser, exists
from os import makedirs


class GlobalConfigDefaults:
    def __init__(self):
        self.verbose: bool = True
        """Should event messages be printed do `stdout`?"""

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
            f"max_concurrent_jobs = {self.semaphore._value}; \n" +
            f"download_folder = {self.download_folder}"
        )

    def set_max_concurrent_jobs(self, amount: int = 20) -> None:

        """
        Defines a globally used `asyncio.Semaphore` that sets the maximum amount of concurrent downloads.
        
        ### Args:
        
        - **amount** (`int`): Maximum amount of cuncurrent downloads, defaults to `20`
        """ # noqa

        if not amount:
            amount = 20

        setattr(self, "semaphore", asyncio.Semaphore(amount))

    def reset_event_loop(self) -> None:

        """
        Replaces the current event loop if it is closed
        """
        if self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
        else:
            try:
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()


Conf = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences""" # noqa

LOG_PLACE = join(Conf.download_folder, "log.txt")
makedirs(Conf.download_folder, exist_ok=True)
if not exists(LOG_PLACE):
    f = open(LOG_PLACE, "x")
    f.close()

def set_log_configs():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename=LOG_PLACE,
        format="[%(asctime)s] - %(name)s::%(levelname)s - %(message)s",
        level=logging.DEBUG
    )
set_log_configs()
""" 
fmt = logging.Formatter(
    "[%(asctime)s] - %(name)s::%(levelname)s - %(message)s")
hdl = logging.FileHandler(filename=LOG_PLACE)
hdl.setFormatter(fmt)
hdl.setLevel(logging.DEBUG) """
