import os
import re
import asyncio
import ftplib
from . import ensure 
from config.prefs import Conf
from typing import Optional, Sequence
from shutil import unpack_archive

async def download_file(
        ftp:                ftplib.FTP,
        remote_file_path:   str,
        local_path:         str, 
        semaphore:          asyncio.Semaphore, 
        ):
     
    """
    Creates a task to download a single file from a FTP server. Looks for a "filename.foo" in `local_file_path` and downloads that file from current directory in `ftp`.

    It is intended to be called by `download_from_folder()`.
    
    Args:

    - ftp (`ftplib.FTP`): Should be already placed on desired remote path with files to be downloaded, using `ftplib.FTP.cwd("/the/remote/path")`;
    - local_file_path (`str`):  Full path of where the file will be downloaded;
    - semaphore (`asyncio.Semaphore`): A semaphore to limit the number of concurrent downloads;
    """
    
    remote_path, filename = os.path.split(remote_file_path)

    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    # Create a local file with the same name inside `local_path`
    local_file_path = os.path.join(local_path, filename)
    async with semaphore:
        with open(local_file_path, "wb") as local_file:

            try:
                if Conf.verbose:
                    print(f"Retrieving {filename}...")

                ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)
                
                if Conf.verbose:
                    print(f"File saved: {local_file_path}")

            except Exception as UnexpectedError:
                print(f"Error downloading {filename}:\n{UnexpectedError}")

async def download_from_folder(
        ftp:                    ftplib.FTP, 
        remote_path:            str, 
        local_path:             str, 
        max_concurrent_jobs:    int=20, 
        stops_with:             Optional[int]=None
        ):

    """
    Download multiple files from a folder on a FTP Server.

    Args:

    - ftp (`ftplib.FTP`): An instance of the FTP class;
    - remote_path (`str`): Remote path on FTP server to desired files;
    - local_path (`str`): Local path where files should be dumped;
    - max_concurrent_jobs (`int`): Maximum number of concurrent downloads. Defaults to 20;
    - stops_with (`int` or `None`): If not `None`, defines the maximum amount of files to be downloaded, otherwise download every file in `remote_path`. Defaults to `None`.
    """

    remote_path = ensure.normal_path(remote_path)
    local_path = ensure.normal_path(local_path, as_posix=False)

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    cwd_success = ensure.change_remote_wd(ftp, remote_path)

    semaphore = asyncio.Semaphore(max_concurrent_jobs)
    
    tasks = []
    filenames = ftp.nlst() # TODO: Check filenames and return only files

    if cwd_success:
        for idx, filename in enumerate(filenames):
            remote_filename = os.path.join(local_path, filename)

            if Conf.verbose:
                print(f"Processing {idx} files", end="\r")

            if stops_with and stops_with==idx:
                break

            task = asyncio.create_task(
                download_file(ftp, remote_filename, semaphore)
            )
            tasks.append(task)
            
    await asyncio.gather(*tasks)

    if Conf.verbose:
        print("Completed!")


# TODO: Remove this soon
def extract_and_organize(
        path:           str, 
        files_prefixes: Sequence[str]=["cons", "det"]
        ):
    
    """
    Looks for sequences of characters on *.zip files, and extract the matched files to the same folder.

    Args:

    - path (`str`): Path to look for .zip files;
    - files_prefixes (`Sequence[str]`): Any list-like with the sequences of charactes to match the file names, each element on the list will produce a folder. Is NOT case sensitive.
    """

    def filter_by_pattern(pattern, elements):
        matches = re.compile(pattern, re.IGNORECASE)
        return list(filter(matches.search, elements))

    path_of_files = os.listdir(path)
    listings = {i:filter_by_pattern(i, path_of_files) for i in files_prefixes}

    for prefix in files_prefixes:
        test_path = os.path.join(path, prefix)

        if not os.path.exists(test_path):
            os.makedirs(test_path)

        for f in listings[prefix]:
            destination = os.path.join(test_path, f)
            unpack_archive(f, destination, "zip")
