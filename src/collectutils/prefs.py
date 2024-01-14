class global_config_defaults():
    def __init__(self):
        self.verbose = False
        """Should event messages be printed do `stdout`?"""
        self.timeout = 10
        """Time to wait for request responses in seconds"""
        self.retry   = 5
        """Maximum amount of attempts for every request"""

Conf = global_config_defaults()
"""Stores global configuration parameters, change it's parameter values to set your preferences"""
