import user
import log
from lib import phpserialize as phpd

""" Deserialises the php stuff and creates objects, not really... big... since there's this like, library... """

def deserialise(raw):
	data = phpd.loads(raw)
	
	if 'auth' in data:
		return False
	
	get_basic_info(data)
	get_buddies(data['buddy_list'][int(data['super_id'])])
	# getClanMemebrs(data)
	# getBannedList(data)
	# getIgnoreList(data)

	return True

def get_basic_info(data):
	user.account = user.Account(int(data['super_id']), data['nickname'], data['cookie'], data['auth_hash'], data['chat_url'], data['ip'])

def get_buddies(buddylist):
	for userKey in buddylist:
		accid = buddylist[userKey]['account_id']
		buddyid = buddylist[userKey]['buddy_id']
		nick = buddylist[userKey]['nickname']
		clantag = buddylist[userKey]['clan_tag'] or ""
		clanname = buddylist[userKey]['clan_name']

		buddy = user.User(accid, buddyid, nick, clantag, clanname, 0, 0)
		user.account.buddylist.append(buddy)

def get_clan_memebrs(data):
	pass

def get_banned_list(data):
	pass

def get_ignore_list(data):
	pass
