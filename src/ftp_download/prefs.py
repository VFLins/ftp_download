from dataclasses import dataclass
import asyncio
import os

class GlobalConfigDefaults():
    def __init__(self):
        self.verbose: bool=False
        """Should event messages be printed do `stdout`?"""

        self.timeout: int=10
        """Time to wait for request responses in seconds"""

        self.retry: int=5
        """Maximum amount of attempts for every request"""

        self.semaphore = asyncio.Semaphore(20)
        """`asyncio.Semaphore` object that defines the maximum amount of simultaneous downloads"""

        self.raise_if_invalid: bool = True
        """Raise error if invalid path provided, just print a message if `False`"""

        self.download_folder :str = self.get_default_download_folder()
    
    def __repr__(self):
        return f"""
        Current settings are:

        verbose: {self.verbose}
        timeout time (s): {self.timeout}
        retry (amount): {self.retry}
        """
    
    def get_default_download_folder(self) -> str:
        user_folder = os.path.expanduser("~")
        return os.path.join(user_folder, "Downloads")

    


Conf = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences"""
