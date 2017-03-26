
About pywinsparkle
==================

Pywinsparkle is a wrapper for the WinSparkle project originally developed by Vaclav Slavik. WinSparkle is an update framework for Windows. 

The original WinSparkle project is located here: https://winsparkle.org/

github: https://github.com/vslavik/winsparkle

Installation
============

`pip install pywinsparkle`

Wheels are built for python 2.7, 3.3, 3.4, 3.5, 3.5, and 3.6.

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


def no_update_found():
    """ when no update has been found, close the updater"""
    print("No update found")
    print("Setting flag to shutdown PassagesUpdater")


def found_update():
    """ log that an update was found """
    print("New Update Available")


def encountered_error():
    print("An error occurred")


def update_cancelled():
    """ when the update was cancelled, close the updater"""
    print("Update was cancelled")
    print("Setting flag to shutdown PassagesUpdater")


def shutdown():
    """ The installer is being launched signal the updater to shutdown """

    # actually shutdown the app here
    print("Safe to shutdown before installing")


def main():

    # register callbacks
    pywinsparkle.win_sparkle_set_did_find_update_callback(found_update)
    pywinsparkle.win_sparkle_set_error_callback(callbacks.encountered_error)
    pywinsparkle.win_sparkle_set_update_cancelled_callback(callbacks.update_cancelled)
    pywinsparkle.win_sparkle_set_did_not_find_update_callback(callbacks.no_update_found)
    pywinsparkle.win_sparkle_set_shutdown_request_callback(callbacks.shutdown)

    # set application details
	update_url = "https://winsparkle.org/example/appcast.xml"
    pywinsparkle.win_sparkle_set_appcast_url(update_url)
    pywinsparkle.win_sparkle_set_app_details("VendorName", "TestApp1", "1.0.0")

    # initialize
    pywinsparkle.win_sparkle_init()

    # check for updates
    pywinsparkle.win_sparkle_check_update_with_ui()

    # alternatively check for updates in the background
    pywinsparkle.win_sparkle_check_update_without_ui()

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