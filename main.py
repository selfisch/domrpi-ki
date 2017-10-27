#!/usr/bin/python3

import os, sys, _thread, threading
#from random import randint
#from mpd import MPDClient
#from select import select

# conf Unterverzeichnis mit durchsuchen
sys.path.append('./conf')

import log
logger = log.setup_custom_logger('main')

from func_cardreader import cardreader
from func_usbbtn import usbbtn
from func_mopidy import mopidy
from func_mousebtn import mouse

# lade die Class mopidy in die Variable mopidy
#mopidy = mopidy()
# lade die Class usbbtn in die Variable usbbtn
usbbtn = usbbtn()
check_usbbtn = usbbtn.check_usbbtn()
cardreader = cardreader()
check_reader = cardreader.check_reader()
mouse = mouse()
check_mouse = mouse.check_mouse()

# Threads definieren
mpd_connect_thread = threading.Thread(name='mpd_connect_thread', target=mopidy.mpdConnect)
read_card_thread = threading.Thread(name='read_card', target=cardreader.read_card)
mouse_press_thread = threading.Thread(name='mouse_press', target=mouse.mouse_press)
button_press_thread = threading.Thread(name='button_press', target=usbbtn.button_press)

# in das Verzeichnis des Skript wechseln
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# lege das conf Verzeichnis an, falls es nicht existiert
if not os.path.exists('conf'):
    os.mkdir('conf')

path = os.path.dirname(os.path.realpath(__file__))

try:
    logger.info('Starte die Anwendung')

    if check_usbbtn != 'n':
        button_press_thread.start()
    if check_reader != 'n':
        read_card_thread.start()
    if check_mouse != 'n':
        mouse_press_thread.start()

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
