import asyncio
import os

class GlobalConfigDefaults():
    def __init__(self):
        self.verbose: bool = False
        """Should event messages be printed do `stdout`?"""

        self.timeout: int = 10
        """Time to wait for request responses in seconds"""

        self.retry: int = 5
        """Maximum amount of attempts for every request"""

        self.set_max_concurrent_jobs(20)
        """`asyncio.Semaphore` object that defines the maximum amount of simultaneous downloads, defaults to 20"""

        self.raise_if_invalid: bool = True
        """Raise error if invalid path provided, will only print a message if `False`"""

        self.download_folder :str = self.set_default_download_folder()
    
    def __repr__(self):
        return (
            "[Current ftp_download settings]\n" +
            f"verbose = {self.verbose}\n" +
            f"timeout = {self.timeout}\n" +
            f"retry = {self.retry}\n" +
            f"max_concurrent_jobs = {self.semaphore._value}\n" +
            f"download_folder = {self.download_folder}"
        )
    
    def set_default_download_folder(self, path: str | None=None) -> str:
        """"""
        if not path:
            user_folder = os.path.expanduser("~")
            setattr(self, "download_folder", os.path.join(user_folder, "Downloads"))
        else:
            setattr(self, "download_folder", path)

    def set_max_concurrent_jobs(self, amount) -> asyncio.Semaphore:
        setattr(self, "semaphore", asyncio.Semaphore(amount))

Configs = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences"""
