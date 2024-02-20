import pytest
from ftplib import FTP, error_perm
from ftp_download.prefs import Conf
from ftp_download.ensure import (
    posix_path,
    describe_dir,
    login
)


@pytest.mark.parametrize(
    "inp,out", [
        ("C:\\path\\to\\something", "/path/to/something"),
        ("C:\\path\\to\\something\\", "/path/to/something"),
        ("/path/to/something", "/path/to/something"),
        ("/path/to/something/", "/path/to/something"),
        ("C:\\", "/"),
        ("/path/to/file.foo", "/path/to/file.foo"),
        ("C:\\path\\to\\file.foo", "/path/to/file.foo")
    ]
)
def test_posix_path(inp, out):
    assert posix_path(inp) == out


@pytest.mark.parametrize(
    "path,out", [
        ("/", {'dirs': ['incoming', 'pub'], 'files': []}),
        ("pub", {'dirs': ['R'], 'files': []}),
        ("/pub/R/html", {'dirs': [], 'files': ['logo.jpg']})
    ]
)
def test_describe_dir(path, out):

    ftp = FTP("cran.r-project.org")
    ftp.login()
    assert out == describe_dir(ftp, path)
    ftp.quit()


@pytest.mark.xfail(raises=error_perm)
def test_describe_dir_fail():
    Conf.__init__()
    Conf.raise_if_invalid = True

    invalid_path = "/wrongpath/"

    ftp = FTP("cran.r-project.org")
    ftp.login()
    describe_dir(ftp, invalid_path)
    ftp.quit()


def test_login():
    Conf.__init__()

    ftp = FTP("cran.r-project.org")
    login(ftp)
    login(ftp)
    ftp.quit()
