import os
import re
import sys
from io import StringIO
import ftplib
from typing import Dict, List
from .prefs import Conf
from pathlib import PureWindowsPath

# IMPORTANT: https://kb.globalscape.com/KnowledgebaseArticle10142.aspx


def posix_path(path: str) -> str:

    """
    Normalizes a path and make compatible usual FTP file systems (unix-like).

    Args:

    - path (`str`): The path to be normalized;

    Returns:

    A `str` with path normalized.
    """ # noqa

    is_windows = (os.path.sep == "\\")

    if is_windows:
        posix_path = PureWindowsPath(path).as_posix()
        swap_drive_letter_for_root = re.compile("[A-Z]:/", re.IGNORECASE)
        return swap_drive_letter_for_root.sub("/", posix_path)

    else:
        return os.path.normpath(path)


def describe_dir(
        ftp: ftplib.FTP,
        path: str = ''
        ) -> Dict[str, List[str]]:

    # Capturing stdout adapted from:
    # https://stackoverflow.com/questions/5136611/capture-stdout-from-a-script

    curr_stdout = sys.stdout
    capturer = StringIO()
    sys.stdout = capturer

    ftp.dir(posix_path(path))

    sys.stdout = curr_stdout
    # Capture stdout as a list
    # Last item is always an empty line
    lines_list = capturer.getvalue().split("\n")[:-1]

    # Will get wrong result if filename or dirname has space " "
    paths = {}
    paths["dirs"] = [i.rpartition(" ")[-1] for i in lines_list if i[0] == "d"]
    paths["files"] = [i.rpartition(" ")[-1] for i in lines_list if i[0] != "d"]

    if len(paths["dirs"]) + len(paths["files"]) == 0:
        error_msg = "Invalid path provided."
        if Conf.raise_if_invalid:
            raise ftplib.error_perm(error_msg)
        else:
            print(error_msg)

    return paths


def login(ftp: ftplib.FTP):
    try:
        ftp.login()
    except ftplib.error_perm as perm_err:
        resp = perm_err.__str__()

        if resp[:3] != "530":
            raise ftplib.error_perm(resp)
