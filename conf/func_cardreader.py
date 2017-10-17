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


    def play_card(plist_id):
        logger.debug('play_card wurde mit folgender plist_id aufgerufen: ' + plist_id)
        while True:
            uri = ''
            play_mode = ''
            card = plist_id
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
                else:
                    logger.info('Card ' + plist_id + ' scheint noch nicht mit einer Playlist verknüpft.')


    def read_card(self, threadName, bool):
        logger.debug('starte read_card')
        while True:
            stri = ''
            key = ''
            logger.debug('erste read_card while Schleife')
            while key != 'KEY_ENTER':
                logger.debug('zweite read_card while Schleife')
                r, w, x = select([if_cardreader], [], [])
                for event in if_cardreader.read():
                    if event.type == 1 and event.value == 1:
                        stri += keys[event.code]
                        key = ecodes.KEY[event.code]
#                        logger.debug(stri)
#                        stri = stri[:-1]
#                        logger.debug(stri)
            stri = stri[:-1]
            logger.debug(stri)
            if stri != '':
                logger.debug('read_card hat folgende plist_id empfangen: stri')
                mouse.play_card(stri)
#        return stri[:-1]
