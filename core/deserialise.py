import user
import log
from lib import phpserialize as phpd

""" Deserialises the php stuff and creates objects, not really... big... since there's this like, library... """

def deserialise(raw):
	data = phpd.loads(raw)
	
	if 'auth' in data:
		return False
	
	getBasicInfo(data)
	getBuddies(data['buddy_list'][int(data['super_id'])])
	# getClanMemebrs(data)
	# getBannedList(data)
	# getIgnoreList(data)

	return True

def getBasicInfo(data):
	user.account = user.Account(int(data['super_id']), data['nickname'], data['cookie'], data['auth_hash'], data['chat_url'], data['ip'])

def getBuddies(buddylist):
	for userKey in buddylist:
		accid = buddylist[userKey]['account_id']
		buddyid = buddylist[userKey]['buddy_id']
		nick = buddylist[userKey]['nickname']
		clantag = buddylist[userKey]['clan_tag'] or ""
		clanname = buddylist[userKey]['clan_name']

		buddy = user.User(accid, buddyid, nick, clantag, clanname, 0, 0)
		user.account.buddylist.append(buddy)

def getClanMemebrs(data):
	pass

def getBannedList(data):
	pass

def getIgnoreList(data):
	pass
