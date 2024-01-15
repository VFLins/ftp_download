from dataclasses import dataclass

@dataclass
class GlobalConfigDefaults:
    verbose: bool=False
    """Should event messages be printed do `stdout`?"""
    timeout: int=10
    """Time to wait for request responses in seconds"""
    no_reset_timeout: int=60
    """Some server responses will reset the `GlobalConfigDefaults.timeout`, this is the maximum amount of wait time, despite the timeout resets in seconds"""
    retry: int=5
    """Maximum amount of attempts for every request"""

Conf = GlobalConfigDefaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences"""
