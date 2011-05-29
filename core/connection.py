import requester

""" Connection Object """

class Connection:

	def  __init__(self):
		self.connected = False
		self.cookie = None

	def connect(user, password):
		""" Opens a connection to HoN """
		result = requester.auth(user, password)
		
		self.cookie = datCookie
		self.connected = True

	def close():
		""" Closes a connection """

	def hash(password):
		""" Hashes a password to MD5 """
		return hashlib.md5(password).hexdigest()