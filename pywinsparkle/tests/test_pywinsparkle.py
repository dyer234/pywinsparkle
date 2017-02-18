import unittest
from .. import pywinsparkle
from pywinauto import Application
import time
from threading import Thread
import requests
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor


VENDOR = "MY_VENDOR"
APP_NAME = "TEST_APP!"
VERSION = "1.0.0"

PORT = 9590
APP_CAST_URL = "http://localhost:" + str(PORT) + "/appcast.xml"

class MyTestCase(unittest.TestCase):

    def setUp(self):

        resource = File('./')
        factory = Site(resource)
        reactor.listenTCP(PORT, factory)
        Thread(target=reactor.run, args=(False,)).start()

        # configure winsparkle
        pywinsparkle.win_sparkle_set_appcast_url(APP_CAST_URL)
        pywinsparkle.win_sparkle_set_app_details(VENDOR, APP_NAME, VERSION)
        pywinsparkle.win_sparkle_init()

    def test_update_available_win_sparkle_check_update_with_ui(self):

        # Remind me later
        pywinsparkle.win_sparkle_check_update_with_ui()
        is_exception = False
        try:
            app = Application().connect(title_re="Software Update")
            app.top_window().window(title="Remind me later").click()
        except Exception:
            is_exception = True
        self.assertFalse(is_exception, "Remind me later failed")

        time.sleep(3)

        # Install Updates
        pywinsparkle.win_sparkle_check_update_with_ui()
        is_exception = False
        try:
            app = Application().connect(title_re="Software Update")
            app.top_window().window(title="Install update").click()
            app.top_window().window(title="Cancel").click()
        except Exception:
            is_exception = True
        self.assertFalse(is_exception, "Install update window not clicked")

if __name__ == '__main__':
    unittest.main()
