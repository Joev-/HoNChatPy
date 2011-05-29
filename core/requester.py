""" Sends requests to the HoN master servers """

masterServer = "http://masterserver.hon.s2games.com/"
header = { 'User-Agent' : "S2 Games/Heroes of Newerth/" + HONVERSION + "/lac/x86-biarch" }

def httpget(url):
	self.url = masterServer + url
	try:
		req = urllib2.Request(url, None, header)
		response = urllib2.urlopen(req)
		return response
	except Exception e:
		log.error(e)
		return ""

def httpost(url):
	""" Post vs Get????"""
	pass

def auth(username, password):
	url = "client_requester.php?f=auth&login=%s&password=%s" % (username, password)
	return httpget(url)

def serverList(cookie, gametype):
	pass

def nick2id(nickname):
	pass

def newBuddy(cookie, aid, bid):
	pass

def removeBuddy(cookie, aid, bid):
	pass

def newBanned(cookie, aid, bid, reason):
	pass

def removeBanned(cookie, aid, bid, reason):
	pass

def newIgnored(cookie, aid, iid, reason):
	pass

def removeIgnored(cookie, aid, iid, reason):
	pass

def statsRequest(aid):
	pass

def statsRequestRanked(aid):
	pass

def motd():
	pass

def patcher(version, os, arch):
	pass