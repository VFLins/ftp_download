import ftplib
import asyncio
from . import timings
from dataclasses import dataclass
from config.prefs import Conf
from typing import Union

# IMPORTANT: https://docs.python.org/3/library/ftplib.html#ftplib.all_errors
#            https://github.com/python/cpython/blob/v2.7.16/Lib/ftplib.py#L202
#            https://kb.globalscape.com/KnowledgebaseArticle10142.aspx

# TODO: support all possible exceptions:
#       ftplib.error_reply, ftplib.error_temp, ftplib.error_perm, ftplib.error_proto, OSError and EOFError

@dataclass
class CheckInputError(Exception):
    message: str = "Check the url requested, or if you have available space on disk for this download."

    def __str__(self):
        return f"[CheckInputError] {self.message}"
    
@dataclass
class NetworkError(Exception):
    message: str = "Timed out trying to retrieve file, check your conection or if the server is available."

    def __str__(self):
        return f"[NetworkError] {self.message}"

check_input_error = (ftplib.error_perm, OSError, EOFError)

async def all(ftp, error):
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

        try:
            return (ftp, ftp.getresp())
        except check_input_error as inp_error:
            return (ftp, inp_error)
        except ftplib.error_proto as unexpec:
            print("Unexpected error")



        


def error_code(ftp):
    msg = ftp.getmultiline()