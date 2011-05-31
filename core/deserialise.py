import phpserialize as phpd

""" Deserialises the php stuff and creates objects, not really... big... since there's this like, library... """

def deserialise(raw):
	clean = phpd.loads(raw)
	
	return clean

def getBasicInfo(data):
	pass

def getBuddies(data):
	pass

def getClanMemebrs(data):
	pass

def getBannedList(data):
	pass

def getIgnoreList(data):
	pass
