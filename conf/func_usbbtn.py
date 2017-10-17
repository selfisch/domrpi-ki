from evdev import InputDevice, ecodes, list_devices
from select import select
import os.path, sys, logging, csv, time

logger = logging.getLogger('main')


class usbbtn:
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        # prüfe die Buttons und richte sie ein
        if not os.path.isfile(path + '/if_usbbtn.py'):
            devices = [InputDevice(fn) for fn in list_devices()]
            i = 0
            print("Choose button input from list")
            for dev in devices:
            	print(i, dev.name)
            	i += 1

            dev_id = int(input('Device Number: '))

            with open(path + '/if_usbbtn.py','w') as f:
            	f.write(devices[dev_id].name)
            	f.close()

        # USB Buttons konfigurieren
        with open(path + '/if_usbbtn.py','r') as f:
            deviceName = f.read()
            devices = [InputDevice(fn) for fn in list_devices()]
        for device in devices:
            if device.name == deviceName:
                global if_usbbtn
                if_usbbtn = device
                break
        try:
            if_usbbtn
        except:
            logger.error('Could not find the device %s\n. Make sure is connected' % deviceName)
            sys.exit()


    def check_usbbtn(self):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/if_usbbtn.py','r') as f:
            deviceName = f.read()
        return deviceName


    def buttons(val):
        if val == 589827:
            print('vol up')
        elif val == 589825:
            print('vol down')


    def button_press(self):
        logger.debug('starte USB Buttons')
        global time_stamp
        time_stamp = time.time()
        while True:
            r, w, x = select([if_usbbtn], [], [])
            for event in if_usbbtn.read():
                if event.code == 4:
                    time_now = time.time()
                    if (time_now - time_stamp) >= 0.5:
                        logger.debug('Button wurde gedrückt.')
                        logger.info(event)
                        usbbtn.buttons(event.value)
                    time_stamp = time_now
