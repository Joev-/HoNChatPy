""" 
TCP packet related functions and management.
	
See: http://honwiki.net/wiki/Chat_Protocol

Receive TCP packets and parse them.

This list is from HoNChat+ DATED 17 MARCH 2011, contains more than the hon wiki page however.
Packets, Server -> Client.
	+ 0x00  - Ping
	+ 0x03  - Regular chat message
	+ 0x04  - 'You' joined a channel
	+ 0x05  - User joined a channel
	+ 0x06  - User left a channel
	+ 0x07  - Unknown
	+ 0x08  - Whisper (Whisper)
	+ 0x09  - User not online, result from whispering
	+ 0x0b  - Buddy list update
	+ 0x0c  - User status update
	+ 0x0d  - Invite to match making game
	+ 0x12 - Notification of some sort
	+ 0x13  - Clan message (Clan)
	+ 0x1c  - Private chat message, those graphical chat messages from F6
	+ 0x1d  - User not online, result from a private chat message
	+ 0x20  - Buddy message, whisper? TODO: What's this?
	+ 0x2b  - 'Not found' result of a WHOIS
	+ 0x2c  - 'Offline' result of a WHOIS
	+ 0x2d  - 'In channels' result of a WHOIS
	+ 0x2e  - 'In game' result of a WHOIS
	+ 0x30  - Topic changed
	+ 0x31  - Kicked from channel. TODO: Check, this is the current user being kicked and not another? Or maybe it's either
	+ 0x34  - Banned from channel. TODO: Check, this is the current user being kicked and not another? "" "" "" "" ""
	+ 0x35  - Result of trying to talk when silenced in a channel. ("You are silenced")
	+ 0x38  - User silenced (initial command)
	+ 0x3a  - User promoted in the channel?
	+ 0x3b  - User demoted in the channel?
	+ 0x3e  - Auth enabled?
	+ 0x3f  - Auth disabled
	+ 0x40  - Auth user addition
	+ 0x41  - Auth user deletion
	+ 0x43  - Chane password notification
	+ 0x65  - Emote
	+ 0x66  - Availability status (AFK/DND/Available)

From honwiki, DATEd 6 MARCH 2010 - LIKELY OUTDATED.
Client -> Server packets.
	+ 0xFF  - Login, sent when logging in?
		+ DWORD: accId
		+ STRING: coookie
		+ DWORD: 0x05 - Is this the auth hash? Maybe a protocol version
	
	+ 0x02  - Pong, response to ping.
	
	+ 0x03  - Channel message.
		+ STRING: message
		+ DWORD: channelId
	
	+ 0x08  - Whisper message
		+ STRING recipient
		+ STRING message
	
	+ 0x1C  - Private message
		+ STRING recipient
		+ STRING message
	
	+ 0x1E  - Join channel
		+ STRING channelName
	
	+ 0x1F  - Channel user list
	
	+ 0x13  - Clan wide message
		+ STRING message
	
	+ 0x22  - Leave channel
		+ STRING channelName
	
	+ 0x2A  - WHOIS request
		+ STRING username
	
	+ 0x47  - Clan invite request
		+ STRING username

Server -> Client packets
	+ 0x00  - Login response
		+ Respond with 0x012A

	+ 0x01  - Ping request
		+ Respond with a pong 0x02
	
	+ 0x03  - Chat message
		+ DWORD accountId - Of who? The sender?
		+ DWORD channelId - Channel the message is for.
		+ STRING message
	
	+ 0x04  - Response to join channel.
		+ STRING channelName
		+ DWORD channelId
		+ BYTE unknown (Channel flags? 0x18)
		+ STRING topic
		+ DWORD opCount - Count of the all of the operators of the channel?
			+ DWORD accountID - ID of the operator
			+ BYTE type - Type of operator?
		+ DWORD userCcount - Count of all normal users in the channel
			+ STRING username
			+ DWORD accId
			+ BYTE state - See :STATES:
			+ BYTE flags - See :FLAGS:
	
	+ 0x05  - Player joined channel
		+ STRING username
		+ DWORD accountId
		+ DWORD channelId
		+ BTYE state - See :STATES:
		+ BYTE flags - See :FLAGS:
	
	+ 0x06 - Player left channel
		+ DWORD accountId
		+ DWORD channelId
	
	+ 0x08  - Whisper
		+ STRING username
		+ STRING message
	
	+ 0x0B  - Buddy list update
		+ DWORD count - Count of buddies
			+ DWORD accountId
			+ BYTE state - See :STATES:
			+ BYTE flags - See :FLAGS:
			+ STRING server - If in lobby/game
			+ STRING gameName - If in a game
	
	+ 0x0C  - User status update - Is this... me? The user? Or 'a' user. i.e any user?
		+ DWORD accountID
		+ BYTE state - See :STATES:
		+ BYTE flags - See :FLAGS:
		+ DWORD clanId
		+ STRING clan
		+ STRING server - If in a game/lobby
		+ STRING gameName - If in a game
			+ DWORD matchId 
	
	+ 0x13  - Clan wide message
		+ DWORD buddyId - Buddy? Surely it means clan member id...
		+ STRING message
	
	+ 0x14  - Notification message
		+ BYTE id - The id of the notification? TODO: Find out.
		+ STRING message 
	
	+ 0x1C  - Private message - Different to whisper.
		+ STRING username
		+ STRING message
	
	+ 0x1F  - Channel list - When is this recieved?
		+ DWORD count - The number of channels
			+ DWORD channelId
			+ STRING channelName
			+ DWORD userCount
	
	+ 0x2B  -  WHOIS response, not found.
		+ STRING username
	
	+ 0x2C  - WHOIS response, offline.
		+ STRING username
		+ STRING lastSeen - This is neat.
	
	+ 0x2D  - WHOIS response, user is online and in channels.
		+ STRING username
		+ DWORD count - Number of channels.
			+ STRING channelName
	
	+ 0x2E  - WHOIS response, user is in a game.
		+ STRING gameName
		+ STRING gameTime or Lobby(?)
	
	+ 0x68  - Online count
		+ DWORD number online.

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
		* DWORD - 4 byte unsigned int, little endian...
		* STRING - UTF8 string, zero terminated.
		* The packet id (e.g. 0x00) is a single byte to identify the packet type
		* Server -> Client packets are always preceded by it's length (a DWORD)
		* The user account is is not checked at the login, i.e. It's not required!
		* Must send a chat protocol version!
	
	Lol, time for code?
"""
import log
import struct
from lib.construct import *

PROTO_VER = 0x0D # Protocol version 13.

# Damn this one is messy, just testing anyway.
def greet(socket, cookie, ip, auth):

	# Build the packet
	c = Struct("login",
                Byte("id"), # 0xFF
                String("cookie",32, encoding="utf8"),
                String("ip", 11, encoding="utf8"),
                String("auth", 40, encoding="utf8"),
                ULInt32("proto")) # Protocol version?

	req = c.build(Container(id=0xFF, cookie=unicode(cookie), ip=unicode(ip), auth=unicode(auth), proto=0x0D))
	log.debug(req)
	socket.send(req)

	resp = socket.recv(500)

	log.debug(resp)
	r = Struct("response", ULInt32("size"), Byte("status"))
	log.debug(r.parse(resp))

def pong(socket):
	c = Struct("pong", Byte("id"))
