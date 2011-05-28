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

from api import *

def sigint_handler(signum,  frame):
    """Handles SIGINT signal (<C-c>). Quits program."""
    log.notice("Quitting..")
    sys.exit(0)

def main():
	log.notice("Hello World")

if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)
	# If settings were stored in variables use:
	#log.addLog(sys.stdout, STDOUT_LOGLEVEL, STDOUT_VERBOSE)
	log.addLogger(sys.stdout, 'DEBUG', False, False)
	log.addLogger('honchat_log', 'DEBUG', True, True)
	main()