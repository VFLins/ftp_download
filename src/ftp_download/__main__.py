from . import ensure
from . import timings
from .prefs import Conf

import os
import re
import asyncio
import ftplib  # https://github.com/python/cpython/blob/3.12/Lib/ftplib.py
from typing import Optional, Sequence
from shutil import unpack_archive


def file(
        ftp: ftplib.FTP,
        remote_file_path: str,
        local_path: str = Conf.download_folder
        ) -> None:

    """
    Download a single file from a FTP server. Uses full path to file on the server, and full path to the download directory.

    Can use relative path to the file on the server, if `ftp.cwd('/path/to/folder/')` was called before.

    Args:

    - ftp (`ftplib.FTP`): A `ftplib.FTP` object, expects to be already connected and logged in
    - remote_file_path (`str`):  Full path including filename of the file that will be downloaded
    - local_path (`str`): Full path to local directory where the file will be downloaded, will try to create folder if doesn't exists. Be careful with typos.
    """ # noqa

    ensure.login(ftp=ftp)

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(
            timings.download_task(ftp, remote_file_path, local_path)
        )
    except Exception as xpt:
        print(f"Unexpected error downloading the file:\n{xpt}")
    loop.close()


def from_folder(
        ftp: ftplib.FTP,
        remote_path: str,
        local_path: str = Conf.download_folder,
        stops_with: Optional[int] = None
        ):

    """
    Download multiple files from a folder on a FTP Server.

    Args:

    - ftp (`ftplib.FTP`): An instance of the FTP class;
    - remote_path (`str`): Remote path on FTP server to desired files;
    - local_path (`str`): Local path where files should be dumped;
    - max_concurrent_jobs (`int`): Maximum number of concurrent downloads. Defaults to 20;
    - stops_with (`int` or `None`): If not `None`, defines the maximum amount of files to be downloaded, otherwise download every file in `remote_path`. Defaults to `None`.
    """ # noqa

    ensure.login(ftp=ftp)

    remote_path = ensure.posix_path(remote_path)
    local_path = os.path.normpath(local_path)

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    filenames = ensure.describe_dir(ftp, remote_path)["files"]
    tasks = []
    for idx, filename in enumerate(filenames):

        if Conf.verbose:
            print(f"Processing {idx}/{len(filenames)} files...", end="\r")

        if stops_with == idx:
            break

        remote_file_path = ensure.posix_path(
            os.path.join(remote_path, filename)
        )

        task = timings.download_task(ftp, remote_file_path, local_path)
        tasks.append(task)

    loop.run_until_complete(timings.download_multiple(tasks))

    if Conf.verbose:
        print("Completed!")


# TODO: Remove this soon
def extract_and_organize(
        path: str,
        files_prefixes: Sequence[str] = ["cons", "det"]
        ):

    """
    Looks for sequences of characters on *.zip files, and extract the matched files to the same folder.

    Args:

    - path (`str`): Path to look for .zip files;
    - files_prefixes (`Sequence[str]`): Any list-like with the sequences of charactes to match the file names, each element on the list will produce a folder. Is NOT case sensitive.
    """ # noqa

    def filter_by_pattern(pattern, elements):
        matches = re.compile(pattern, re.IGNORECASE)
        return list(filter(matches.search, elements))

    path_of_files = os.listdir(path)
    listings = {i: filter_by_pattern(i, path_of_files) for i in files_prefixes}

    for prefix in files_prefixes:
        test_path = os.path.join(path, prefix)

        if not os.path.exists(test_path):
            os.makedirs(test_path)

        for f in listings[prefix]:
            destination = os.path.join(test_path, f)
            unpack_archive(f, destination, "zip")
