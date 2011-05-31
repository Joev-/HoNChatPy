import log
import requester
from deserialise import *

""" Connection Object 
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

"""
class Connection:

	def  __init__(self):
		self.connected = False
		self.cookie = None
		self.ip = None
		self.auth = None
		self.chatserv = None
		# self.user.nick = None
		# self.user.clan = None
		# self.user.tag = None
		# self.user.follow = None

	def connect(self, user, password):
		""" Opens a connection to HoN """
		log.notice("Opening a connection")

		global connection
		result = requester.auth(user, password)

		log.notice(result)

		if result == None:
			log.error("Could not connect to Heroes of Newerth")
			return False

		# Push the result through the deserialiser
		data = deserialise(result)
		
		# self.user.nick = data[1]
		# self.user.clan = data[2]
		# self.user.tag = data[3]
		# self.user.follow = data[4]
		# self.cookie = data[5]
		# self.ip = data[6]
		# self.auth = data[7]
		# self.chatserv = data[8]
		self.connected = True

		return True

	def close():
		""" Closes a connection """
		self.connected = False
		self.cookie = None
		self.ip = None
		self.auth = None
		self.chatserv = None
		self.user.nick = None
		self.user.clan = None
		self.user.tag = None
		self.user.follow = None
	