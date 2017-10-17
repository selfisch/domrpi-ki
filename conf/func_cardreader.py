from evdev import InputDevice, ecodes, list_devices
from select import select
import os.path, sys, logging

logger = logging.getLogger('main')
keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"

class cardreader:
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))

        # prüfe Reader und richte ihn ein
        if not os.path.isfile(path + '/if_cardreader.py'):
            # Frage, ob ein Kartenleser verwendet werden soll
            auswahl = ''
            while auswahl != 'j' and auswahl != 'n':
                auswahl = input('Möchten Sie einen Kartenleser verwenden?(j/n): ')

            if auswahl == 'j':
                devices = [InputDevice(fn) for fn in list_devices()]
                i = 0
                print("Wähle den Kartenleser aus der Liste")
                for dev in devices:
                	print(i, dev.name)
                	i += 1

                dev_id = int(input('Gerätenummer: '))

                with open(path + '/if_cardreader.py','w') as f:
                	f.write(devices[dev_id].name)
                	f.close()

            if auswahl == 'n':
                with open(path + '/if_cardreader.py','w') as f:
                	f.write(auswahl)
                	f.close()

        # Cardreader konfigurieren
        with open(path + '/if_cardreader.py','r') as f:
            deviceName = f.read()
            if not deviceName == 'n':
                devices = [InputDevice(fn) for fn in list_devices()]

                for device in devices:
                    if device.name == deviceName:
                        global if_cardreader
                        if_cardreader = device
                        break
                try:
                    if_cardreader
                except:
                    logger.error('Kann das Gerät nicht finden %s\n. Bitte sicherstellen, dass es verbunden ist' % deviceName)
                    sys.exit()


    def check_reader(self):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/if_cardreader.py','r') as f:
            deviceName = f.read()
        return deviceName


    def read_card(self, threadName, bool):
        logger.info('starte read_card')
        stri = ''
        key = ''
        while key != 'KEY_ENTER':
            r, w, x = select([if_cardreader], [], [])
            for event in if_cardreader.read():
                if event.type == 1 and event.value == 1:
                    stri += keys[event.code]
    #                print( keys[ event.code ] )
                    key = ecodes.KEY[event.code]
        return stri[:-1]


    def play_card(x, y):
        #logger.info('starte play_card')
        while True:
            uri = ''
            play_mode = ''
            card = cardreader.read_card()
            rows = csv.reader(open("plist.csv", "r"), delimiter=';')
            plist = []
            plist.extend(rows)
            #print(plist)
            for row in plist:
                if row[3] == card:
                    uri = row[1]
                    play_mode = row[2]
                    logger.debug("URI to pass: " + uri)
                    logger.debug("Playmode: " + play_mode)
                    mpdConnect()
                    client.clear()
                    client.add(uri)
                    if play_mode == 'play':
                        client.random(0)
                        client.play()
                    elif play_mode == 'shuffle':
                        client.random(1)
                        client.play()
                    mpdDisconnect()
