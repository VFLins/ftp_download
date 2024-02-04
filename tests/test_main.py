import pytest
from ftp_download import (
    file, 
    from_folder
)


@pytest.mark.xfail(reason="Might fail due to network issues")
def test_file():
    pass
