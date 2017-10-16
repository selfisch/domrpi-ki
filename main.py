#!/usr/bin/python3

import csv, os, sys, _thread
from random import randint
from mpd import MPDClient
from select import select

# conf Unterverzeichnis mit durchsuchen
sys.path.append('./conf')

import log
logger = log.setup_custom_logger('main')

from func_mopidy import mopidy
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

keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"

path = os.path.dirname(os.path.realpath(__file__))

# lade die Class cardreader in die Variable cardreader
cardreader = cardreader()
check_reader = cardreader.check_reader()

# lade die Class mouse in die Variable mouse
mouse = mouse()
check_mouse = mouse.check_mouse()

try:
    logger.info('Starte die Anwendung')
    if not check_reader == 'n':
        _thread.start_new_thread(cardreader.read_card('read_card', True, ) )
    if not check_mouse == 'n':
        _thread.start_new_thread(mouse.mouse_press('mouse_press', True, ) )
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
