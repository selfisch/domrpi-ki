from evdev import InputDevice, ecodes, list_devices
from select import select
import os.path, sys, logging, csv

logger = logging.getLogger('main')


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
                with open(path + '/if_mouse.py','w') as f:
                	f.write(auswahl)
                	f.close()

        # Maus konfigurieren
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
                    logger.error('Kann das Gerät nicht finden:')
                    logger.error(deviceName)
                    logger.error('Bitte sicherstellen, dass es verbunden ist')
                    sys.exit()


    def check_mouse(self):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/if_mouse.py','r') as f:
            deviceName = f.read()
        return deviceName


    def mouse_press(self, theadName, bool):
        #logger.info('Starte mouse_press')
        while True:
            r, w, x = select([if_mouse], [], [])
            for event in if_mouse.read():
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

    # linke Aussentaste an der Maus startet eine random Playliste
    def linksAussen(self):
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

    def linkeMaustaste(self):
      mpdConnect()
      state = client.status()['state'].split(":")
      if 'play' in state:
        client.pause()
      elif 'pause' in state:
        client.play()
      mpdDisconnect()

    def rechteMaustaste(self):
      mpdConnect()
      state = client.status()['state'].split(":")
      if 'play' in state:
        client.stop()
      else:
        client.stop()
      mpdDisconnect()

    def rechtsAussen(self):
      mpdConnect()
      client.stop()
      client.clear()
      client.add('http://ndr-ndr2-niedersachsen.cast.addradio.de/ndr/ndr2/niedersachsen/mp3/128/stream.mp3')
      client.play()
      mpdDisconnect()
