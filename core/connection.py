import log
import requester
import user

import socket
import tcp
import time

from deserialise import *

""" 
Connection Object 
The connection object holds all data related to the server connections including information about the chat server 
and the master server and what not.

The connection holds
	+ The socket to the chat server
	+ A connect flag.

	Chat server port is 11031. Does it change?
"""
CHAT_PORT = 11031
INVIS = False # TODO: Move somewhere, a settings option.

class Connection:

	def  __init__(self):
		self.connected = False

	def connect(self, user, password):
		""" Requests the user data and opens a socket using it."""

		tries = 1

		while True:
			try:
				log.notice("Getting authentication data...")
				response = requester.auth(user, password)
				break
			except:
				if tries == 3:
					log.critical("Failed to connect, something's wrong!")
					return False
				timeout = pow(2, tries)
				log.notice("Connection error, retrying in %i seconds." % timeout)
				time.sleep(timeout)
				tries += 1
		
		if response == None:
			log.error("Could not connect to Heroes of Newerth.")
			self.connected = False
			return False
		elif response == "":
			log.error("Could not obtain user information.")
			self.connected = False
			return False

		# Add handling for invalid username/password here too. Will need to parse the response and check for "invalid details"
		
		# Push the result through the deserialiser
		data = deserialise(response)

		if data == False:
			log.error("Incorrect username/password")
			return False

		return True
	
	def make_socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((user.account.chat_url, CHAT_PORT))

		# Send the initial login packet
		log.debug("Greeting the login")
		if tcp.greet(self.socket, user.account.super_id, user.account.cookie, user.account.ip, user.account.auth_hash, INVIS) == 1:
			self.connected = True
			log.notice("Connection successfull")
		else:
			self.connected = False
			log.notice("Connection failed, is the chat protocol correct?")
		
		return self.socket

	def close(self):
		""" Closes a connection """
		self.connected = False
		self.socket.close()
