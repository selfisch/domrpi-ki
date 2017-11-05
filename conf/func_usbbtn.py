from evdev import InputDevice, ecodes, list_devices
from select import select
import os, sys, logging, csv, time, threading, time, settings
import RPi.GPIO as GPIO

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

global TunerPin
TunerPin = 36
global AuxPin
AuxPin = 38
global CDPin
CDPin = 40
global TapePin
TapePin = 33
global Test1
Test1 = 35
global Test2
Test2 = 37

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location

GPIO.setup(TunerPin, GPIO.OUT)   # Set LedPin's mode is output
GPIO.output(TunerPin, GPIO.HIGH)  # Set LedPin to low(0V)

GPIO.setup(AuxPin, GPIO.OUT)   # Set LedPin's mode is output
GPIO.output(AuxPin, GPIO.HIGH)  # Set LedPin to low(0V)

GPIO.setup(CDPin, GPIO.OUT)   # Set LedPin's mode is output
GPIO.output(CDPin, GPIO.HIGH)  # Set LedPin to low(0V)

GPIO.setup(TapePin, GPIO.OUT)   # Set LedPin's mode is output
GPIO.output(TapePin, GPIO.LOW)  # Set LedPin to low(0V)

GPIO.setup(Test1, GPIO.OUT)   # Set LedPin's mode is output
GPIO.output(Test1, GPIO.LOW)  # Set LedPin to low(0V)

GPIO.setup(Test2, GPIO.OUT)   # Set LedPin's mode is output
GPIO.output(Test2, GPIO.LOW)  # Set LedPin to low(0V)


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

    ## Ende __init__

    def source_led():
        logger.debug("source: " + settings.source)
        if settings.source == 'Tuner':
            GPIO.output(TunerPin, GPIO.LOW) # led on
            GPIO.output(AuxPin, GPIO.HIGH)  # led off
        elif settings.source == 'Aux':
            GPIO.output(TunerPin, GPIO.HIGH) # led on
            GPIO.output(AuxPin, GPIO.LOW)  # led off


    def destroy_led_blink():
        logger.debug('led destroyed')
        GPIO.output(TunerPin, GPIO.HIGH)    # turn off all leds
        GPIO.output(AuxPin, GPIO.HIGH)    # turn off all leds
        GPIO.cleanup()


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
            #usbbtn.source('tuner')
            logger.debug('Tuner')
            settings.source = 'Tuner'
            usbbtn.source_led()
        elif val == 589834:
            #usbbtn.source('aux')
            logger.debug('Aux')
            settings.source = 'Aux'
            usbbtn.source_led()
        elif val == 589836:
            #usbbtn.source('cd')
            logger.debug('cd')
        elif val == 589833:
            logger.debug('tape')


    def button_press(self):
        try:
            logger.debug('starte USB Buttons')
            usbbtn.source_led()
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
            usbbtn.destroy_led_blink()
        except (KeyboardInterrupt):
            logger.info("via Tastatur beendet")
            usbbtn.destroy_led_blink()
            exit()
        except Exception as e:
            logger.error("main crashed {0}".format(str(e)))
            logger.exception("Error")
            destroy_led_blink()
            raise
        except:
            logger.info("Unbekannter Fehler:", sys.exc_info()[0])
            destroy_led_blink()
            raise
        pass
