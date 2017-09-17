#!/usr/bin/python3

# Requirements apt: sudo apt-get install -y mopidy git python3 python3-dev python3-pip
# Requirements pip: sudo pip3 install evdev python-mpd2 evdev Mopidy-Iris
# git clone git@github.com:selfisch/domrpi-ki.git

import csv, os, sys, _thread
import logging
from evdev import InputDevice, ecodes, list_devices
from select import select
from random import randint
from mpd import MPDClient

# in das Verzeichnis des Skript wechseln
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# lege das conf Verzeichnis an, falls es nicht existiert
if not os.path.exists('conf'):
    os.mkdir('conf')

if not os.path.exists('/log'):
    os.mkdir('/conf')


sys.path.append('./conf')

# MPDClient config
client = MPDClient()    # create client object
client.timeout = 10     # network timeout in seconds (floats allowed), default: None
client.idletimeout = None

# logger konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.FileHandler('log/aiwa.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
thread_x = ''


def init():
    path = os.path.dirname(os.path.realpath(__file__))
    # lege das conf Verzeichnis an, falls es nicht existiert
    if not os.path.exists(path + '/conf'):
        os.mkdir(path + '/conf')

    if not os.path.exists(path + '/log'):
        os.mkdir(path + '/conf')

    # prüfe Reader und richte ihn ein
    if not os.path.isfile(path + '/conf/reader.py'):
        devices = [InputDevice(fn) for fn in list_devices()]
        i = 0
        print("Choose the reader from list")
        for dev in devices:
        	print(i, dev.name)
        	i += 1

        dev_id = int(input('Device Number: '))

        with open(path + '/conf/reader.py','w') as f:
        	f.write(devices[dev_id].name)
        	f.close()
    else:
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

    # prüfe die Buttons und richte sie ein
    if not os.path.isfile(path + '/conf/buttons.py'):
        devices = [InputDevice(fn) for fn in list_devices()]
        i = 0
        print("Choose button input from list")
        for dev in devices:
        	print(i, dev.name)
        	i += 1

        dev_id = int(input('Device Number: '))

        with open(path + '/conf/buttons.py','w') as f:
        	f.write(devices[dev_id].name)
        	f.close()
    else:
        # Maus konfigurieren
        with open(path + '/conf/buttons.py','r') as f:
            deviceName = f.read()
        devices = [InputDevice(fn) for fn in list_devices()]
        for device in devices:
            if device.name == deviceName:
                global buttons
                buttons = device
                break
        try:
            buttons
        except:
            logger.error('Could not find the device %s\n. Make sure is connected' % deviceName)
            sys.exit()


def mpdConnect():
    client.connect("localhost", 6600)


def mpdDisconnect():
    client.disconnect()


def button_press(x, y):
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


def button():
    while True:
        r, w, x = select([buttons], [], [])
        for button in buttons.read():
            print(button)


def read_card():
    logger.debug('starte read_card')
    stri = ''
    key = ''
    while key != 'KEY_ENTER':
        r, w, x = select([reader], [], [])
        for event in reader.read():
            if event.type == 1 and event.value == 1:
                stri += keys[event.code]
#                print( keys[ event.code ] )
                key = ecodes.KEY[event.code]
    return stri[:-1]
    logger.debug('beende read_card')


def play_card(x, y):
    while True:
        uri = ''
        logger.debug('starte play_card')
        card = read_card()
        rows = csv.reader(open("plist.csv", "r"), delimiter=';')
        plist = []
        plist.extend(rows)
        #print(plist)
        for row in plist:
            if row[3] == card:
                uri = row[1]

        #if not



#if __name__ == "__main__":
while True:
    try:
        logger.info('Starte die Anwendung')
        init()
        _thread.start_new_thread(play_card(thread_x, True))
        _thread.start_new_thread(button_press(thread_x, True))
    except (SystemExit):
        logger.info("Anwendung beendet")
        exit()
    except (KeyboardInterrupt):
        logger.info("via Tastatur beendet")
        exit()
#       except mpd, m:
#       logger.debug("mpd meldet {0}",format(str(m)))
#       logger.info("mpd meldet {0}",format(str(m)))
    except Exception as e:
        logger.error("main crashed {0}".format(str(e)))
        logger.exception("Error")
        mpdDisconnect()
    except:
        logger.info("Unbekannter Fehler:", sys.exc_info()[0])
        raise
    else:
        pass
