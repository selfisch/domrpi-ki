from evdev import InputDevice, ecodes, list_devices
from select import select
import os.path

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
