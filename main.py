#!/usr/bin/python3

import csv, os, sys, _thread
import logging
from random import randint
from mpd import MPDClient
from select import select

# conf Unterverzeichnis mit durchsuchen
sys.path.append('./conf')

from func_cardreader import cardreader
#from func_usbbtn import usbbtn
from func_mousebtn import mouse

# in das Verzeichnis des Skript wechseln
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# lege das conf Verzeichnis an, falls es nicht existiert
if not os.path.exists('conf'):
    os.mkdir('conf')

if not os.path.exists('log'):
    os.mkdir('log')

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


logger.info('Starte main __init__')
path = os.path.dirname(os.path.realpath(__file__))

# lade die Class cardreader in die Variable cardreader
cardreader = cardreader()
check_reader = cardreader.check_reader()

mouse = mouse()
check_mouse = mouse.check_mouse()


def mpdConnect():
    client.connect("localhost", 6600)


def mpdDisconnect():
    client.disconnect()


def play_card(x, y):
    logger.info('starte play_card')
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


#if __name__ == "__main__":
#while True:
    try:
        logger.info('Starte die Anwendung')
        if not check_reader == 'n':
            _thread.start_new_thread(play_card(play_card, True))
#        _thread.start_new_thread(buttons(thread_x, True))
#        _thread.start_new_thread(button_press(thread_x, True))
    except (SystemExit):
        logger.info("Anwendung beendet")
        exit()
    except (KeyboardInterrupt):
        logger.info("via Tastatur beendet")
        exit()
    except Exception as e:
        logger.error("main crashed {0}".format(str(e)))
        logger.exception("Error")
        raise
    except:
        logger.info("Unbekannter Fehler:", sys.exc_info()[0])
        raise
#    else:
#        pass
