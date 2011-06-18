import hashlib, urllib2, socket
import log 

""" 
Sends requests to the HoN master servers.
These are just basic HTTP get requests which return serialised php.
"""

HONVERSION = "2.0.33.0" # Put this somewhere else and clean it. Maybe make it local and double as an updater.
masterServer = "http://masterserver.hon.s2games.com/"
header = { 'User-Agent' : "S2 Games/Heroes of Newerth/" + HONVERSION + "/lac/x86-biarch" }

def hash(password):
	""" Hashes a password to MD5 """
	return hashlib.md5(password).hexdigest()

def httpget(url):
	url = masterServer + url
	req = urllib2.Request(url, None, header)
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		log.error(e.code)
		log.error(e.read())
		return None

	
	return response.read()

def httpost(url):
	""" When should POST be used VS GET?"""
	pass

# The available requests

def auth(username, password):
	""" Requests basic information about the user's account """
	url = "client_requester.php?f=auth&login=%s&password=%s" % (username, hash(password))
	return httpget(url)

def logout(cookie):
	""" Sends a logout 'request'(?) """
	url = "client_requester.php?f=logout&cookie=%s" % cookie 
	return httpget(url)

def server_list(cookie, gametype):
	pass

def nick2id(nickname):
	pass

def new_buddy(cookie, aid, bid):
	pass

def remove_buddy(cookie, aid, bid):
	pass

def new_banned(cookie, aid, bid, reason):
	pass

def remove_banned(cookie, aid, bid, reason):
	pass

def new_ignored(cookie, aid, iid, reason):
	pass

def remove_ignored(cookie, aid, iid, reason):
	pass

def stats_request(aid):
	pass

def stats_request_ranked(aid):
	pass

def motd():
	pass

def patcher(version, os, arch):
	pass