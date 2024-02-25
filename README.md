![Project banner](docs/gh_banner.png)

Easily download files from ftp servers!

![Tests](https://github.com/VFLins/ftp_download/actions/workflows/tests.yml/badge.svg)
<a href="https://vflins.github.io/ftp_download/docs/ftp_download.html" ><img alt="Static Badge" src="https://img.shields.io/badge/documentation%20-%20vflins.github.io%20-%20blue?logo=github&color=blue">
</a>

# Installation

Install from PyPI using `pip`:

```
pip install ftp_download
```

# Getting started:

`ftp_download` is built upon Python's [`ftplib`](https://docs.python.org/3/library/ftplib.html), an it is a higher level interface made to allow downloads from ftp servers with simple and straightfoward code. 

Here, everything starts with creating an `ftplib.FTP` object:

```
from ftplib import FTP

ftp = FTP(
    host = "ftp.examplehost.com",
    user = "your_login_name",
    passwd = "your_secure_password",
    acct = "your_account_if_any"
)
```

Then you can start downloading. **Here are some examples:**

### Download a single file

For the examples here we will go with:

```
import ftp_download as ftpd
from ftplib import FTP
import os

ftp = FTP("cran.r-project.org")
```

To download a file we can do this:

```
# downloading /pub/R/CRANlogo.png 
# from cran.r-project.org

rp = "/pub/R/CRANlogo.png"
lp = os.path.expanduser("~") # Download to user folder

ftpd.file(ftp, remote_file_path=rp, local_path=lp)
```

Notice that `local_path` was specified, but if not, `ftp_download` will save the files in `{user_folder}/Downloads/ftp_download`.

### Download files from a folder

You can also give a path to a folder and download everything from there, notice that this is not recursive, and will get only the files at the top level of `remote_path`.

```
rp = "/pub/R/web"
lp = os.path.expanduser("~") # Download to user folder

ftpd.from_folder(ftp, remote_path=rp, local_path=lp)
```

It's also important to notice that currently, `ftp_download` will not create a "web" folder on the `local_path` specified.

### Important configurations

`ftp_download` will have a standard behavior that can be tweaked by changing the default values of `ftp_download.Conf`:

```
import ftp_download as ftpd

# To stop printing event messages to stdout (default: True)
ftpd.Conf.verbose = False

# To change the standard download path (default: {user_folder}/Downloads/ftp_download)
ftpd.Conf.download_folder = "C:\\my\\custom\\path"

# To change the maximum amount of concurrent downloads (default: 20)
ftpd.Conf.set_max_concurrent_jobs(300)
```

For more information, read the [documentation](https://vflins.github.io/ftp_download/docs/ftp_download/prefs.html).
