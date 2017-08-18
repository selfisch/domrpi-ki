#!/usr/bin/python

# Requirements apt: python-dev
# Requirements pip: MPDClient, evdev,

from evdev import InputDevice
from select import select
from mpd import MPDClient
from random import randint
import csv
import os

# MPDClient config
client = MPDClient()    # create client object
client.timeout = 10     # network timeout in seconds (floats allowed), default: None
client.idletimeout = None
client.connect("localhost", 6600)


# linke Aussentaste an der Maus startet eine random Playliste
def playList():
	uris = csv.reader(open("plist.csv", "r"),delimiter=';')
	plist = []
	plist.extend(uris)

	plist_zahl = randint(0, len(plist))
	plist_zahl = plist_zahl - 1
	#print(plist_zahl)
	#print(plist[plist_zahl])
	uri = str(plist[plist_zahl])
	uri = uri.replace('[','')
	uri = uri.replace(']','')
	uri = uri.replace('\'','')
	#print(uri)
	client.clear()
	client.add(uri)
	client.play()

# zweite Maus fuer Test an meinem Rechner
#dev = InputDevice('/dev/input/event15') # This can be any other event number. On$

# Maus an der Aiwa
dev = InputDevice('/dev/input/event0') # This can be any other event number. On$

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
            #print "linker Knopf"
            state = client.status()['state'].split(":")
            if 'play' in state:
                client.pause()
            elif 'pause' in state:
                #print("rechte Maustaste")
                client.play() and event.value == 1
        elif event.code == 273 and event.value == 1:
            #print "rechter Knopf"
            state = client.status()['state'].split(":")
            if 'play' in state:
                client.stop()
        elif event.code == 274 and event.value == 1:
            #print "Mausrad klick"
            os.system("sudo shutdown -h now")
        elif event.code == 275 and event.value == 1:
            #print "links aussen"
			playList()
        elif event.code == 276 and event.value == 1:
            #print "rechts aussen"
            state = client.status()['state'].split(":")
            if 'play' in state:
                client.stop()
                client.clear()
            elif 'stop' in state:
                #print("rechte Maustaste")
                client.clear()
                client.add('http://ndr-ndr2-niedersachsen.cast.addradio.de/ndr/ndr2/niedersachsen/mp3/128/stream.mp3')
                client.play()
