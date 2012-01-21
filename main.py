#!/usr/bin/env python
import sys, threading, signal, re, time, getpass
from hashlib import md5
from PySide.QtGui import QApplication
from PySide.QtCore import QTimer

try:
    from lib.honcore.client import HoNClient
    from lib.honcore.exceptions import *
except ImportError:
    print "HoNCore could not be found in the lib folder, please ensure it is available."

from core import log, events, ConnectionManager
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
        if len(password) != 32:
            password = md5(password).hexdigest()
        try:
            self._login(username, password)
        except MasterServerError, e:
            log.error(e)
            return False
        self.logged_in = True
        return True

    def connect(self):
        log.info("Connecting..")
        try:
            self._chat_connect()
        except ChatServerError, e:
            log.error(e)
            return False
        return True

    def logout(self):
        log.info("Logging out...")
        try:
            self._logout()
        except MasterServerError, e:
            log.error(e)
            return False
        self.logged_in = False
        return True
    
    def disconnect(self):
        log.info("Disconnecting...")
        try:
            self._chat_disconnect()
        except ChatServerError, e:
            log.error(e)
            return False
        return True

def main():
    client = HCPHoNClient()
    
    # Temporary client config
    # Move to self implementation using QSettings later.
    client._configure(protocol=19)

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
       
        while client.is_logged_in:
            core_window.show()
            client.connect()
            app.exec_()
     
if __name__ == "__main__":
    log.add_logger(sys.stdout, 'DEBUG', False)
    log.add_logger('honchat_log', 'DEBUG', True)
    main()

