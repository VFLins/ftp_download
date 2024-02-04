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

        self.raise_if_invalid: bool = True
        """Raise error if invalid path provided, will only print a message if `False`"""

        self.set_max_concurrent_jobs()
        self.set_default_download_folder()
    
    def __repr__(self):
        return (
            "[Current ftp_download settings]\n" +
            f"verbose = {self.verbose}\n" +
            f"timeout = {self.timeout} seconds\n" +
            f"retry = {self.retry} times\n" +
            f"max_concurrent_jobs = {self.semaphore._value}\n" +
            f"download_folder = {self.download_folder}"
        )
    
    def set_default_download_folder(self, path: str | None=None) -> None:
        """Defines a standard destination path for all downloads.
        
        Args:
        
        - path (`str` or `None`): Path to be used as standard destination, if `None` will set the default value:
        `"~/Downloads/ftp_downloads"` or the OS equivalent
        
        Returns:
        
        `None`"""
        if not path:
            user_folder = os.path.expanduser("~")
            full_path = os.path.join(user_folder, "Downloads", "ftp_downloads")
            normalpath = os.path.normpath(full_path)

        else:
            normalpath = os.path.normpath(path)
        
        setattr(self, "download_folder", normalpath)

    def set_max_concurrent_jobs(self, amount: int | None=None) -> None:
        """Defines a globally used `asyncio.Semaphore` that sets the maximum amount of concurrent downloads.
        
        Args:
        
        - amount (`int` or `None`): Maximum amount of cuncurrent downloads, if `None` will set the default value: 20
        
        Returns:
        
        `None`"""
        if not amount:
            amount = 20

        setattr(self, "semaphore", asyncio.Semaphore(amount))

Conf = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences"""
