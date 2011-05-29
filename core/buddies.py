""" Holds the buddy list and also provides a Buddy class.

	An example buddy returned by S2's client-request.
	{s:10:"account_id";s:6:"478695";s:8:"buddy_id";s:5:"39360";s:6:"status";s:1:"2";s:11:"create_time";s:10:"1284477435";
	s:11:"expire_time";N;s:8:"nickname";s:8:"herregud";s:9:"clan_name";N;s:8:"clan_tag";N;}

	A buddy needs to hold:
		+ Account id
		+ Buddy id
		+ Status
		+ Nickname
		+ Clan Name
		+ Clan Tag
"""

buddyList = []

class Buddy:
	
	def __init__(self, aid, bid, status, nickname, clanName, clanTag):
		global buddyList
		self.aid = aid
		self.bid = bid
		self.status = status
		self.nickname = nickname
		self.clanName = clanName
		self.clanTag = clanTag
		
		buddyList.append(self)

	
# Just ideas...

#def addBuddy(buddy):
#	self.buddies.append(buddy)

#def removeBuddy(buddy):
#	self.buddies.remove(buddy)