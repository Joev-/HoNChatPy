import socket

import log
import requester
import tcp

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
		self.user = {}

	def connect(self, user, password):
		""" Requests the user data and opens a socket using it."""
		log.notice("Opening a connection")

		response = requester.auth(user, password)
		if response == None:
			log.error("Could not connect to Heroes of Newerth")
			self.connected = False
			return False
		elif response == "":
			log.error("Could not obtain user information")
			self.connected = False
			return False
		# Add handling for invalid username/password here too.
		
		# Push the result through the deserialiser
		data = deserialise(response)

		self.getBasicData(data)
		self.getUserData(data)

		log.debug(self.cookie + " "  + self.ip + " " + self.auth + " " + self.chatserv)
		return True
	
	def socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.chatserv, CHAT_PORT))

		# Send the initial login packet
		log.debug("Greeting the login with " + self.cookie + " - " + self.ip + " - " + self.user['auth'])
		tcp.greet(self.socket, self.cookie, self.ip, self.user['auth'])

		self.connected = True
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

		self.user = {}
	
	def getBasicData(self, data):
		self.cookie = data['cookie']
		self.ip = data['ip']
		self.auth = data['auth_hash']
		self.chatserv = data['chat_url']
	
	def getUserData(self, data):
		self.user['nickname'] = data['nickname']
		self.user['superid'] = int(data['super_id'])
		self.user['auth'] = data['auth_hash']

