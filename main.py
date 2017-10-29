#!/usr/bin/python3

import os, sys, _thread, threading, time
import RPi.GPIO as GPIO
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

global LedPin
LedPin = 12

# lege das conf Verzeichnis an, falls es nicht existiert
if not os.path.exists('conf'):
    os.mkdir('conf')

path = os.path.dirname(os.path.realpath(__file__))

def gpio_setup():
    global p
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.output(LedPin, GPIO.LOW)  # Set LedPin to low(0V)

    p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
    p.start(0)                     # Duty Cycle = 0


def loop():
    while True:
        for dc in range(0, 101, 4):   # Increase duty cycle: 0~100
            p.ChangeDutyCycle(dc)     # Change duty cycle
            time.sleep(0.05)
        time.sleep(1)
        for dc in range(100, -1, -4): # Decrease duty cycle: 100~0
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
        time.sleep(1)


def destroy():
    p.stop()
    GPIO.output(LedPin, GPIO.HIGH)    # turn off all leds
    GPIO.cleanup()


try:
    logger.info('Starte die Anwendung')
    gpio_setup()
    loop()

    if check_usbbtn != 'n':
        button_press_thread.start()
    if check_reader != 'n':
        read_card_thread.start()
    if check_mouse != 'n':
        mouse_press_thread.start()

except (SystemExit):
    logger.info("Anwendung beendet")
    destroy()
    exit()
except (KeyboardInterrupt):
    logger.info("via Tastatur beendet")
    destroy()
    exit()
except Exception as e:
    logger.error("main crashed {0}".format(str(e)))
    logger.exception("Error")
    destroy()
    raise
except:
    logger.info("Unbekannter Fehler:", sys.exc_info()[0])
    destroy()
    raise
#    else:
#        pass
