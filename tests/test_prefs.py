import pytest
from os.path import normpath, expanduser, sep
from asyncio import Semaphore
from ftp_download.prefs import Conf


@pytest.mark.parametrize(
    "amount,out", [
        (1, Semaphore(1)),
        (341, Semaphore(341)),
        (None, Semaphore(20))
    ]
)
def test_set_max_concurrent_jobs(amount, out):

    Conf.set_max_concurrent_jobs(amount=amount)
    assert Conf.semaphore._value == out._value
