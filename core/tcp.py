""" 
TCP packet related functions and management.
	
See: http://honwiki.net/wiki/Chat_Protocol

Receive TCP packets and parse them.

My documentation of packets.

Client -> Server packets.

	+ 0x0C00  - Login request. 101 bytes.
		+ ULInt16: aid - Account id
		+ String: cookie
		+ String: ip
		+ String: authHash
		+ ULInt32: proto - Chat protocol version
		+ ULInt8: unknown - No idea, Normal hon client uses 0x01, HoNPurple uses 0x05
		+ ULInt32: invisible - Sets if the user is invisible or not, invisible is 0x03, normal is 0x00. Will need handling later.
	
	+ 0x02A01  - Pong, response to ping.

Server -> Client packets

	+ 0x1C00 - Login acknowlegement. 4 Bytes.
		+ ULInt16: size
		+ ULInt16: packetid
	
	+ 0x0B - Initial status, sent after 0x1C00. Contains initial data, channels, players online? amongst other stuff.
		+ ULInt16: size
		+ ULInt16: packetid
		+ ULInt32: buddycount - Number of buddies online.
			+ ULInt32: buddyid - ID of buddy, can be matched with response from http auth request.
			+ Byte: status - Offline, online, in lobby, in game. If in game/lobby then:
				+ CString: server - IP and port of the game server.
				+ CString: name - Name of the game.
		+ There's more stuff, unsure what to do with it, no one else seems to use it..

	+ 0x0C - Status update... Friends joining/leaving games, etc?
		+ ULInt16: size
		+ ULInt16: packetid
		+ ????
	
	+ 0x08 - Whisper. Basic whisper message.
		+ ULInt16: size
		+ ULInt16: packetid
		+ CString: name - Name of the person who sent the message, includes clan tag.
		+ CString: message
	
	+ 0x68 - Number of players online. Sent every 30 seconds. Contains 35 Bytes of data.
		+ ULInt16: size
		+ ULInt16: packetid
		+ ULInt32: count - Number of players online.
		+ There's other data here, I think it's best to ignore it. Seems like weird region IDs or something.

	States:
	The available states of a user.
		+ 0x0 - Offline
		+ 0x3 - Online
		+ 0x4 - In Lobby
		+ 0x5 - In Game
	
	Flags:
	The available accout flags of a user
		+ 0x00 - None, basic user.
		+ 0x01 - Moderator
		+ 0x02 - Leader?
		+ 0x03 - Administrator?
		+ 0x04  - Staff?
		+ 0x40 - Prepurchased, gold shield? 

	Notes:
		* All strings are zero terminated (\\x00). Can be grabbed using CString.
		* Server -> Client packets are always preceded by it's length
		* Must send a chat protocol version!
		* On the 9th June 2011 the maintenence made changes to the servers, the new chat server IP is 50.56.42.64 and the protocol was bumped to 0x0E.
"""
import struct, threading

import log
import user
from lib.construct import *
from packet import *


""" Some constants """
HON_FLAGS_NONE			= 0x00
HON_FLAGS_OFFICER		= 0x01
HON_FLAGS_LEADER		= 0x02
HON_FLAGS_ADMINISTRATOR	= 0x03
HON_FLAGS_STAFF			= 0x04
HON_FLAGS_PREPURCHASED	= 0x40

HON_STATUS_OFFLINE		= 0
HON_STATUS_ONLINE		= 3
HON_STATUS_INLOBBY		= 4
HON_STATUS_INGAME		= 5

HON_NOTIFICATION_ADDED_AS_BUDDY =	0x01
HON_NOTIFICATION_BUDDY_ACCEPTED =	0x02
HON_NOTIFICATION_REMOVED_AS_BUDDY =	0x03
HON_NOTIFICATION_BUDDY_REMOVED =	0x04

HON_MODE_NORMAL			= 0x00
HON_MODE_INVISIBLE		= 0x03

class PacketParser(threading.Thread):
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self._stop = threading.Event()
		self.conn = conn
		
	def run(self):
		socket = self.conn.make_socket()

		# Infinate loop, receive packets and process them.
		while self.conn.connected == True:
			packet = socket.recv(1024)
			# log.debug("Packet length is : " + str(len(packet)))
			parse_packet(socket, packet)

		if self.conn.connected != True:
			log.notice("Disconnected.. Stopping thread.")
			self.stop()

	def stop (self):
		self._stop.set()

	def stopped (self):
		return self._stop.isSet()

""" Functions """
def parse_packet(socket, packet):
	""" Parses the incoming packet by passing it to the relevant function.
		The socket is needed for the ping, but it's sort of bloated data 
		here because that's the only place it's used. Is there
		some other way to get the socket when sending the pong?
	"""
	if len(packet) == 0:
		return
	
	r = Struct("response", ULInt16("size"), ULInt16("packetid"))
	data = r.parse(packet)
	log.debug("<< 0x%x - Len: %d" % (data.packetid, len(packet)))
	if data.packetid == HON_SC_PING:
		send_pong(socket)
	elif data.packetid == HON_SC_WHISPER:
		parse_whisper(packet)
	elif data.packetid == HON_SC_INITIAL_STATUS:
		parse_initial_statuses(packet)
	elif data.packetid == HON_SC_UPDATE_STATUS:
		parse_user_status_update(packet)
	elif data.packetid == HON_SC_TOTAL_ONLINE:
		parse_total_online(packet)
	# else:
	# 	log.debug("Unknown packet: %x" % data.packetid)

def greet(socket, aid, cookie, ip, auth, invis = False):
	""" Sends the initial login request to the chat server, sends the account id, cookie, ip, auth hash and chat protocol version.
		
		Server responds with a response (0x1C00) to acknlowdge the login and also the intial data (0x0B)

	"""
	# Invisible mode flag.
	if invis == True:
		mode = HON_MODE_INVISIBLE
	else:
		mode = HON_MODE_NORMAL
	
	# Build the packet
	c = Struct("login",
			ULInt16("id"), # 0x0C00
			ULInt32("aid"),
			String("cookie", len(cookie)+1, encoding="utf8", padchar = "\x00"),
			String("ip", len(ip)+1, encoding="utf8", padchar = "\x00"),
			String("auth", len(auth)+1, encoding="utf8", padchar = "\x00"),
			ULInt32("proto"), # Protocol version?
			ULInt8("unknown"), # Unknown also, 5? HoN uses 0x01, HonPurple uses 0x05..
			ULInt32("mode") # Invisible or normal.
		)

	req = c.build(Container(id=HON_CS_AUTH_INFO, aid=aid, cookie=unicode(cookie), ip=unicode(ip), auth=unicode(auth), 
							proto=HON_PROTOCOL_VERSION, unknown=0x01, mode=mode))
	b = socket.send(req)

	log.notice("Authenticating...")

	""" Check that the server sends the ack response (0x0200 0x1C00). If it does, then all is good,
		 otherwise the log in failed and something is wrong. """

	resp = socket.recv(1024)
	if len(resp) == 0:
		return 0
			
	# Handle the login response here
	r = Struct("response", ULInt16("size"), ULInt16("packetid"))
	data = r.parse(resp)
	log.debug("<< 0x%x" % data.packetid)

	if data.packetid == HON_SC_AUTH_ACCEPTED:
		# Success! Logged in!
		# Auto connect channels need to be sent at this point!
		# joinChannel() or so.
		return 1

	# Something went wrong...
	log.error("Server did not respond correctly. Did something change?")
	return 0

""" Client to server """
def send_pong(socket):
	""" Replies to a ping request (0x2A00) with a pong response (0x2A01) """
	socket.send(struct.pack('h', HON_CS_PONG))
	log.debug(">> Pong")


""" Server to Client """
def parse_total_online(packet):
	""" Gets the number of players online """

	c = Struct("packet", ULInt16("size"), ULInt16("packetid"), ULInt32("count"))
	r = c.parse(packet)
	log.notice(str(r.count) + " players online.")

def parse_initial_statuses(packet):
	""" Parses the initial status packet sent. 
		Retrieves states for all online buddies, also contains some information I'm unsure of
		what to do with yet.
	"""

	buddycount = int(struct.unpack_from('i', packet[4:8])[0]) # Tuples?!!
	buddy_data = packet[8:]
	if buddycount > 0:
		i = 1
		log.debug("Parsing buddy data for %i buddies." % buddycount)
		while i <= int(buddycount):
			status = int(struct.unpack_from('B', buddy_data[4])[0])
			nick = ""
			if status == HON_STATUS_INLOBBY or status == HON_STATUS_INGAME:
				c = Struct("buddy", ULInt32("buddyid"), Byte("status"), Byte("flag"), CString("server"), CString("gamename"))
				r = c.parse(buddy_data)
				nick = user.id2nick(r.buddyid)
				buddy_data = buddy_data[6 + (len(r.server)+len(r.gamename)):]
				log.debug(nick + " is online and in the game " + r.gamename)
			else:
				c = Struct("buddy", ULInt32("buddyid"), Byte("status"), Byte("flag"))
				r = c.parse(buddy_data[:8])
				nick = user.id2nick(r.buddyid)
				buddy_data = buddy_data[6:]
				log.debug(nick + " is online")
			
			if nick != "":
				# Check for a name because sometimes weird and random data is returned.. Also a name is needed
				# to find the user to update.
				# user.updateStatus(nick)
				pass
			i+=1

def parse_user_status_update(packet):
	""" Parses a user status update, fired when a user joins a game, logs on?, etc. 
		Updates the state of buddies.
	"""

	pass

def parse_whisper(packet):
	""" A normal whisper from anyone """
	c = Struct("packet", ULInt16("size"), ULInt16("packetid"), CString("name"), CString("message"))
	r = c.parse(packet)
	log.notice(r.name + ": " + r.message)
