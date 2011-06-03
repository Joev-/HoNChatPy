from lib import phpserialize as phpd
from user import *

""" Deserialises the php stuff and creates objects, not really... big... since there's this like, library... """

def deserialise(raw):
	data = phpd.loads(raw)
	
	if 'auth' in data:
		return data
	
	# getBuddies(data)
	# getClanMemebrs(data)
	# getBannedList(data)
	# getIgnoreList(data)

	info = getBasicInfo(data)

	return info

def getBasicInfo(data):
	info = {}
	info['master_svr'] = data['master_svr']
	info['ip'] = data['ip']
	info['chat_url'] = data['chat_url']
	info['cookie'] = data['cookie']
	info['auth_hash'] = data['auth_hash']
	info['nickname'] = data['nickname']
	info['super_id'] = data['super_id']
	return info

def getBuddies(data):
	pass

def getClanMemebrs(data):
	pass

def getBannedList(data):
	pass

def getIgnoreList(data):
	pass
