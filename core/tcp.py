""" 
TCP packet related functions and management.
	
See: http://honwiki.net/wiki/Chat_Protocol

Receive TCP packets and parse them.

My documentation of packets.

Client -> Server packets.

	+ 0x0C00  - Login, sent when logging in?
		+ ULInt16: aid - Account id, pad wit 0x00
		+ STRING: cookie - Pad and +1 the len
		+ STRING: ip - Pad and +1 the len
		+ STRING: authHash - Pad and +1 the len
		+ ULInt32: proto - Chat protocol version
		+ ULInt32: unknown - No idea, Normal hon client uses 0x01, HoNPurple uses 0x05, HoNChatPlus doesn't use anything, it has a weird way of doing it.
		+ ULInt8: unknown - No idea, empty padding I guess... Could be merged with the protocol i.e. 0x0D 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00
	
	+ 0x02  - Pong, response to ping.


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

def greet(socket, aid, cookie, ip, auth):
	""" Sends the initial login request to the chat server, sends the account id, cookie, ip, auth hash and chat protocol version.
		
		Server responds with two packets, one empty and one containing a tiny response. (0x00?). This must be responded to with...?

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
				ULInt8("unknown")) # no idea?

	req = c.build(Container(id=0x0C00, aid=aid+0x00, cookie=unicode(cookie), ip=unicode(ip), auth=unicode(auth), 
							proto=0x0D, nan=0x05, unknown=0x00))
	log.debug(req)
	socket.send(req)

	log.notice("Authenticating...")

	resp = socket.recv(500)
	if len(resp) != 0:
		log.debug("Recieved a response!")
		log.debug(resp)
		r = Struct("response", ULInt32("size"), Byte("status"))
		log.debug(r.parse(resp))

		# Handle the login response here
		
		return 1
	
	return 0

def pong(socket):
	c = Struct("pong", Byte("id"))
