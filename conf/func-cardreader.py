from evdev import InputDevice, ecodes, list_devices
from select import select

# prüfe Reader und richte ihn ein
if not os.path.isfile(path + '/conf/if-cardreader.py'):
    devices = [InputDevice(fn) for fn in list_devices()]
    i = 0
    print("Choose the reader from list")
    for dev in devices:
    	print(i, dev.name)
    	i += 1

    dev_id = int(input('Device Number: '))

    with open(path + '/conf/if-cardreader.py','w') as f:
    	f.write(devices[dev_id].name)
    	f.close()


# Cardreader konfigurieren
with open(path + '/conf/reader.py','r') as f:
    deviceName = f.read()
    devices = [InputDevice(fn) for fn in list_devices()]
for device in devices:
    if device.name == deviceName:
        global reader
        reader = device
        break
try:
    reader
except:
    logger.error('Could not find the device %s\n. Make sure is connected' % deviceName)
    sys.exit()
