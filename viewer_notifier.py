#!/usr/bin/python

hitbox_user = "put your hitbox username here"
hitbox_pass = "put your password here"
hitbox_dologin = True;

import os
import urllib
import urllib2
import time
import json
import pprint
import winsound, sys

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)

class apiHitbox:
	def __init__(self, hitbox_user, hitbox_pass, login):
		self.user = hitbox_user
		self.password = hitbox_pass
		self.api_url = "https://www.hitbox.tv/api/"
		self.authtoken = ""

		if(login):
			self.getToken()

	def getViewerCount(self):
		data = self.readAPI( "media/status/"+self.user)
		return data["media_views"]

	def getUserInfos(self):
		data = self.readAPI( "user/"+self.user)
		return data

	def readAPI(self, command):
		req =  urllib.urlopen(self.api_url+command)
		reply = req.read()
		jsondata = json.loads(reply)
		req.close()
		return jsondata

	def getToken(self):
		#logging in and getting a token.
		values = {'login' : self.user, 'pass' : self.password, 'app' : "desktop"}
		data = urllib.urlencode(values)
		req =  urllib2.urlopen(self.api_url+"auth/token",data)
		reply = req.read()
		jsondata = json.loads(reply)
		req.close()
		print "Logging in..."
		if('authToken' in jsondata.keys()):
			print "...success!"
			self.authtoken = jsondata['authToken']
			#print self.authtoken
		else:
			print "...failed!"	

viewers = 1
hitbox = apiHitbox(hitbox_user,hitbox_pass, hitbox_dologin)

while(True):
	
	curr_viewers = int(hitbox.getViewerCount())
	if(curr_viewers > viewers):
		print str(curr_viewers - viewers) + " joined."
		beep("ding")
		print str(curr_viewers) + " viewers.\n"
	elif(curr_viewers < viewers):
		print str(viewers - curr_viewers) + " left."
		beep("dong")
		print str(curr_viewers) + " viewers."
	viewers = curr_viewers


	time.sleep(5.0);