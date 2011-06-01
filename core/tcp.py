""" 
TCP packet related functions and management.
	
See: http://honwiki.net/wiki/Chat_Protocol

Receive TCP packets and parse them.

My documentation of packets.

Client -> Server packets.

	+ 0x0C00  - Login request. 101 bytes.
		+ ULInt16: aid - Account id, pad wit 0x00
		+ String: cookie - Pad and +1 the len
		+ String: ip - Pad and +1 the len
		+ String: authHash - Pad and +1 the len
		+ ULInt32: proto - Chat protocol version
		+ ULInt32: unknown - No idea, Normal hon client uses 0x01, HoNPurple uses 0x05, HoNChatPlus doesn't use anything, it has a weird way of doing it.
		+ ULInt8: unknown - No idea, empty padding I guess... Could be merged with the protocol i.e. 0x0D 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00
	
	+ 0x02  - Pong, response to ping.

Server -> Client packets

	+ 0x1C00 - Login acknowlegement. 4 Bytes.
		+ ULInt16: size
		+ ULInt16: packetid
	
	+ 0x0B - Initial status, sent after 0x1C00. Contains initial data, channels, players online? amongst other stuff.
		+ ULInt16: size
		+ ULInt16: packetid
		+ ????

	+ 0x0C - Status update... Friends joining/leaving games, etc?
		+ ULInt16: size
		+ ULInt16: packetid
		+ ????
	
	+ 0x08 - Whisper. Basic whisper message.
		+ ULInt16: size
		+ ULInt16: packetid
		+ ?String: name?
		+ ?String: message.?
	
	+ 0x68 - Number of players online. Sent every 30 seconds. Contains 35 Bytes of data.
		+ ULInt16: size
		+ ULInt16: packetid
		+ ???

	:STATES:
	The available states of a user.
		+ 0x00 - Offline
			+ 0x03 - Online
			+ 0x04 - In Lobby
			+ 0x05 - In Game
	
	:FLAGS:
	The available accout flags of a user
		+ 0x00 - None, basic user.
		+ 0x01 - Moderator
		+ 0x02 - Founder, S2 Games employee?
		+ 0x40 - Prepurchased, gold shield? 

	Notes:
		* When sending a login request, pad the strings with zeros, is this the same for all packets?
		* When sending a login request, pad the account id with 0x00 once. Why?
		* Server -> Client packets are always preceded by it's length
		* Must send a chat protocol version!
"""
import log
import struct
from lib.construct import *

PROTO_VER = 0x0D # Protocol version 13.

""" Magical packet handlers
	
	Idea is to register each packet handler and put it in the packet handlers list.
	Then each packet will have it's packet id checked against that list.
"""

class Handler(object):
	pass

_packetHandlers = []

# Unused, would be nice to have.
def registerPacketHandler(packetid, function):
	global _packetHandlers
	handler = Handler()
	handler.packetid = packetid
	handler.function = function
	if handler not in _packetHandlers:
		_packetHandlers.append(handler)
		log.debug("Registered a handler for " + str(packetid) + " " + str(function))

# Unused, would be nice to have.
def parsePacket(socket, packet):
	global _packetHandlers

	log.debug("Recieved a packet")
	r = Struct("response", ULInt16("size"), ULInt16("packetid"))
	log.debug(r.parse(packet))

	for handler in _packetHandlers:
		if r.packetid == handler.packetid:
			handler.function(socket)

def shitParsePacket(socket, packet):
	if len(packet) == 0:
		return
	
	r = Struct("response", ULInt16("size"), ULInt16("packetid"))
	data = r.parse(packet)
	log.debug("<< 0x%x - Len: %d" % (data.packetid, len(packet)))
	if data.packetid == 0x2A00:
		sendPong(socket)
	elif data.packetid == 0x68:
		parseTotalOnline(socket, packet)

def greet(socket, aid, cookie, ip, auth):
	""" Sends the initial login request to the chat server, sends the account id, cookie, ip, auth hash and chat protocol version.
		
		Server responds with a response (0x1C00) to acknlowdge the login and also the intial data (0x0B)

	 """

	# Build the packet
	c = Struct("login",
			ULInt16("id"), # 0x0C00
			ULInt32("aid"),
			String("cookie", len(cookie)+1, encoding="utf8", padchar = "\x00"),
			String("ip", len(ip)+1, encoding="utf8", padchar = "\x00"),
			String("auth", len(auth)+1, encoding="utf8", padchar = "\x00"),
			ULInt32("proto"), # Protocol version?
			ULInt32("nan"), # Unknown also, 5? HoN uses 0x01, HonPurple uses 0x05.. Honchatplus uses...?
			ULInt8("unknown") # no idea?
		)

	req = c.build(Container(id=0x0C00, aid=aid+0x00, cookie=unicode(cookie), ip=unicode(ip), auth=unicode(auth), 
							proto=0x0D, nan=0x05, unknown=0x00))
	b = socket.send(req)

	log.notice("Authenticating...")

	""" Check that the server sends the ack response (0x0200 0x1C00). If it does, then all is good to go
		and packets will be sent and received nicely, otherwise the log in failed and 
		something is wrong. """

	resp = socket.recv(1024)
	if len(resp) is None or 0:
		return 0
			
	# Handle the login response here
	r = Struct("response", ULInt16("size"), ULInt16("packetid"))
	data = r.parse(resp)
	log.debug("<< 0x%x" % data.packetid)

	if data.packetid == 0x1C00:
		# Success! Logged in!
		return 1

	# Something went wrong...
	return 0

""" Client to server methods """
def sendPong(socket):
	""" Replies to a ping request (0x2A00) with a pong response (0x2A01) """
	c = Struct("pong", ULInt16("packetid"))
	req = c.build(Container(packetid=0x2A01))

	socket.send(req)
	log.debug(">> 0x%x" % c.parse(req).packetid)


""" Server to Client methods """
def parseTotalOnline(socket, packet):
	""" Gets the number of players online """

	c = Struct("packet", ULInt16("size"), ULInt16("packetid"), ULInt32("count"), CString("unknown"))
	r = c.parse(packet)
	log.notice(str(r.count) + " players online.")

def parseInitialStatuses(socket, packet):
	""" Initial status packet contains the following
			+ Channels
			+ ...
	"""
	pass

def parseStatusUpdate(socket, packet):
	""" Status updates contain...? """
	pass