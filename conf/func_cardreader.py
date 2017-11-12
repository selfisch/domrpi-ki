from evdev import InputDevice, ecodes, list_devices
from select import select
import os.path, sys, logging, csv, random
from func_mopidy import mopidy

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


    def check_card(card):
        logger.debug('check_card')
        rows = csv.reader(open("plist.csv", "r"), delimiter=';')
        uri = ''
        plist = []
        plist.extend(rows)
        artist_uri_list = []
        for row in plist:
            if row[3] == card:
                uri = row[1]
                play_mode = row[2]
            elif row[4] == card:
                artist_uri_list.append(row[1])
                play_mode = 'play'

        if len(artist_uri_list) >= 1 and uri == '':
            mopidy.play_list(uri, play_mode)

        elif uri != '':
            mopidy.play_list(uri, play_mode)


    def read_card(self):
        logger.debug('starte read_card')
        while True:
            stri = ''
            key = ''
            while key != 'KEY_ENTER':
                r, w, x = select([if_cardreader], [], [])
                for event in if_cardreader.read():
                    if event.type == 1 and event.value == 1:
                        stri += keys[event.code]
                        key = ecodes.KEY[event.code]
            stri = stri[:-1]
            if stri != '':
                logger.debug('read_card hat folgende plist_id erzeugt: ' + stri)
                cardreader.check_card(stri)
