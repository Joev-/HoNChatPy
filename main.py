#!/usr/bin/env python
import sys, threading, signal, re, time, getpass
from PySide.QtGui import QApplication
from hashlib import md5
try:
    from lib.honcore.client import HoNClient
    from lib.honcore.exceptions import *
except ImportError:
    print "HoNCore could not be found in the lib folder, please ensure it is available."

from core import log, events
from core.gui import HCPLoginWindow, HCPCoreWindow

class HCPHoNClient(HoNClient):
    def __init__(self):
        super(HCPHoNClient, self).__init__()
        self.logged_in = False

    @property
    def is_logged_in(self):
        return self.logged_in

    def login(self, username, password):
        log.info("Logging in..")
        password = md5(password).hexdigest()
        try:
            self._login(username, password)
        except MasterServerError, e:
            log.error(e)
            return False
        self.logged_in = True
        return True

    def connect(self):
        try:
            self._chat_connect()
        except ChatServerError, e:
            log.error(e)
            return False
        return True

    def logout(self):
        log.info("Logging out...")
        try:
            self._chat_disconnect()
        except ChatServerError, e:
            log.error(e)

        try:
            self._logout()
        except MasterServerError, e:
            log.error(e)

        self.logged_in = False

def main():
    client = HCPHoNClient()
    app = QApplication(sys.argv)
    app.setApplicationName("HoNChatPy")
    #app.setQuitOnLastWindowClosed(True) # May need to change for system tray behaviour
    
    login_window = HCPLoginWindow(client)
    login_window.setObjectName('login_window')
    
    core_window = HCPCoreWindow(client)
    core_window.setObjectName('hcp_window')
    
    while True:
        while not client.is_logged_in:
            login_window.show()
            app.exec_()
       
        # The login window gets closed. Check if it was closed because the user logged in
        # or if it was closed because 
        if client.is_logged_in:
            core_window.show()
        else:
            sys.exit()
        
        sys.exit(app.exec_())
     
def sigint_handler(signum,  frame):
    """Handles SIGINT signal (<C-c>). Quits program."""
    if honchatpy.is_logged_in:
        honchatpy.logout()
    else:
        log.info("Quitting...")
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    log.add_logger(sys.stdout, 'DEBUG', False)
    log.add_logger('honchat_log', 'DEBUG', True)
    main()

