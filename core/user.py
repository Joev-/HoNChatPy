import log
""" 
Functions and information for globally accessable objects, Users, Account, Channels, Buddies/Bans/Ignores. etc.
These are needed as they are global objects which are created when a response is returned from the client requester 
and will be updated in real time. The response contains a big list of buddies, bans, ignores, and other than watching for
buddy/ignore/ban add/remove packets is the only way to obtain this information.
"""
account = None

""" Functions """
def id2nick(bid):
	""" Provide a user's nick instead of their ID. Purely visual, useful for notifications."""
	for user in account.buddylist:
		if bid == user.buddyid:
			if user.clantag != "":
				clantag = "[" + user.clantag + "]"
			else:
				clantag = ""
			name = clantag + user.nickname
			return name
	return str(bid) # It's going to be used as a string anyway...

def set_status(nick, server, gamename, status):
	""" Update the status for a buddy.
		Some data like server and game name are not stored... Buuuut, they could be.
	"""
	global account
	for user in account.buddylist:
		if user.nickname == nick:
			user.status = status
	
"""
A User object holds information pertaining a user, can be a clan member, a buddy, both, or none. 

A user holds the following
	+ accId			~ The user's account id.
	+ nick 			~ The user's nickname.
	+ accIcon		~ The user's account icon. e.g. ....
	+ clanTag 		~ The user's clan tag, to go together with the nick.
	+ status		~ The current status of the user. e.g. Not Found, Offline, In Channels... and In Game....
	+ flags			~ Flags for the user, e.g. prepurchased, officer, admin, staff.

Possible information to hold.
	+ If the user is in a game it would show the game name and server.. Optionally that they are in. 
	  Storing it would reduce requests, and it would be changed when the user leaves a game since a new
	  status is sent anyway.

Some information about users can be obtained using a whois command, the whois returns the user's status and the channels the 
user is currently in unless the user is in a game. If the user is in a game then it returns the game name and the... current
game time. e.g. "Current game time: Lobby" or "Current game time: Banning" or "Current game time: 0:39:00."
"""
class User:
	def __init__(self, accid, buddyid, nick, clantag = "", clanname = None, status = 0, flag = 0x00):
		self.accid = int(accid)
		self.buddyid = int(buddyid)
		self.nickname = nick
		self.status = int(status)
		self.flag = int(flag)
		self.clantag = clantag
		self.clanname = clanname

"""
An account object holds information pertaining to the user who is logged in. It will store some account information 
which may be needed by the program.

"""
class Account:
	def __init__(self, super_id, nickname, cookie, auth_hash, chat_url, ip):
		self.super_id = super_id
		self.nickname = nickname
		self.cookie = cookie
		self.auth_hash = auth_hash
		self.chat_url = chat_url
		self.ip = ip
		self.buddylist = []
		self.banlist = []
		self.ignorelist = []

		global account
		account = self
""" 
Channel Information

Needs work and more information.

A channel holds the following
	+ id		~ The id of the channel
	+ name		~ The name of the channel
"""

class Channel:
	pass

		