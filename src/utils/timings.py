import asyncio
import ftplib
from ftp_download.prefs import Conf

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