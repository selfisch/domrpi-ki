import csv, os
from random import randint
from mpd import MPDClient


class mopidy:
		def __init__(self):
				# MPDClient config
				client = MPDClient()    # create client object
				client.timeout = 10     # network timeout in seconds (floats allowed), default: None
				client.idletimeout = None


		def mpdConnect(self):
				client.connect("localhost", 6600)


		def mpdDisconnect(self):
				client.disconnect()


		def randomPlaylist():
				mpdConnect()
				uris = csv.reader(open("plist.csv", "r"),delimiter=';')
				plist = []
				plist.extend(uris)

				plist_zahl = randint(0, len(plist))
				if plist_zahl >= 1:
					plist_zahl = plist_zahl - 1
				uri = str(plist[plist_zahl][1])
				play_mode = str(plist[plist_zahl][2])
				uri = uri.replace('[','')
				uri = uri.replace(']','')
				uri = uri.replace('\'','')
				logger.debug("URI to pass: " + uri)
				logger.debug("Playmode: " + play_mode)
				client.clear()
				client.add(uri)
				if play_mode == 'play':
					client.random(0)
					client.play()
				elif play_mode == 'shuffle':
					client.random(1)
					client.play()
				mpdDisconnect()
