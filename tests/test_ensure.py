import pytest
from unittest.mock import mock_open, patch
from ftplib import FTP, error_perm
from ftp_download.prefs import Conf
from ftp_download.ensure import (
    posix_path,
    describe_dir,
    login,
    check_file
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


@pytest.mark.parametrize("file_content, hash_value, hash_type, expected_result", [
    (b"test data", "916f0027a575074ce72a331777c3478d6513f786a591bd892da1a577bf2335f9", "sha256", True),
    (b"test data", "invalid_hash", "sha256", False),
    (b"test data", "eb733a00c0c9d336e65691a37ab54293", "md5", True),
    (b"test data", "invalid_hash", "md5", False),
    (b"test data", "0e1e21ecf105ec853d24d728867ad70613c21663a4693074b2a3619c1bd39d66b588c33723bb466c72424e80e3ca63c249078ab347bab9428500e7ee43059d0d", "sha512", True),
    (b"test data", "invalid_hash", "sha512", False),
])
def test_check_file(file_content, hash_value, hash_type, expected_result):
    with patch("builtins.open", mock_open(read_data=file_content)):
        result = check_file("test.txt", hash_value, hash_type)
    assert result == expected_result