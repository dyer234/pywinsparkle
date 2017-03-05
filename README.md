
About pywinsparkle
==================

Pywinsparkle is a wrapper for the WinSparkle project originally developed by Vaclav Slavik. WinSparkle is an update framework for Windows. 

The original WinSparkle project is located here: https://winsparkle.org/

github: https://github.com/vslavik/winsparkle

Installation
============

`pip install pywinsparkle`

Wheels are built for python 2.7, 3.4 (64bit), and 3.5 (32bit). I'll be working on getting more uniform wheel coverage
soon.

Note: If you are using one of the above versions and the version is listed on pypi at: https://pypi.python.org/pypi?:action=display&name=pywinsparkle

Consider upgrading pip with `pip install --upgrade pip`


Usage
=====

All of the API function wrapper names are the same as the original WinSparkle project. The only difference
is in the argument types which are either python strings or integers. For the callback functions, just the function
object is required (ie, the name of the function without the parenthesis).

In pywinsparkle, it is necessary to always specify the application details with the `win_sparkle_set_app_details()` function.
It is also necessary to set the appcast url with `win_sparkle_set_appcast_url()` (This is a distinction in between pywinsparkle and WinSparkle).

Basic Example
============= 

```python
from pywinsparkle import pywinsparkle


def get_version():
    return "1.0.0"


def found_update():
    print("callback: found an update")


def main():

    # register callbacks
    pywinsparkle.win_sparkle_set_did_find_update_callback(found_update)

    # set application details
	update_url = "https://winsparkle.org/example/appcast.xml"
    pywinsparkle.win_sparkle_set_appcast_url(update_url)
    pywinsparkle.win_sparkle_set_app_details("VendorName", "TestApp1", get_version())

    # initialize
    pywinsparkle.win_sparkle_init()

    # check for updates
    pywinsparkle.win_sparkle_check_update_with_ui()

	# dont do it this way, just an example to keep the thread running
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
```

Freezing with Pyinstaller
=========================

Currently requires you to add an entry to .SPEC in Analysis for binaries. I haven't worked out why the auto discovery
isn't working yet.

Assuming you are using a virtual environment and it is called "venv" it would look like this:

```python

import platform

if architecture == "64bit":
    winsparkle = 'venv\\Lib\\site-packages\\pywinsparkle\\libs\\x64\\WinSparkle.dll'
else:
    winsparkle = 'venv\\Lib\\site-packages\\pywinsparkle\\libs\\x86\\WinSparkle.dll'

a = Analysis(['PassagesUpdater\\src\\main.py'],
             pathex=['.'],
             binaries=[(winsparkle, '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
```