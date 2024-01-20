# This is `ftp_download`

Utilities to download files from ftp servers with Python.

# Getting started:

`ftp_download` is built upon Python's [`ftplib`](https://docs.python.org/3/library/ftplib.html), an it is a higher level layer specifically made to allow downloads from ftp servers with simple and straightfoward code. 

Here, everything starts with creating an `ftplib.FTP` object:

```
import ftp_download
from ftplib import FTP

ftp = FTP(
    host = "ftp.examplehost.com",
    user = "your_login_name",
    passwd = "your_secure_password",
    acct = "your_account_if_any"
)
```

Then you can start downloading. Here are some examples:

## Download a single file

```
# downloading https://ftp.examplehost.com/example/path/to/file.foo

rfp = "/example/path/to/file.foo"
lp = "/my_download_folder/"

ftp_download.file(ftp=ftp, remote_file_path=rfp, local_path=lp)
```

## Download files from a folder


```
```