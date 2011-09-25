#!/usr/bin/env python
import sys, threading, signal, re, time, getpass
from hashlib import md5
try:
    from lib.honcore.client import HoNClient
    from lib.honcore.exceptions import *
except ImportError:
    print "HoNCore could not be found in the lib folder, please ensure it is available."

from core import *

class HoNChatPy(HoNClient):
    def __init__(self):
        super(HoNChatPy, self).__init__()
        self.logged_in = False

    @property
    def is_logged_in(self):
        return self.logged_in

    def login(self, username, password):
        log.info("Logging in..")
        try:
            self._login(username, password)
        except MasterServerError, e:
            log.error(e)

        try:
            self._chat_connect()
        except ChatServerError, e:
            log.error(e)

        self.logged_in = True

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
    while 1:
        while honchatpy.is_logged_in is False:
            usr = raw_input("Username: ")
            passw = getpass.getpass()
            passw = md5(passw).hexdigest()

            honchatpy.login(usr, passw)
             
        while honchatpy.is_logged_in:
            time.sleep(1)
        
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
    honchatpy = HoNChatPy()
    main()

