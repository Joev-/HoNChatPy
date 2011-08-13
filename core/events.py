import time
from lib.honcore import handler
import log

@handler.event_handler('all')
def on_event(packet_id, packet):
	""" 
	On all events.
	Nice for packet logging.
	"""
	log.debug("<< 0x%x " % packet_id)

@handler.event_handler('ping')
def on_ping():
	""" 
	Pongs are handled silently by the library, but this
	can be used for anything else :)
	"""
	log.debug("Pong")

@handler.event_handler('total_online')
def on_total_online(players_online):
	log.info(str(players_online) + " players online.")

@handler.event_handler('whisper')
def on_whisper_recieved(name, message):
	log.info("%s: %s" % (name, message))