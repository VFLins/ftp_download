import pytest
from python_scripts.collectutils.ensure import normal_path

@pytest.mark.parametrize(
        "inp,out,as_posix", [
        ("C:\\path\\to\\something", "/path/to/something", True),
        ("C:\\path\\to\\something\\", "/path/to/something", True),
        ("/path/to/something", "/path/to/something", True),
        ("/path/to/something/", "/path/to/something", True),
        ("C:\\", "/", True)
    ]
)
def test_normal_path(inp, out, as_posix):
    assert normal_path(inp, as_posix) == out