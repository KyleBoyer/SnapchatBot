#!/usr/bin/env python

from pysnap import Snapchat
import os
import hashlib
import datetime
import sys
today = datetime.date.today().strftime('%m.%d.%y')
s = Snapchat()
updates = s.logina("USERNAME", "AUTH_TOKEN")
#updates = s.login("USERNAME", "PASSWORD")
print "\nLogged in with this auth token: " + s.auth_token
def startm(s):
	options = {1 : block,
                2 : unblock,
                3 : add,
                4 : delete,
                5 : getblocked,
                6 : normal,
                7 : upload,
                8 : exit,
	}
	print("\nList of Modes:\n1. Block User\n2. Unblock User\n3. Add Friend\n4. Delete Friend\n5. Get List of Blocked Users\n6. Add Snaps to Story\n7. Upload Local Image\n8. Exit")
	whattodo = input("Which mode would you like: ")
	if int(whattodo) in (1, 2, 3, 4, 5, 6, 7, 8):
		print "Your choice is " + str(whattodo) + "."
		options[int(whattodo)](s)
	else:
		print "Invalid Option, you needed to type a 1, 2, 3, 4, 5, 6, 7, or 8..."
		startm(s)
def block(s):
	print ""
	blockwho = raw_input("Who should be blocked: ")
	print s.block(blockwho)
	startm(s)
def exit(s):
	sys.exit()
def add(s):
	print ""
	addwho = raw_input("Who should be added: ")
	print s.add_friend(addwho)['message']
	startm(s)
def upload(s):
	print ""
	path = raw_input("Where is the image that should be uploaded: ")
	path = path.rstrip()
	path = path.lstrip()
	data = ""
	if not os.path.exists(path):
		raise ValueError('No such file: {0}'.format(path))
	with open(path, 'rb') as f:
		data = f.read()
	s.retry_post_story(data, hashlib.md5(s.username + today).hexdigest())
	print "Added Image!"
	startm(s)
def delete(s):
	print ""
	addwho = raw_input("Who should be deleted: ")
	print s.delete_friend(addwho)
	startm(s)
def getblocked(s):
	print ""
	print "The following users are blocked:"
	for friend in s.get_blocked():
		print friend['name']
	startm(s)
def unblock(s):
	print ""
	print "The following users are blocked:"
	for friend in s.get_blocked():
		print friend['name']
	unblockwho = raw_input("Who should be unblocked: ")
	print s.unblock(unblockwho)
	startm(s)
def normal(s):
	print ""
	for friend in [friend['name'] for friend in s.get_updates()['friends_response']['added_friends'] if friend['type'] == 1]:
		s.add_friend(friend)
		print "Added: " + friend
	convos = [convo for convo in s.get_updates()['conversations_response']]
	for convo in convos:
		for snap in convo['pending_received_snaps']:
			snapdata = s.get_blob(snap['id'])
			#with open(path, 'wb') as f:
			#	f.write(snapdata)
			if not (snapdata is None):
				s.retry_post_story(snapdata, hashlib.md5(snap['sn'] + today).hexdigest())
				s.mark_viewed(snap['id'])
				print "Added: " + snap['id']
		s.clear_convo(convo['id'])
	startm(s)
startm(s)
