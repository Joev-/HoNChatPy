import hashlib
import urllib2
import log 

""" Sends requests to the HoN master servers """

HONVERSION = "2.0.31.0" # Put this somewhere else and clean it. Maybe make it local and double as an updater.
masterServer = "http://masterserver.hon.s2games.com/"
header = { 'User-Agent' : "S2 Games/Heroes of Newerth/" + HONVERSION + "/lac/x86-biarch" }

def hash(password):
		""" Hashes a password to MD5 """
		return hashlib.md5(password).hexdigest()

def httpget(url):
	url = masterServer + url
	try:
		req = urllib2.Request(url, None, header)
		response = urllib2.urlopen(req)
		return response.read()
	except Exception, e:
		log.error(e)
		return None

def httpost(url):
	""" When should POST be used VS GET?"""
	pass

# The available requests

def auth(username, password):
	url = "client_requester.php?f=auth&login=%s&password=%s" % (username, hash(password))
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