import pytest
from ftplib import FTP
import hashlib
import os
import ftp_download


@pytest.mark.xfail(reason="Might fail due to network issues")
def test_file():

    ftp = FTP("cran.r-project.org")
    ftp.login()

    lp = os.getcwd()
    remote_file_path = "/pub/R/CRANlogo.png"
    filename = os.path.split(remote_file_path)[1]

    ftp_download.file(ftp, remote_file_path=remote_file_path, local_path=lp)

    # get hash adapted from: https://stackoverflow.com
    # /questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python

    local_file_path = os.path.join(lp, filename)
    with open(local_file_path, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read()
        while chunk:
            file_hash.update(chunk)
            chunk = f.read()

    md5read = file_hash.hexdigest()
    md5check = "c1c5f6b5f19ee2d8a5d0f9a3c612ae40"

    os.remove(local_file_path)
    assert md5read == md5check
