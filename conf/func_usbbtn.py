from evdev import InputDevice, ecodes, list_devices
from select import select
import os, sys, logging, csv, time, threading

logger = logging.getLogger('main')

from func_mopidy import mopidy

# lade die Class cardreader in die Variable cardreader
from func_cardreader import cardreader
cardreader = cardreader()
check_reader = cardreader.check_reader()

# lade die Class mouse in die Variable mouse
from func_mousebtn import mouse
mouse = mouse()
check_mouse = mouse.check_mouse()

mpd_connect_thread = threading.Thread(name='mpd_connect_thread', target=mopidy.mpdConnect)
read_card_thread = threading.Thread(name='read_card', target=cardreader.read_card)
mouse_press_thread = threading.Thread(name='mouse_press', target=mouse.mouse_press)

class usbbtn:
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        # prüfe die Buttons und richte sie ein
        if not os.path.isfile(path + '/if_usbbtn.py'):
            auswahl = ''
            while auswahl != 'j' and auswahl != 'n':
                auswahl = input('Möchten Sie ein Button Interface verwenden?(j/n): ')

            if auswahl == 'j' or auswahl == 'J':
                devices = [InputDevice(fn) for fn in list_devices()]
                i = 0
                print("Wähle das Button Interface aus")
                for dev in devices:
                	print(i, dev.name)
                	i += 1

                dev_id = int(input('Gerätenummer: '))

                with open(path + '/if_usbbtn.py','w') as f:
                	f.write(devices[dev_id].name)
                	f.close()

            if auswahl == 'n':
                with open(path + '/if_usbbtn.py','w') as f:
                	f.write(auswahl)
                	f.close()

        # USB Buttons konfigurieren
        with open(path + '/if_usbbtn.py','r') as f:
            deviceName = f.read()
            if not deviceName =='n':
                devices = [InputDevice(fn) for fn in list_devices()]

                for device in devices:
                    if device.name == deviceName:
                        global if_usbbtn
                        if_usbbtn = device
                        break
                try:
                    if_usbbtn
                except:
                    logger.error('Kann das Gerät nicht finden:')
                    logger.error(deviceName)
                    logger.error('Bitte sicherstellen, dass es verbunden ist')
                    sys.exit()


    def check_usbbtn(self):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/if_usbbtn.py','r') as f:
            deviceName = f.read()
        return deviceName


    def buttons(val):
        if val == 589827:
            print('vol up')
            os.system("amixer -q sset Master 1%+")
        elif val == 589825:
            print('vol down')
            os.system("amixer -q sset Master 1%-")
        elif val == 589826:
            print('next track')
            mopidy.next()
        elif val == 589829:
            print('prev track')
            mopidy.previous()
        elif val == 589831:
            print('play/pause')
            mopidy.play()
        elif val == 589830:
            print('stop')
            mopidy.stop()
        elif val == 589835:
            usbbtn.source('tuner')
        elif val == 589834:
            usbbtn.source('aux')
        elif val == 589836:
            usbbtn.source('cd')
        elif val == 589833:
            usbbtn.source('tape')


    def source(source):
        if source == 'tuner':
            logger.debug('tuner')
            if check_reader != 'n' and not read_card_thread.is_alive():
                read_card_thread.start()
            if check_mouse != 'n' and not mouse_press_thread.is_alive():
                mouse_press_thread.start()

        if source == 'aux':
            if read_card_thread.is_alive():
                read_card_thread.stop()
            logger.debug('aux')
        if source == 'cd':
            logger.debug('cd')
        if source == 'tape':
            logger.debug('tape')


    def button_press(self):
        try:
            logger.debug('starte USB Buttons')
            global time_stamp
            time_stamp = time.time()
            while True:
                r, w, x = select([if_usbbtn], [], [])
                for event in if_usbbtn.read():
                    if event.code == 4:
                        time_now = time.time()
                        if (time_now - time_stamp) >= 0.5:
                            logger.debug('Button wurde gedrückt.')
                            logger.info(event)
                            usbbtn.buttons(event.value)
                        time_stamp = time_now
        except Exception as e:
            logger.error("main crashed {0}".format(str(e)))
            logger.exception("Error")
            raise
        except:
            logger.info("Unbekannter Fehler:", sys.exc_info()[0])
            raise
        pass
