#!/usr/bin/python

# Requirements apt: python-dev
# Requirements pip: MPDClient, evdev,

from evdev import InputDevice
from select import select
import os
from mpd import MPDClient
import re
from CardList import CardList

# MPDClient config
client = MPDClient()    # create client object
client.timeout = 10     # network timeout in seconds (floats allowed), default: None
client.idletimeout = None
client.connect("localhost", 6600)

# linke Aussentaste an der Maus startet eine random Playliste
def play(client, plist):
	try:
		client.stop()
		client.clear()
		client.add(plist)
		if re.search('playlist',plist):
			client.shuffle()
		client.play()
	except:
		print 'Could not play playlist %s' % plist

# zweite Maus fuer Test an meinem Rechner
#dev = InputDevice('/dev/input/event13') # This can be any other event number. On$

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
                client.play()
        elif event.code == 273 and event.value == 1:
            #print "rechter Knopf"
            state = client.status()['state'].split(":")
            if 'play' in state:
                client.stop()
        elif event.code == 274 and event.value == 1:
            #print "Mausrad klick"
            os.system("sudo shutdown -h now")
        elif event.code == 275:
            #print "links aussen"
            #card = reader.readCard()
            card = 1
            print 'Read card', card
            plist = cardList.getPlaylist(card)
            print 'Playlist', plist
            if plist != '':
                if plist=='pause':
                    client.pause()
                else:
                    play(client, plist)
                    #client.close()
        elif event.code == 276:
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
