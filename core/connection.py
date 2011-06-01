import socket

import log
import requester
import tcp
import time

from deserialise import *

""" 
Connection Object 
The connection object holds all data related to the server connections including information about the chat server 
and the master server and what not.

The connection holds
	+ The cookie
	+ An IP Address for some unknown server. TODO: Find out what it is.
	+ Auth Hash for something. TODO: Find out what for.
	+ Chat Server Address.
	+ The connected user info
		+ Nick
		+ Account ID
		+ Clan Name
		+ Clan Tag
		+ The person being followed?

	Chat server port is 11031. Does it change?
"""
CHAT_PORT = 11031

class Connection:

	def  __init__(self):
		self.connected = False
		self.cookie = None
		self.ip = None
		self.auth = None
		self.chatserv = None
		self.account = {}

	def connect(self, user, password):
		""" Requests the user data and opens a socket using it."""

		log.notice("Getting authentication data...")
		tries = 0
		try:
			response = requester.auth(user, password)
		except:
			if tries == 3:
				log.critical("Failed to connect, something's wrong!")
				return False
			timeout = pow(2, tries)
			log.notice("Connection error, retrying in %i " % timeout)
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

		if 'auth' in data:
			log.error("Incorrect username/password")
			return False
		
		self.getBasicData(data)
		self.getAccountData(data)

		return True
	
	def socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.chatserv, CHAT_PORT))

		# Send the initial login packet
		log.debug("Greeting the login")
		if tcp.greet(self.socket, self.account['superid'], self.cookie, self.ip, self.account['auth']) == 1:
			self.connected = True
			log.notice("Connection successfull")
		else:
			self.connected = False
			log.notice("Connection failed, is the chat protocol correct?")
		
		return self.socket

	def close(self):
		""" Closes a connection """
		self.connected = False
		self.cookie = None
		self.ip = None
		self.auth = None
		self.chatserv = None

		self.socket.close()
		self.socket = None

		self.account = {}
	
	def getBasicData(self, data):
		self.cookie = data['cookie']
		self.ip = data['ip']
		self.auth = data['auth_hash']
		self.chatserv = data['chat_url']
	
	def getAccountData(self, data):
		self.account['nickname'] = data['nickname']
		self.account['superid'] = int(data['super_id'])
		self.account['auth'] = data['auth_hash']

