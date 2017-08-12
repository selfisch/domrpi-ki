#!/usr/bin/python

from evdev import InputDevice
from select import select
import os

dev = InputDevice('/dev/input/event0') # This can be any other event number. On$

while True:
  r,w,x = select([dev], [], [])
  for event in dev.read():
    # The event.code for a scroll wheel event is 8, so I do the following
    # button left 272, right 273
    if event.code == 8:
      print "wheel"
      print(event.value)
      if event.value == 1:
        os.system("amixer -q sset Master 1%+")
      elif event.value == -1:
        os.system("amixer -q sset Master 1%-")
    elif event.code == 272:
      print "left button"
      print(event.value)
    elif event.code == 273:
      print "right button"
      print(event.value)
    else:
      print(event.value)
