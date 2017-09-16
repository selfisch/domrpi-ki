#!/usr/bin/python3

import os.path
from evdev import InputDevice, list_devices

devices = [InputDevice(fn) for fn in list_devices()]
path = os.path.dirname(os.path.realpath(__file__))
i = 0
print("Choose the reader from list")
for dev in devices:
	print(i, dev.name)
	i += 1

dev_id = int(input('Device Number: '))

with open(path + 'conf/reader.py','w') as f:
	f.write(devices[dev_id].name)
	f.close()
