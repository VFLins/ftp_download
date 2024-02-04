import pytest
from ftplib import FTP
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


@pytest.mark.xfail(reason="Might fail due to network issues")
def test_describe_dir():

    ftp = FTP("cdimage.debian.org")
    ftp.login()
    path = "/"
    desc = describe_dir(ftp=ftp, path=path)
    ftp.quit()

    assert len(desc["files"]) == 0
    assert len(desc["dirs"]) == 1


@pytest.mark.xfail(reason="Might fail due to network issues")
def test_login():
    ftp = FTP("cran.r-project.org")
    login(ftp)
    login(ftp)
    ftp.quit()
