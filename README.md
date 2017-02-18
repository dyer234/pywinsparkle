
About pywinsparkle
==================

Pywinsparkle is a wrapper for the WinSparkle project originally developed by Vaclav Slavik. WinSparkle is an update framework for Windows. 

The original WinSparkle project is located here: https://winsparkle.org/

github: https://github.com/vslavik/winsparkle

Usage
=====

All of the API function wrapper names are the same as the original WinSparkle project. The only difference
is in the argument types which are either python strings, integers. For the callback, just the function object.

In the pywinsparkle, it is necessary to always specify the application details with the `win_sparkle_set_app_details()` function.
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