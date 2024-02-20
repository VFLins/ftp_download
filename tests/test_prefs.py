import pytest
from os.path import normpath, expanduser, sep
import logging
from ftp_download.prefs import (
    Conf,
    set_log_configs,
    LOG_FILE,
    LOG_FMT,
    LOG_LVL
)


""" @pytest.mark.parametrize(
    "amount,out", [
        (1, Semaphore(1)),
        (341, Semaphore(341)),
        (None, Semaphore(20))
    ]
)
def test_set_max_concurrent_jobs(amount, out):

    Conf.set_max_concurrent_jobs(amount=amount)
    assert Conf.semaphore._value == out._value
 """


""" def test_set_log_configs():
    set_log_configs()
    log = logging.getLogger(__name__)
    
    logging.RootLogger.ha

    assert log.getEffectiveLevel() == LOG_LVL
    assert log.hasHandlers() == True
"""
