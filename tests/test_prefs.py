import logging
from ftp_download.prefs import (
    LocalLogger,
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


def test_local_logger():
    log = LocalLogger()

    assert len(log.logger.handlers) >= 1
    assert type(log.handler) is logging.FileHandler

    assert log.handler.__dict__['baseFilename'] == LOG_FILE
    assert log.handler.level == LOG_LVL
    assert log.handler.formatter._fmt == LOG_FMT

    assert log.logger.getEffectiveLevel() == LOG_LVL
