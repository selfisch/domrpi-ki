#!/usr/bin/python

# Requirements apt: python-dev
# Requirements pip: MPDClient, evdev,

from evdev import InputDevice
from select import select
import os
from mpd import MPDClient

# MPDClient config
client = MPDClient()    # create client object
client.timeout = 10     # network timeout in seconds (floats allowed), default: None
client.idletimeout = None
client.connect("localhost", 6600)

#dev = InputDevice('/dev/input/event13') # This can be any other event number. On$
dev = InputDevice('/dev/input/event0') # This can be any other event number. On$

while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
    # The event.code for a scroll wheel event is 8, so I do the following
    # button left 272, right 273
        if event.code == 8:
            #print "wheel"
            #print(event.value)
            if event.value == 1:
                os.system("amixer -q sset Master 1%+")
            elif event.value == -1:
                os.system("amixer -q sset Master 1%-")
        elif event.code == 272 and event.value == 1:
            #print "linker Knopf"
            #print(event.value)
            #print(event.code)
            #print(event.type)
            #client.next()
            if 'play' in state:
                client.pause()
            elif 'pause' in state:
                #print("rechte Maustaste")
                client.play()
        elif event.code == 273 and event.value == 1:
            #print "rechter Knopf"
            #print(event.value)
            state = client.status()['state'].split(":")
            #print(state)
            if 'play' in state:
                client.stop()
                client.clear()
            elif 'stop' in state:
                #print("rechte Maustaste")
                client.clear()
                client.add('http://ndr-ndr2-niedersachsen.cast.addradio.de/ndr/ndr2/niedersachsen/mp3/128/stream.mp3')
                client.play()
        elif event.code == 275:
            print "links aussen"
            #print(event.value)
        elif event.code == 276:
            ##print "rechts aussen"
            os.system("sudo shutdown -h now")
            #print(event.value)
