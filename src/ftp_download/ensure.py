import os
import re
import sys
from io import StringIO
import ftplib
from typing import Dict, List
from config.prefs import Conf
from pathlib import PureWindowsPath

# IMPORTANT: https://kb.globalscape.com/KnowledgebaseArticle10142.aspx

def normal_path(
        path:       str, 
        as_posix:   bool=True
    ) -> str:
    
    """
    Normalizes a path received.

    Should be used with `as_posix=True` (default) to normalize paths compatible usual FTP file systems (unix-like). Otherwise the pathname will be compatible with current running OS.

    Args:

    - path (`str`): The path to be normalized;
    - as_posix (`bool`): If `True`, output will be in posix style, otherwise returns in current OS style (might still be posix). Defaults to `True`.

    Returns:

    A string with path normalized

    """

    is_windows = (os.path.sep == "\\")
    
    if is_windows and as_posix:
        posix_path = PureWindowsPath(path).as_posix()
        swap_driver_for_root = re.compile("[A-Z]:/", re.IGNORECASE)
        return swap_driver_for_root.sub("/", posix_path)
    
    else:
        return os.path.normpath(path)

def change_remote_wd(
        ftp:        ftplib.FTP, 
        path:       str,
        ) ->        bool:
    
    """
    Tries to change directory on remote `ftp` server to `path` and returns a boolean signal indicating operation success.

    Args:

    - ftp (`ftplib.FPT`): An instance of the FTP class, expects to be already connected;
    - path (`str`): FULL remote path targeted;

    Returns:

    `bool` indicating wether the operation was successful or not.
    """

    path = normal_path(path)
    
    for attempt in range(1, Conf.retry+1):
        try:

            if Conf.verbose:
                print(f"connecting to {path}")

            ftp.cwd(path)
            if Conf.verbose:
                print(
                    f"Request completed after {attempt} attempts!"
                    f"Now we are in {path}",
                    sep="\n")
            break

        except ftplib.error_reply as reply:
            if Conf.verbose:
                print(
                    f"Server respnded: {reply}",
                    "Waiting...", sep="\n")
            # TODO: include wait behaviour

        # TODO: support other possible exceptions:
        #        ftplib.error_temp, ftplib.error_perm, ftplib.error_proto, OSError and EOFError
                
        except Exception:
            print("Unexpected error:\n", Exception)

    current_path = normal_path(ftp.pwd())

    return current_path == path

def describe_dir(ftp: ftplib.FTP, path: str) -> Dict[str, List[str]]:

    # Capturing stdout adapted from:
    # https://stackoverflow.com/questions/5136611/capture-stdout-from-a-script

    curr_stdout = sys.stdout
    capturer = StringIO()
    sys.stdout = capturer

    ftp.dir(*path.split("/"))

    sys.stdout = curr_stdout
    return capturer.getvalue().split("\n")[:-1]


