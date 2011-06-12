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
import sys, os, time, signal, getpass, threading

from core import *

def sigint_handler(signum,  frame):
	"""Handles SIGINT signal (<C-c>). Quits program."""
	log.notice("Quitting...")
	sys.exit(0) # If sys.exit is used then 'Caught SIGINT' is also called in the except catch below.
	# os._exit(1)

def main():
	logged_in = False

	while logged_in == False:
		usr = raw_input("Username: ")
		passw = getpass.getpass()
		log.info("Connecting...")

		# Request an initial connection
		conn = Connection()
		result = conn.connect(usr, passw)
		logged_in = result
			
	# Logged_in is true so try connecting to the chat server now.
	# Thread the packet parsing
	t = tcp.PacketParser(conn)
	t.daemon = True
	t.start()
	
	""" Temporary solution for catching SIGINT in threads. Remove at a later point. """
	try:
		while t.is_alive():
			t.join(timeout=1.0)
	except (KeyboardInterrupt, SystemExit):
		log.notice("Caught SIGINT") # Doesn't get called?
		t.stop()
	
if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)
	
	# If settings were stored in variables use:
	#log.addLog(sys.stdout, STDOUT_LOGLEVEL, STDOUT_VERBOSE)
	log.add_logger(sys.stdout, 'DEBUG', False)
	log.add_logger('honchat_log', 'DEBUG', True)
	main()
