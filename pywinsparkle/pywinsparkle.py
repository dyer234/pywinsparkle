""" A wrapper for the WinSparkle project

"""
from ctypes import cdll, c_char_p, c_wchar_p, c_int16, c_int64, CFUNCTYPE
import os
import sys
import platform

# this python is 64bit or 32bit? Need to know to choose the right library to load
architecture, _ = platform.architecture()
if architecture == "64bit":
    LIB_FOLDER = "libs" + os.sep + "x64"
elif architecture == "32bit":
    LIB_FOLDER = "libs" + os.sep + "x86"


# compatibility with pyinstaller, else running live
if getattr( sys, 'frozen', False ):
    THIS_DIRECTORY = sys._MEIPASS
    DLL_FILE = os.path.join(THIS_DIRECTORY, "WinSparkle")

else:
    THIS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    DLL_FILE = os.path.join(THIS_DIRECTORY, LIB_FOLDER, "WinSparkle")


# documentation and wheel creation is done on linux, if this is linux then
# dont try and load the DLL.
if os.name == "nt":
    dll = cdll.LoadLibrary(DLL_FILE)
else:
    dll = None

def win_sparkle_init():
    """ Starts WinSparkle.

    If WinSparkle is configured to check for updates on startup, proceeds
    to perform the check. You should only call this function when your app
    is initialized and shows its main window.

    @note This call doesn't block and returns almost immediately. If an
          update is available, the respective UI is shown later from a separate
          thread.

    """
    dll.win_sparkle_init.restype = None
    dll.win_sparkle_init()


def win_sparkle_cleanup():
    """ Cleans up after WinSparkle.

    Should be called by the app when it's shutting down. Cancels any
    pending Sparkle operations and shuts down its helper threads.

    """

    dll.win_sparkle_cleanup.restype = None
    dll.win_sparkle_cleanup()


def win_sparkle_set_lang(language):
    """ Sets UI language from its Win32 LANGID code.
    
    This function must be called before win_sparkle_init().
    :param language: An int, Language code (LANGID) as created by the MAKELANGID macro
    or returned by e.g. ::GetThreadUILanguage()
    """

    dll.win_sparkle_set_lang.restype = None
    dll.win_sparkle_set_lang.argtypes = [c_int16]
    dll.win_sparkle_set_lang(language)


def win_sparkle_set_appcast_url(url):
    """  Sets URL for the app's appcast. Only http and https schemes are supported.

    If this function isn't called by the app, the URL is obtained from
    Windows resource named "FeedURL" of type "APPCAST".

    note: Always use HTTPS feeds, do not use unencrypted HTTP! This is
          necessary to prevent both leaking user information and preventing
          various MITM attacks.

    :param url: URL of the appcast.
    """

    dll.win_sparkle_set_appcast_url.restype = None
    dll.win_sparkle_set_appcast_url.argtypes = [c_char_p]
    dll.win_sparkle_set_appcast_url(url.encode())


def win_sparkle_set_app_details(company_name, app_name, app_version):
    """ Sets application metadata.

    Normally, these are taken from VERSIONINFO/StringFileInfo resources,
    but if your application doesn't use them for some reason, using this
    function is an alternative.

    note  company_name and app_name are used to determine the location
          of WinSparkle settings in registry.
          (HKCU\Software\<company_name>\<app_name>\WinSparkle is used.)

    :param company_name: Company name of the vendor.
    :param app_name: Application name. This is both shown to the user
                         and used in HTTP User-Agent header
    :param app_version: Version of the app, as string (e.g. "1.2" or "1.2rc1").
    """

    dll.win_sparkle_set_app_details.restype = None
    dll.win_sparkle_set_app_details.argtypes = [c_wchar_p, c_wchar_p, c_wchar_p]
    dll.win_sparkle_set_app_details(company_name, app_name, app_version)


def win_sparkle_set_app_build_version(build_number):
    """ Sets application build version number.

    This is the internal version number that is not normally shown to the user.
    It can be used for finer granularity that official release versions, e.g. for
    interim builds.

    If this function is called, then the provided *build* number is used for comparing
    versions; it is compared to the "version" attribute in the appcast and corresponds
    to OS X Sparkle's CFBundleVersion handling. If used, then the appcast must
    also contain the "shortVersionString" attribute with human-readable display
    version string. The version passed to win_sparkle_set_app_details()
    corresponds to this and is used for display.

    :param build_number: the build number (as string)
    """

    dll.win_sparkle_set_app_build_version.restype = None
    dll.win_sparkle_set_app_build_version.argtypes = [c_wchar_p]
    dll.win_sparkle_set_app_build_version(build_number)


def win_sparkle_set_registry_path(registry_path):
    """ Set the registry path where settings will be stored.

    Normally, these are stored in
    "HKCU\Software\<company_name>\<app_name>\WinSparkle"
    but if your application needs to store the data elsewhere for
    some reason, using this function is an alternative.

    Note that @a path is relative to HKCU/HKLM root and the root is not part
    of it. For example:
    example:
    win_sparkle_set_registry_path("Software\\My App\\Updates");

    :param registry_path: Registry path where settings will be stored.
    """

    dll.win_sparkle_set_registry_path.restype = None
    dll.win_sparkle_set_registry_path.argtypes = [c_wchar_p]
    dll.win_sparkle_set_registry_path(registry_path)


def win_sparkle_set_automatic_check_for_updates(update_state):
    """ Sets whether updates are checked automatically or only through a manual call.
    If disabled, win_sparkle_check_update_with_ui() must be used explicitly.

    :param update_state: 1 to have updates checked automatically, 0 otherwise
    """

    dll.win_sparkle_set_automatic_check_for_updates.restype = None
    dll.win_sparkle_set_automatic_check_for_updates.argtypes = [c_int64]
    dll.win_sparkle_set_automatic_check_for_updates(update_state)


def win_sparkle_set_update_check_interval(interval):
    """ Sets the automatic update interval.

    :param interval: interval The interval in seconds between checks for updates.
                     The minimum update interval is 3600 seconds (1 hour).
    """

    dll.win_sparkle_set_update_check_interval.restype = None
    dll.win_sparkle_set_update_check_interval.argtypes = [c_int64]
    dll.win_sparkle_set_update_check_interval(interval)


def win_sparkle_get_update_check_interval():
    """ Gets the time for the last update check.

    Default value is -1, indicating that the update check has never run.

    """

    dll.win_sparkle_get_update_check_interval.restype = c_int64
    dll.win_sparkle_get_update_check_interval.argtypes = None
    result = dll.win_sparkle_get_update_check_interval()

    return result


def win_sparkle_get_last_check_time():
    """ Gets the time for the last update check.

    Default value is -1, indicating that the update check has never run.

    :return: Time in seconds since unix epoch
    """

    dll.win_sparkle_get_last_check_time.restype = c_int64
    dll.win_sparkle_get_last_check_time.argtypes = [None]
    result = dll.win_sparkle_get_last_check_time()

    return result


def win_sparkle_set_error_callback(app_callback):
    """ Set callback to be called when the updater encounters an error.

    :param app_callback: The function name that should called
    """

    me = win_sparkle_set_error_callback
    callback_function = _callback_function_helper(me, app_callback)

    dll.win_sparkle_set_error_callback.restype = None
    dll.win_sparkle_set_error_callback.argytpes = []
    dll.win_sparkle_set_error_callback(callback_function)


def win_sparkle_set_can_shutdown_callback(app_callback):
    """ Set callback for querying the application if it can be closed.

    This callback will be called to ask the host if it's ready to shut down,
    before attempting to launch the installer. The callback returns TRUE if
    the host application can be safely shut down or FALSE if not (e.g. because
    the user has unsaved documents).

    Note: There's no guarantee about the thread from which the callback is called,
          except that it certainly *won't* be called from the app's main thread.
          Make sure the callback is thread-safe.

    :param app_callback: The function name that should called
    """

    me = win_sparkle_set_can_shutdown_callback
    callback_function = _callback_function_helper(me, app_callback)

    dll.win_sparkle_set_can_shutdown_callback.restype = None
    dll.win_sparkle_set_can_shutdown_callback.argtypes = []
    dll.win_sparkle_set_can_shutdown_callback(callback_function)


def win_sparkle_set_shutdown_request_callback(app_callback):
    """ Set callback for shutting down the application.

    This callback will be called to ask the host to shut down immediately after
    launching the installer. Its implementation should gracefully terminate the
    application.

    It will only be called if the call to the callback set with
    win_sparkle_set_can_shutdown_callback() returns TRUE.

    @note There's no guarantee about the thread from which the callback is called,
          except that it certainly *won't* be called from the app's main thread.
          Make sure the callback is thread-safe.

    :param app_callback: The function name that should called
    """

    me = win_sparkle_set_shutdown_request_callback
    callback_function = _callback_function_helper(me, app_callback)

    dll.win_sparkle_set_shutdown_request_callback.restype = None
    dll.win_sparkle_set_shutdown_request_callback.argtypes = []
    dll.win_sparkle_set_shutdown_request_callback(callback_function)


def win_sparkle_set_did_find_update_callback(app_callback):
    """ Set callback to be called when the updater did find an update.

    This is useful in combination with
    win_sparkle_check_update_with_ui_and_install() as it allows you to perform
    some action after WinSparkle checks for updates.

    :param app_callback: The function name that should called
    """

    me = win_sparkle_check_update_with_ui
    callback_function = _callback_function_helper(me, app_callback)

    dll.win_sparkle_set_did_find_update_callback.restype = None
    dll.win_sparkle_set_did_find_update_callback.argtypes = []
    dll.win_sparkle_set_did_find_update_callback(callback_function)


def win_sparkle_set_did_not_find_update_callback(app_callback):
    """ Set callback to be called when the updater did not find an update.

    This is useful in combination with
    win_sparkle_check_update_with_ui_and_install() as it allows you to perform
    some action after WinSparkle checks for updates.

    :param app_callback: The function name that should called
    """

    me = win_sparkle_set_did_not_find_update_callback
    callback_function = _callback_function_helper(me, app_callback)

    dll.win_sparkle_set_did_not_find_update_callback.restype = None
    dll.win_sparkle_set_did_not_find_update_callback.argtypes = []
    dll.win_sparkle_set_did_not_find_update_callback(callback_function)


def win_sparkle_set_update_cancelled_callback(app_callback):
    """ Set callback to be called when the user cancels a download.

    This is useful in combination with
    win_sparkle_check_update_with_ui_and_install() as it allows you to perform
    some action when the installation is interrupted.

    :param app_callback: The function name that should called
    """

    me = win_sparkle_set_update_cancelled_callback
    callback_fucntion = _callback_function_helper(me, app_callback)
    dll.win_sparkle_set_update_cancelled_callback.restype = None
    dll.win_sparkle_set_update_cancelled_callback.argtypes = []
    dll.win_sparkle_set_update_cancelled_callback(callback_fucntion)

def _callback_function_helper(wrapper_function, user_callback_funcion):
    """ A helper function and should not be used outside the module.

    When declaring these function pointers inside the wraper function, it is
    necessary to store a reference somewhere or else it will be garbage collected.
    If anything tries to use it after that, then it will crash. To Prevent this,
    a reference is stored inside the function attributes similar to a c++ function
    static variable. This also prevents the need to store it globally.

    :param wrapper_function:
    :param user_callback_funcion:
    """

    prototype = CFUNCTYPE(None)
    callback_function = prototype(user_callback_funcion)

    # store reference to function inside function attributes
    if not hasattr(wrapper_function, "callback_function"):
        wrapper_function.callback_function = None

    wrapper_function.callback_function = callback_function

    return wrapper_function.callback_function


def win_sparkle_check_update_with_ui():
    """ Checks if an update is available, showing progress UI to the user.

    Normally, WinSparkle checks for updates on startup and only shows its UI
    when it finds an update. If the application disables this behavior, it
    can hook this function to "Check for updates..." menu item.

    When called, background thread is started to check for updates. A small
    window is shown to let the user know the progress. If no update is found,
    the user is told so. If there is an update, the usual "update available"
    window is shown.

    This function returns immediately.
    """

    dll.win_sparkle_check_update_with_ui.restype = None
    dll.win_sparkle_check_update_with_ui()


def win_sparkle_check_update_with_ui_and_install():
    """ Checks if an update is available, showing progress UI to the user and
    immediately installing the update if one is available.

    This is useful for the case when users should almost always use the
    newest version of your software. When called, WinSparkle will check for
    updates showing a progress UI to the user. If an update is found the update
    prompt will be skipped and the update will be installed immediately.

    If your application expects to do something after checking for updates you
    may wish to use win_sparkle_set_did_not_find_update_callback() and
    win_sparkle_set_update_cancelled_callback().

    """

    dll.win_sparkle_check_update_with_ui_and_install.restype = None
    dll.win_sparkle_check_update_with_ui_and_install()


def win_sparkle_check_update_without_ui():
    """ Checks if an update is available.

    No progress UI is shown to the user when checking. If an update is
    available, the usual "update available" window is shown; this function
    is *not* completely UI-less.

    Use with caution, it usually makes more sense to use the automatic update
    checks on interval option or manual check with visible UI.

    This function returns immediately.
    """

    dll.win_sparkle_check_update_without_ui.restype = None
    dll.win_sparkle_check_update_without_ui()
