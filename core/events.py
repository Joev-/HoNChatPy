import time
from lib.honcore import handler
import log

@handler.event('all')
def on_event(packet_id, packet):
	""" Debug logging """
	log.debug("<< 0x%x " % packet_id)

@handler.event('ping')
def on_ping():
	""" Ping...Pong... """
	log.debug("Pong")

@handler.event('total_online')
def on_total_online(players_online):
	log.info(str(players_online) + " players online.")
