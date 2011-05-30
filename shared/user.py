""" Functions and information pertaining to users, including buddies, bans, ignores and other such stuff.
	
	A User object holds information pertaining a user.
	
	A user holds the following
		+ nick 			~ The user's nickname
		+ clanTag 		~ The user's clan tag, to go together with the nick.
		+ accType		~ The user's account type. e.g. premium, normal, trial? TODO: Find real, non-guess values.
		+ accIcon		~ The user's account icon. e.g. ....
		+ channels		~ A list of channels that the user is currently in.
		+ accId			~ The user's account it.
		+ status		~ The current status of the user. e.g. Not Found, Offline, In Channels... and In Game....
		+ buddy			~ A boolean if the user is a buddy of the logged in user or not.
		+ clanMember	~ A boolean if the user is a clan member of the logged in user's clan or not.
	
	Some information about users can be obtained using a whois command, the whois returns the user's status and the channels the 
	user is currently in unless the user is in a game. If the user is in a game then it returns the game name and the... current
	game time. e.g. "Current game time: Lobby" or "Current game time: Banning" or "Current game time: 0:39:00."
	Full information in the tcp file documentation.

"""

buddyList = []
banList = []
ignoreList = []


class User:
	def __init__(self, nick, clanTag, accType, accIcon, channels = [], 
				accId, status, buddy = False, clanMember = False):
		self.nick = nick
		self.clanTag = clanTag
		self.accType = accType
		self.accIcon = accIcon
		self.channels = channels
		self.accId = accId
		self.status = status
		self.buddy = buddy
		self.clanMember = clanMember
	


		