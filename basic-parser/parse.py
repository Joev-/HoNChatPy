#! /usr/bin/env python

import sys
from phpserialize import *
import getopt

def prnDict(aDict, br='\n', html=0,
            keyAlign='l',   sortKey=0,
            keyPrefix='',   keySuffix='',
            valuePrefix='', valueSuffix='',
            leftMargin=0,   indent=1 ):
    '''
return a string representive of aDict in the following format:
    {
     key1: value1,
     key2: value2,
     ...
     }

Spaces will be added to the keys to make them have same width.

sortKey: set to 1 if want keys sorted;
keyAlign: either 'l' or 'r', for left, right align, respectively.
keyPrefix, keySuffix, valuePrefix, valueSuffix: The prefix and
   suffix to wrap the keys or values. Good for formatting them
   for html document(for example, keyPrefix='<b>', keySuffix='</b>'). 
   Note: The keys will be padded with spaces to have them
         equally-wide. The pre- and suffix will be added OUTSIDE
         the entire width.
html: if set to 1, all spaces will be replaced with '&nbsp;', and
      the entire output will be wrapped with '<code>' and '</code>'.
br: determine the carriage return. If html, it is suggested to set
    br to '<br>'. If you want the html source code eazy to read,
    set br to '<br>\n'

version: 04b52
author : Runsun Pan
require: odict() # an ordered dict, if you want the keys sorted.
         Dave Benjamin 
         http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/161403
    '''
   
    if aDict:

        #------------------------------ sort key
        if sortKey:
            dic = aDict.copy()
            keys = dic.keys()
            keys.sort()
            aDict = odict()
            for k in keys:
                aDict[k] = dic[k]
            
        #------------------- wrap keys with ' ' (quotes) if str
        tmp = ['{']
        ks = [type(x)==str and "'%s'"%x or x for x in aDict.keys()]

        #------------------- wrap values with ' ' (quotes) if str
        vs = [type(x)==str and "'%s'"%x or x for x in aDict.values()] 

        maxKeyLen = max([len(str(x)) for x in ks])

        for i in range(len(ks)):

            #-------------------------- Adjust key width
            k = {1            : str(ks[i]).ljust(maxKeyLen),
                 keyAlign=='r': str(ks[i]).rjust(maxKeyLen) }[1]
            
            v = vs[i]        
            tmp.append(' '* indent+ '%s%s%s:%s%s%s,' %(
                        keyPrefix, k, keySuffix,
                        valuePrefix,v,valueSuffix))

        tmp[-1] = tmp[-1][:-1] # remove the ',' in the last item
        tmp.append('}')

        if leftMargin:
          tmp = [ ' '*leftMargin + x for x in tmp ]
          
        if html:
            return '<code>%s</code>' %br.join(tmp).replace(' ','&nbsp;')
        else:
            return br.join(tmp)     
    else:
        return '{}'

def getBasicInfo():
		f = open('raw.txt', 'rU')
		feedIn = f.read()

		f.close()

		data = loads(feedIn)

		f = open('all.txt', 'w')
		print >>f, prnDict(data)
		f.flush()
		f.close()

		""" Get the basic user data """
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


		""" Get the buddy list data """
		buddyList = data['buddy_list'][int(userData['super_id'])]
		buddies = []

		for userKey in buddyList:
			buddy = {}
			userKey = int(userKey) # MUST BE INT
			buddy['status'] = buddyList[userKey]['status']
			buddy['accId'] = buddyList[userKey]['account_id']
			buddy['clanName'] = buddyList[userKey]['clan_name']
			buddy['buddy_id'] = buddyList[userKey]['buddy_id']
			buddy['createTime'] = buddyList[userKey]['create_time']
			buddy['clanTag'] = buddyList[userKey]['clan_tag']
			buddy['nick'] = buddyList[userKey]['nickname']
			buddies.append(buddy)
		
		f = open('buddies.txt', 'w')
		print >>f, "Buddy list."
		print >>f, "Number of buddies: " + str(len(buddies)) + "\n"

		for buddy in buddies:
			if str(buddy['clanTag']) != "None":
				tag = "[" + buddy['clanTag'] + "]"
			else:
				tag = ""

			print >>f, tag + buddy['nick']
		f.close


		""" Get the banlist data """
		bannedData = data['banned_list'][int(userData['super_id'])]
		bannedList = []

		for userKey in bannedData:
			user = {}
			userKey = int(userKey) # MUST BE INT
			user['account_id'] = bannedData[userKey]['account_id'] # This is... MY account id, wtf.
			user['banned_id'] = bannedData[userKey]['banned_id']
			user['reason'] = bannedData[userKey]['reason']
			user['nickname'] = bannedData[userKey]['nickname']
			bannedList.append(user)
		
		f = open('banned_list.txt', 'w')
		print >>f, "Ban list."
		print >>f, str(len(bannedList)) + " twats bannned.\n"

		for user in bannedList:
			print >>f, user['nickname'] + " - " + user['reason']
		f.close


		""" Get the ignore list data """
		ignoreData = data['ignored_list'][int(userData['super_id'])]
		ignoreList = []

		for userKey in ignoreData:
			user = {}
			userKey = int(userKey) # MUST BE INT
			user['account_id'] = ignoreData[userKey]['account_id'] # This is... MY account id, wtf.
			user['ignored_id'] = ignoreData[userKey]['ignored_id']
			user['nickname'] = ignoreData[userKey]['nickname']
			ignoreList.append(user)
		
		f = open('ignore_list.txt', 'w')
		print >>f, "Ignore list."
		print >>f, str(len(ignoreList)) + " cunts ignored.\n"

		for user in ignoreList:
			print >>f, user['nickname']
		f.close

		""" Get the clan list data """
		clanData = data['clan_roster']
		clanList = []

		for userKey in clanData:
			user = {}
			userKey = int(userKey) # MUST BE INT
			user['account_id'] = clanData[userKey]['account_id'] # This is... MY account id, wtf.
			user['nickname'] = clanData[userKey]['nickname']
			clanList.append(user)
		
		f = open('clan_list.txt', 'w')
		print >>f, "Clan list."
		print >>f, str(len(clanList)) + " awesome clan memebers!!!!.\n"

		for user in clanList:
			print >>f, user['nickname']
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