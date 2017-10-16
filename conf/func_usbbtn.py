from evdev import InputDevice, ecodes, list_devices
from select import select

class usbbtn:
    def __init__():
        # prüfe die Buttons und richte sie ein
        if not os.path.isfile(path + '/conf/if-usbbtn.py'):
            devices = [InputDevice(fn) for fn in list_devices()]
            i = 0
            print("Choose button input from list")
            for dev in devices:
            	print(i, dev.name)
            	i += 1

            dev_id = int(input('Device Number: '))

            with open(path + '/conf/if-usbbtn.py','w') as f:
            	f.write(devices[dev_id].name)
            	f.close()

        # Maus konfigurieren
        with open(path + '/conf/if-usbbtn.py','r') as f:
            deviceName = f.read()
            devices = [InputDevice(fn) for fn in list_devices()]
        for device in devices:
            if device.name == deviceName:
                global usbbtn
                usbbtn = device
                break
        try:
            usbbtn
        except:
            logger.error('Could not find the device %s\n. Make sure is connected' % deviceName)
            sys.exit()


    def buttons(x, y):
        logger.info('starte Buttons')
        while True:
            r, w, x = select([usbbtn], [], [])
            for event in usbbtn.read():
                logger.info('Button wurde gedrückt.')
                logger.info(event)
                print(event)
