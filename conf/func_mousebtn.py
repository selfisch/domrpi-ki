from evdev import InputDevice, ecodes, list_devices
from select import select
import os.path

class mouse:
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        # prüfe Reader und richte ihn ein
        if not os.path.isfile(path + '/if_mouse.py'):
            # Frage, ob ein Kartenleser verwendet werden soll
            auswahl = ''
            while auswahl != 'j' and auswahl != 'n':
                auswahl = input('Möchten Sie eine Maus verwenden?(j/n): ')

            if auswahl == 'j':
                devices = [InputDevice(fn) for fn in list_devices()]
                i = 0
                print("Wähle die Maus aus der Liste")
                for dev in devices:
                	print(i, dev.name)
                	i += 1

                dev_id = int(input('Gerätenummer: '))

                with open(path + '/if_mouse.py','w') as f:
                	f.write(devices[dev_id].name)
                	f.close()

            if auswahl == 'n':
                with open(path + '/if_mouses.py','w') as f:
                	f.write(auswahl)
                	f.close()

        # Cardreader konfigurieren
        with open(path + '/if_mouse.py','r') as f:
            deviceName = f.read()
            if not deviceName == 'n':
                devices = [InputDevice(fn) for fn in list_devices()]

                for device in devices:
                    if device.name == deviceName:
                        global if_mouse
                        if_mouse = device
                        break
                try:
                    if_mouse
                except:
                    logger.error('Kann das Gerät nicht finden %s\n. Bitte sicherstellen, dass es verbunden ist' % deviceName)
                    sys.exit()


    def check_mouse(self):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/if_mouse.py','r') as f:
            deviceName = f.read()
        return deviceName


    def mouse_press(x, y):
        while True:
            r, w, x = select([dev], [], [])
            for event in dev.read():
                if event.code == 8:
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
                    os.system("sudo shutdown -h now")
                    logger.info('fahren auf Anforderung herunter')
                elif event.code == 275 and event.value == 1:
                    logger.debug('links aussen gedrueckt')
                    linksAussen()
                elif event.code == 276 and event.value == 1:
                    logger.debug('rechts aussen gedrueckt')
                    rechtsAussen()
