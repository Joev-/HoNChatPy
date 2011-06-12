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
import sys, os, time, signal, getpass

from core import *

def sigint_handler(signum,  frame):
	"""Handles SIGINT signal (<C-c>). Quits program."""
	log.notice("Quitting...")
	# sys.stdout.flush()
	# sys.exit(0)
	os._exit(1)

def main():
	logged_in = False

	while logged_in == False:
		usr = raw_input("Username: ")
		passw = getpass.getpass()
		log.info("Connecting...")

		# Request an initial connection
		conn = Connection()
		result = conn.connect(usr, passw)
		if result == True:
			logged_in = True
		else:
			logged_in = False
	
	# Logged_in is true so try connecting to the chat server now.
	# Thread the packet parsing
	tcp.PacketParser(conn).setDaemon(True)
	tcp.PacketParser(conn).start()

	while logged_in == True:
		command = raw_input("> ")
		if command != "":
			log.debug("Received command " + command)
	
if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)
	
	# If settings were stored in variables use:
	#log.addLog(sys.stdout, STDOUT_LOGLEVEL, STDOUT_VERBOSE, SCREEN)
	log.add_logger(sys.stdout, 'DEBUG', False, True)
	log.add_logger('honchat_log', 'DEBUG', True, False)
	main()
