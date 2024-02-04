import pytest
from os.path import normpath, expanduser, sep
from asyncio import Semaphore
from ftp_download.prefs import Conf


@pytest.mark.parametrize(
    "inp,win_val,posix_val", [
        (
            "C:\\path\\to\\something",
            "C:\\path\\to\\something",
            "/path/to/something"
        ),
        (
            "C:\\path\\to\\something\\",
            "C:\\path\\to\\something",
            "/path/to/something"
        ),
        (
            "/path/to/something",
            "\\path\\to\\something",
            "/path/to/something"
        ),
        (
            "C:\\",
            "C:\\",
            "C:/"
        ),
        (
            None,
            normpath(expanduser("~/Downloads/ftp_downloads")),
            normpath(expanduser("~/Downloads/ftp_downloads"))
        )
    ]
)
def test_set_default_download_folder(inp, win_val, posix_val):

    Conf.set_default_download_folder(inp)
    if sep == "\\":
        assert Conf.download_folder == win_val

    else:
        assert Conf.download_folder == posix_val


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
