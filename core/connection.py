""" Connection Object """

class Connection:

	def  __init__(self):
		self.connected = False
		self.cookie = None

	def connect(user, password):
		""" Opens a connection to HoN """
		result = requester.auth(user, password)

		# Push the result through the deserialiser
		if result != None:
			result.deserialise()
		
		self.cookie = datCookie
		self.connected = True

	def close():
		""" Closes a connection """

	