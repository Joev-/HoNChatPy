#!/usr/bin/env python
import sys, threading, signal, re, time, hashlib, getpass

try:
	from lib.honcore import client
	from lib.honcore.exceptions import *
except ImportError:
	print "HoNCore could not be found in the lib folder, please ensure it is available."

from core import *

def md5hash(password):
	""" Hashes a password to MD5 """
	return hashlib.md5(password).hexdigest()

chat_client = client.HoNClient()

def main():

	while not chat_client.is_logged_in():
		usr = raw_input("Username: ")
		passw = getpass.getpass()

		log.info("Logging in...")
		try:
			chat_client.login(usr, md5hash(passw))
		except MasterServerError, e:
			log.error(e)
	
	if chat_client.is_logged_in():
		log.info("Waiting for chat server to verify authentication.")
		try:
			chat_client.chat_connect()
		except ChatServerError, e:
			log.error(e)
	
	while chat_client.is_logged_in() and chat_client.is_connected():
		time.sleep(1)
		
			
def disconnect_logout():
	if chat_client.is_connected():
		log.info("Disconnecting from chat server")

	try:
		# TODO: Handle response from chat_disconnect
		# Not much can fail because the socket gets killed anyway
		# it's up to the chat server to clean up broken connections. :)
		chat_client.chat_disconnect()
	except ChatServerError, e:
		pass
	
	if chat_client.is_logged_in():
		log.info("Logging out")
		
	try:
		# TODO: Handle requester response for logging out
		chat_client.logout()
	except MasterServerError, e:
		if e.code == 106:
			log.error('Logout was forced, master server did receive the logout request.')

def sigint_handler(signum,	frame):
	"""Handles SIGINT signal (<C-c>). Quits program."""
	disconnect_logout()
	log.info("Quitting...")
	sys.exit(0)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)
	log.add_logger(sys.stdout, 'DEBUG', False)
	log.add_logger('honchat_log', 'DEBUG', True)
	main()
