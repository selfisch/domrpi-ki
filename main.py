#!/usr/bin/env python

# Requirements apt: python-dev
# Requirements pip: MPDClient, evdev,

import csv, os, sys

# in das Verzeichnis des Skript wechseln
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('./conf')

from evdev import InputDevice
from select import select
from random import randint
import logging
from input import dev
from mpd import MPDClient

# MPDClient config
client = MPDClient()    # create client object
client.timeout = 10     # network timeout in seconds (floats allowed), default: None
client.idletimeout = None

# logger konfigurieren
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.FileHandler('log/aiwa.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def mpdConnect():
	client.connect("localhost", 6600)

def mpdDisconnect():
	client.disconnect()

# linke Aussentaste an der Maus startet eine random Playliste
def linksAussen():
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

def linkeMaustaste():
  mpdConnect()
  state = client.status()['state'].split(":")
  if 'play' in state:
    client.pause()
  elif 'pause' in state:
    client.play()
  mpdDisconnect()

def rechteMaustaste():
  mpdConnect()
  state = client.status()['state'].split(":")
  if 'play' in state:
    client.stop()
  else:
    client.stop()
  mpdDisconnect()

def rechtsAussen():
  mpdConnect()
  client.stop()
  client.clear()
  client.add('http://ndr-ndr2-niedersachsen.cast.addradio.de/ndr/ndr2/niedersachsen/mp3/128/stream.mp3')
  client.play()
  mpdDisconnect()

def main():
	while True:
	    r,w,x = select([dev], [], [])
	    for event in dev.read():
			if event.code == 8:
				#print "wheel"
				if event.value == 1:
				    os.system("amixer -q sset Master 1%+")
				elif event.value == -1:
				    os.system("amixer -q sset Master 1%-")
			elif event.code == 272 and event.value == 1:
				logger.debug('linkeMaustaste gedrueckt')
				linkeMaustaste()
			elif event.code == 273 and event.value == 1:
				logger.debug('linkeMaustaste gedrueckt')
				rechteMaustaste()
			elif event.code == 274 and event.value == 1:
				logger.debug('Mausrad gedrueckt')
				os.system("shutdown -h now")
				logger.info('fahren auf Anforderung herunter')
			elif event.code == 275 and event.value == 1:
				logger.debug('links aussen gedrueckt')
				linksAussen()
			elif event.code == 276 and event.value == 1:
				logger.debug('rechts aussen gedrueckt')
				rechtsAussen()

# und laufen lassen
if __name__ == "__main__":
  try:
    logger.info('Starte die Anwendung')
    main()
  except (SystemExit):
	logger.info("Anwendung beendet")
  except (KeyboardInterrupt):
	logger.info("via Tastatur beendet")
  except mpd, m:
	logger.debug("mpd meldet {0}",format(str(m)))
	logger.info("mpd meldet {0}",format(str(m)))
  except Exception, e:
	logger.error("main crashed {0}".format(str(e)))
  except:
    logger.info("Unbekannter Fehler:", sys.exc_info()[0])
    raise
