import ftplib
import asyncio
from . import timings
from config.prefs import Conf
from typing import Union

# IMPORTANT: https://docs.python.org/3/library/ftplib.html#ftplib.all_errors
#            https://github.com/python/cpython/blob/v2.7.16/Lib/ftplib.py#L202
#            https://kb.globalscape.com/KnowledgebaseArticle10142.aspx

# TODO: support all possible exceptions:
#       ftplib.error_reply, ftplib.error_temp, ftplib.error_perm, ftplib.error_proto, OSError and EOFError

def all(ftp, error):
    """
    Delivers the error message received to appropriate error handler based on type.
    Errors 
    """
    pass

async def reply(
        ftp:    ftplib.FTP,
        error:  ftplib.error_reply
        ) -> Union[ftplib.error_temp, ftplib.error_perm, ftplib.error_proto]:

    """
    Will keep waiting for next responses from the server until recieve another type of error or timeout. Getting another code of `ftplib.error_reply` will reset the timeout, in this case the maximum waiting time will be `Conf.no_reset_timeout`.

    Args:

    - ftp (`ftplib.FPT`): An instance of the FTP class
    - error (`ftplib.error_reply`): An `ftplib.error_reply` exception

    Return:

    One of ftplib.error_temp, ftplib.error_perm, ftplib.error_proto, or a '200' class response.
    """
    
    while True:
        if timings.event_loop_available():
            await timings.not_resetable()
        else:
            asyncio.run(timings.not_resetable())

        


def error_code(ftp):
    msg = ftp.getmultiline()