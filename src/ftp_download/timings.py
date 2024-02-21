from .prefs import Conf, LocalLogger

import os
import ftplib
import asyncio
import types


log = LocalLogger()


def blocking_download_task(
        ftp: ftplib.FTP,
        remote_file_path: str,
        local_path: str
        ) -> None:

    """
    Sychronous version of `download_task()`.

    ### Args:

    - **ftp** (`ftplib.FTP`): `ftplib.FTP` object logged in to the server that houses the file to be downloaded
    - **remote_file_path** (`str`): path to the file on the remote server
    - **local_path** (`str`): path to local folder where the file will be downloaded
    """ # noqa

    filename = os.path.split(remote_file_path)[1]
    local_file_path = os.path.join(local_path, filename)

    if Conf.verbose:
        print(f"Retrieving {filename}...")
    log.debug(
        f"Trying to download {ftp.__dict__['host']}" +
        f"{remote_file_path} with blocking task"
    )

    with open(local_file_path, "wb") as local_file:

        try:
            ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)

            if Conf.verbose:
                print(f"File saved: {local_file_path}")
            log.info(f"File saved: {local_file_path}")

        except Exception as UnexpectedError:
            log.error(f"Could not download {filename}:\n{UnexpectedError}")
            print(f"Could not download {filename}:\n{UnexpectedError}")


async def download_task(
        ftp: ftplib.FTP,
        remote_file_path: str,
        local_path: str
        ) -> None:

    """
    Asynchronous task that downloads a single file. Create a local file with the same filename found in `remote_file_path` inside `local_path`.

    ### Args:

    - **ftp** (`ftplib.FTP`): `ftplib.FTP` object logged in to the server that houses the file to be downloaded
    - **remote_file_path** (`str`): path to the file on the remote server
    - **local_path** (`str`): path to local folder where the file will be downloaded
    """ # noqa

    filename = os.path.split(remote_file_path)[1]
    local_file_path = os.path.join(local_path, filename)

    if Conf.verbose:
        print(f"Retrieving {filename}...")
    log.debug(
        f"Trying to download {ftp.__dict__['host']}" +
        f"{remote_file_path} with async task"
    )

    with open(local_file_path, "wb") as local_file:

        try:
            ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)

            if Conf.verbose:
                print(f"File saved: {local_file_path}")
            log.info(f"File saved: {local_file_path}")

        except Exception as UnexpectedError:
            log.error(f"Could not download {filename}:\n{UnexpectedError}")
            print(f"Could not download {filename}:\n{UnexpectedError}")


async def run_multiple(tasks: list) -> None:
    for task in tasks:
        await task


def run(coro):

    """
    Emulate asyncio.run() on older versions

    Adapted from:
    https://stackoverflow.com/questions/55590343/asyncio-run-or-run-until-complete
    """ # noqa 

    if not isinstance(coro, types.CoroutineType):
        raise TypeError("run() requires a coroutine object")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
        asyncio.set_event_loop(None)
