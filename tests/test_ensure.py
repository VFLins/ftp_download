import pytest
from ftplib import FTP, error_temp
from ftp_download.ensure import (
    normal_path,
    describe_dir,
    login
)

@pytest.mark.parametrize(
    "inp,out,as_posix", [
    ("C:\\path\\to\\something", "/path/to/something", True),
    ("C:\\path\\to\\something\\", "/path/to/something", True),
    ("/path/to/something", "/path/to/something", True),
    ("/path/to/something/", "/path/to/something", True),
    ("C:\\", "/", True),
    ("/path/to/file.foo" , "/path/to/file.foo", True),
    ("C:\\path\\to\\file.foo", "/path/to/file.foo", True)]
)
def test_normal_path(inp, out, as_posix):
    assert normal_path(inp, as_posix) == out

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

