""" 
Functions and information for globally accessable objects, Users, Account, Channels, Buddies/Bans/Ignores. etc.
----------

Functions and information pertaining to users, including buddies, bans, ignores and other such stuff.
These are needed as they are global objects which are created when a response is returned from the client requester 
and will be updated in real time. The response contains a big list of buddies, bans, ignores, and other than watching for
buddy/ignore/ban add/remove packets is the only way to obtain this information.
	
A User object holds information pertaining a user, can be a clan member, a buddy, both, or none. 

A user holds the following
	+ accId			~ The user's account id.
	+ nick 			~ The user's nickname.
	+ accIcon		~ The user's account icon. e.g. ....
	+ clanTag 		~ The user's clan tag, to go together with the nick.
	+ status		~ The current status of the user. e.g. Not Found, Offline, In Channels... and In Game....
	+ flags			~ Flags for the user, e.g. prepurchased, officer, admin, staff.
	+ buddy			~ A boolean if the user is a buddy of the logged in user or not.
	+ clanMember	~ A boolean if the user is a clan member of the logged in user's clan or not.

Some information about users can be obtained using a whois command, the whois returns the user's status and the channels the 
user is currently in unless the user is in a game. If the user is in a game then it returns the game name and the... current
game time. e.g. "Current game time: Lobby" or "Current game time: Banning" or "Current game time: 0:39:00."
Full information in the tcp file documentation.

An account object holds information pertaining to the user who is logged in. It will store some account information 
which may be needed by the program.



"""

buddyList = []
banList = []
ignoreList = []

class User(object):
	pass

class Account(object):

	def __init__(self):
		pass


""" 
Channel Information

Needs work and more information.

A channel holds the following
	+ id		~ The id of the channel
	+ name		~ The name of the channel
"""

class Channel:

	def __init__(self):
		pass

		