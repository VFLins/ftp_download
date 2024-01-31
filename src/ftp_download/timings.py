import asyncio
import ftplib
import os
from .prefs import Conf

from typing import Callable, Awaitable, List

# Create a local file with the same name inside `local_path`
async def download_task(ftp, remote_file_path, local_path) -> None:
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

async def download_multiple(download_tasks: List[Callable[[Awaitable], None]]) -> None:
    asyncio.gather(*download_task)

async def not_resetable():
    asyncio.sleep(Conf.no_reset_timeout)
    raise ftplib.error_temp(f"Maximum wait time ({Conf.no_reset_timeout} seconds) exceeded")

async def resetable():
    asyncio.sleep(Conf.timeout)
    raise ftplib.error_temp(f"")

def event_loop_available():
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        return False
    else:
        return True