import pytest
from ftp_download.ensure import normal_path

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