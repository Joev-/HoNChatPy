#! /usr/bin/env python

import sys
from phpserialize import *
import getopt

def getBasicInfo():
		f = open('raw.txt', 'rU')
		feedIn = f.read()

		f.close()

		data = loads(feedIn)

		userData = {}

		userData['ip'] = data['ip']
		userData['master_srv'] = data['master_svr']
		userData['auth_hash'] = data['auth_hash']
		userData['super_id'] = data['super_id']
		userData['cookie'] = data['cookie']
		userData['nickname'] = data['nickname']
		userData['chat_url'] = data['chat_url']

		f = open('user-data.txt', 'w')
		print >>f, "Unstructured user data:\n"
		print >>f, userData
		print >>f, "\n\nStructured user data:\n"

		## userData vs userData.iterkeys() vs userData.keys() vs userData.items()?
		for key in userData:
			print >>f, key, " - ", userData[key]
		f.close

		# j = open('clan_members.txt', 'w')
		# print >>j, "Listing clan members and account ids"
		# for members in data["clan_roster"]:
		# 	print >>j, "# %s - %s" % (data["clan_roster"][members]["account_id"], data["clan_roster"][members]["nickname"])
		# j.close()

		# w = open('clan_roster.txt', 'w')
		# print >>w, data["clan_roster"]
		# w.close()

def main():
	getBasicInfo()

if __name__ == '__main__':
	main()