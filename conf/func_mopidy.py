import csv, os, logging, time
from random import randint
from mpd import MPDClient
from persistMPDclient import PersistentMPDClient

logger = logging.getLogger('main')

global client
client = MPDClient()    # create client object

class mopidy:
	def mpdConnect():
		# MPDClient config
		client.timeout = 10
		client.idletimeout = None
		client.connect("localhost", 6600)

	def mpdDisconnect():
		client.close()
		client.disconnect()


	def randomPlaylist():
		mopidy.mpdConnect()
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
		mopidy.mpdDisconnect()


	def playList(uri, play_mode):
		mopidy.mpdConnect()
		client.clear()
		client.add(uri)
		if play_mode == 'play':
			client.random(0)
			client.play()
		elif play_mode == 'shuffle':
			client.random(1)
			client.play()
		mopidy.mpdDisconnect()


	def play():
		mopidy.mpdConnect()
		#mpd_status = client.ping()
		#logger.debug('mpd status: ' + str(mpd_status))
		#state = client.status()['state'].split(":")
		#if 'play' in state:
		#	client.pause()
		#elif 'pause' in state:
		client.play()
		mopidy.mpdDisconnect()


	def stop():
		mopidy.mpdConnect()
		#state = client.status()['state'].split(":")
		#if 'play' in state:
		client.stop()
		mopidy.mpdDisconnect()


	def next():
		mopidy.mpdConnect()
		# state = client.status()['state'].split(":")
		# if 'play' in state:
		client.next()
		mopidy.mpdDisconnect()


	def previous():
		mopidy.mpdConnect()
		#state = client.status()['state'].split(":")
		#if 'play' in state:
		client.previous()
		mopidy.mpdDisconnect()


	# def mpdConnect(self):
	# 	try:
	# 		delay = 0
	# 		# MPDClient config
	# 		client.timeout = 10
	# 		client.idletimeout = None
	# 		client.connect("localhost", 6600)
	# 		while True:
	# 			if delay <= 30:
	# 				logger.debug('mpdConnect delay: ' + str(delay))
	# 				delay = delay + 1
	# 				time.sleep(1)
	# 			elif delay > 30:
	# 			  logger.debug('mpdConnect ping')
	# 			  client.ping()
	# 			  delay = 0
	# 	except Exception as e:
	# 			logger.error("main crashed {0}".format(str(e)))
	# 			logger.exception("Error")
	# 			raise
	# 	except:
	# 			logger.info("Unbekannter Fehler:", sys.exc_info()[0])
	# 			raise
	# 	pass
