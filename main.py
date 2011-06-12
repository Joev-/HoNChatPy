#!/usr/bin/env python
"""
 _   _       _   _ _____ _           _  ______       
| | | |     | \ | /  __ \ |         | | | ___ \      
| |_| | ___ |  \| | /  \/ |__   __ _| |_| |_/ /_   _ 
|  _  |/ _ \| . ` | |   | '_ \ / _` | __|  __/| | | |
| | | | (_) | |\  | \__/\ | | | (_| | |_| |   | |_| |
\_| |_/\___/\_| \_/\____/_| |_|\__,_|\__\_|    \__, |
                                                __/ |
                                               |___/ 
"""
import sys
import time
import signal
import getpass

from core import *

def sigint_handler(signum,  frame):
    """Handles SIGINT signal (<C-c>). Quits program."""
    log.notice("Quitting..")
    sys.exit(0)

def main():
	_logged_in = False

	while _logged_in == False:
		usr = raw_input("Username: ")
		passw = getpass.getpass()
		log.info("Connecting...")

		# Request an initial connection
		conn = Connection()
		result = conn.connect(usr, passw)
		if result == True:
			_logged_in = True
			# Got the user info, so try connecting to the chat server now.
			# Thread the packet parsing
			tcp.parseThread(conn).start()
		else:
			_logged_in = False

if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)
	
	# If settings were stored in variables use:
	#log.addLog(sys.stdout, STDOUT_LOGLEVEL, STDOUT_VERBOSE)
	log.add_logger(sys.stdout, 'DEBUG', False)
	log.add_logger('honchat_log', 'DEBUG', True)
	main()
