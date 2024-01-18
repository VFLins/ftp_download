from dataclasses import dataclass

@dataclass
class GlobalConfigDefaults:
    verbose: bool=False
    """Should event messages be printed do `stdout`?"""
    timeout: int=10
    """Time to wait for request responses in seconds"""
    retry: int=5
    """Maximum amount of attempts for every request"""
    raise_if_invalid: bool=True
    """Raise error if invalid path provided, just print a message if `False`"""

Conf = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences"""
