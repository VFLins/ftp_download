from . import ensure
from . import timings
from .prefs import Conf

from os import path, makedirs
import asyncio
import ftplib  # https://github.com/python/cpython/blob/3.12/Lib/ftplib.py
from typing import Optional


def file(
        ftp: ftplib.FTP,
        remote_file_path: str,
        local_path: str = Conf.download_folder
        ) -> None:

    """
    Download a single file from a FTP server. Uses full path to file on the server, and full path to the download directory.

    Can use relative path to the file on the server, if `ftp.cwd('/path/to/folder/')` was called before.

    ### Args:

    - **ftp** (`ftplib.FTP`): A `ftplib.FTP` object, expects to be already connected and logged in
    - **remote_file_path** (`str`):  Full path including filename of the file that will be downloaded
    - **local_path** (`str`): Full path to local directory where the file will be downloaded, defaults to `Conf.download_folder`'s value
    """ # noqa

    ensure.login(ftp=ftp)

    if not path.exists(local_path):
        makedirs(local_path)

    task = timings.download_task(ftp, remote_file_path, local_path)
    Conf.loop.create_task(task)


def from_folder(
        ftp: ftplib.FTP,
        remote_path: str,
        local_path: str = Conf.download_folder,
        stops_with: Optional[int] = None
        ) -> None:

    """
    Download multiple files from a folder on a FTP Server.

    ### Args:

    - **ftp** (`ftplib.FTP`): An instance of the FTP class;
    - **remote_path** (`str`): Remote path on FTP server to desired files;
    - **local_path** (`str`): Local path where files should be dumped;
    - **stops_with** (`int` or `None`): If not `None`, defines the maximum amount of files to be downloaded, otherwise download every file in `remote_path`. Defaults to `None`.
    """ # noqa

    ensure.login(ftp=ftp)

    remote_path = ensure.posix_path(remote_path)
    local_path = path.normpath(local_path)

    if not path.exists(local_path):
        makedirs(local_path)

    filenames = ensure.describe_dir(ftp, remote_path)["files"]
    tasks = []
    for idx, filename in enumerate(filenames):

        if Conf.verbose:
            print(f"Processing {idx}/{len(filenames)} files...", end="\r")

        if stops_with == idx:
            break

        remote_file_path = ensure.posix_path(path.join(remote_path, filename))

        task = timings.download_task(ftp, remote_file_path, local_path)
        Conf.loop.create_task(task)
