import asyncio
from os.path import join, expanduser


class GlobalConfigDefaults:
    def __init__(self):
        self.verbose: bool = True
        """Should event messages be printed do `stdout`?"""

        self.timeout: int = 10
        """Time to wait for request responses in seconds (unused yet)"""

        self.retry: int = 5
        """Maximum amount of attempts for every request (unused yet)"""

        self.raise_if_invalid: bool = True
        """Shoud stop if an error is encountered? If `False` it will just print a message (unused yet)""" # noqa

        self.use_async: bool = False
        """Should send asynchronous download requests? If `True` it might get faster downloads, but will be incompatible with Jupyter Notebooks and some implementations of GUI applications."""

        self.download_folder: str = join(
            expanduser("~"), "Downloads", "ftp_download"
        )
        """Standard destination path for all downloads"""

        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
        """Get running event loop or create new with `asyncio`"""

        self.set_max_concurrent_jobs()

    def __repr__(self):
        return (
            "FTP_DOWLOAD SETTINGS: \n" +
            f"verbose = {self.verbose}; \n" +
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


Conf = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences""" # noqa
