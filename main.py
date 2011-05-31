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

cookie = None
ip = None
auth = None
chatserv = None

def sigint_handler(signum,  frame):
    """Handles SIGINT signal (<C-c>). Quits program."""
    log.notice("Quitting..")
    sys.exit(0)

def main():
	usr = raw_input("Username: ")
	#passw = raw_input("Password: ")
        passw = getpass.getpass()         
	log.info("Connecting...")

	# Request an initial connection
	conn = Connection()
	result = conn.connect(usr, passw)
	if result == True:
		# Got the user info, so try connecting to the chat server now.
		socket = conn.socket()
		# pass
		# Get initial connection stuff here and go into a loop.
		while conn.connect == True:
			packet = socket.recv(1024)
			
			if len(packet) == 0:
				 continue
			
			log.debug("Packet length is : " + str(len(packet)))
			r = Struct("basic",
	                    ULInt32("size"),
	                    Byte("function"))
	        logging.debug(packet)
	        data = r.parse(packet)
	        logging.debug(data)



if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)
	
	# If settings were stored in variables use:
	#log.addLog(sys.stdout, STDOUT_LOGLEVEL, STDOUT_VERBOSE)
	log.addLogger(sys.stdout, 'DEBUG', False, False)
	log.addLogger('honchat_log', 'DEBUG', True, True)
	main()
