from ftplib import FTP
import hashlib
import os
import ftp_download


ftp_download.Conf = ftp_download.prefs.GlobalConfigDefaults()


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

    read = file_hash.hexdigest()
    check = "c1c5f6b5f19ee2d8a5d0f9a3c612ae40"

    os.remove(local_file_path)
    ftp.quit()

    assert read == check


def test_from_folder():
    ftp = FTP("cran.r-project.org")
    ftp.login()

    remote_path = "/pub/R/web"
    lp = os.getcwd()
    filenames = ftp_download.ensure.describe_dir(ftp, remote_path)['files']

    ftp_download.from_folder(ftp=ftp, remote_path=remote_path, local_path=lp)

    reads = []
    for filename in filenames:
        local_file_path = os.path.join(lp, filename)
        with open(local_file_path, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read()
            while chunk:
                file_hash.update(chunk)
                chunk = f.read()

        reads.append(file_hash.hexdigest())
        os.remove(local_file_path)

    ftp.quit()

    checks = [
        '2c6ecf143a56da19705976ae315e81f8',
        '9467c77e7a6426087722c0712ed02b17'
    ]
    for read, check in zip(reads, checks):
        assert read == check


def test_file_async():
    ftp_download.Conf.__init__()
    ftp_download.Conf.use_async = True
    test_file()


def test_from_folder_async():
    ftp_download.Conf.__init__()
    ftp_download.Conf.use_async = True
    test_from_folder()
