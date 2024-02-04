import asyncio
import os
import ftplib
from .prefs import Conf
from typing import Callable, Awaitable, List


# Create a local file with the same name inside `local_path`
async def download_task(
        ftp: ftplib.FTP,
        remote_file_path: str,
        local_path: str
        ) -> None:
    """
    Asynchronous task that downloads a single file.

    ### Args:

    - **ftp** (`ftplib.FTP`): `ftplib.FTP` object logged in to the server that houses the file to be downloaded
    - **remote_file_path** (`str`): path to the file on the remote server
    - **local_path** (`str`): path to local folder where the file will be downloaded
    """ # noqa

    remote_path, filename = os.path.split(remote_file_path)
    local_file_path = os.path.join(local_path, filename)

    async with Conf.semaphore:
        with open(local_file_path, "wb") as local_file:

            try:
                if Conf.verbose:
                    print(f"Retrieving {filename}...")

                ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)

                if Conf.verbose:
                    print(f"File saved: {local_file_path}")

            except Exception as UnexpectedError:
                print(f"Error downloading {filename}:\n{UnexpectedError}")


async def download_multiple(
        download_tasks: List[Callable[[Awaitable], None]]
        ) -> None:
    """
    Runs multiple downloads asynchronously, it's meant to be called by `ftp_download.from_folder()`

    ### Args:

    - **download_tasks** (`list(awaitables)`): List of `ftp_download.timings.download_task()`
    """  # noqa

    await asyncio.gather(*download_tasks)
