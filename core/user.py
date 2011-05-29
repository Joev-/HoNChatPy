""" A User object holds all of the information pertaining the current user who logged in.
	Specifically the user's cookie is important, aswell as their account id.

	Example of the user information returned by S2's client request.

	i:0;b:1;s:8:"super_id";s:6:"478695";s:10:"account_id";s:6:"478695";s:8:"nickname";s:4:"Joev";
	s:5:"email";s:22:"joev_wow@hotmail.co.uk";s:12:"account_type";s:1:"4";s:5:"trial";s:1:"0";
	s:7:"susp_id";s:1:"0";s:11:"prepay_only";N;s:8:"pass_exp";N;s:6:"cookie";s:32:"3a83addd2a3fbc576e2a71612db2f4fd";
	s:2:"ip";s:11:"199.7.79.38";s:9:"auth_hash";s:40:"892854be025b42c930122bf2bbc9173b92d7f883";s:8:"chat_url";s:13:"174.36.178.66"

	A User holds
		+ Account Id / Super Id - These are the same, what is a super id?
		+ Nickname
		+ Cookie
		+ An IP Adress - What's this? HoN's master server?
		+ Auth Hash - What's this for?
		+ Chat Server Address - I assume this is the address the chat server packets will originate
"""
user = None

class User:
	def __init__(self, aid, nick, cookie, ip, auth, chatip):
		global user

		self.aid = aid
		self.nick = nick
		self.cookie = cookie
		self.ip = ip
		self.auth = auth
		self.chatip = chatip
		
		user = self