import csv, os, logging, time
from random import randint
from mpd import MPDClient
#from persistMPDclient import PersistentMPDClient

logger = logging.getLogger('main')


#persistMPDclient = PersistentMPDClient()

class mopidy:
    global client
    client = MPDClient()    # create client object


    def mpdConnect():
        # MPDClient config
        client.timeout = 10
        client.idletimeout = None
        client.connect("localhost", 6600)


    def mpdDisconnect():
        client.close()
        client.disconnect()


    def randomPlaylist():
        mopidy.mpdConnect()
        uris = csv.reader(open("plist.csv", "r"),delimiter=';')
        plist = []
        plist.extend(uris)

        plist_zahl = randint(0, len(plist))
        if plist_zahl >= 1:
            plist_zahl = plist_zahl - 1
        uri = str(plist[plist_zahl][1])
        play_mode = str(plist[plist_zahl][2])
        uri = uri.replace('[','')
        uri = uri.replace(']','')
        uri = uri.replace('\'','')
        logger.debug("URI to pass: " + uri)
        logger.debug("Playmode: " + play_mode)
        client.clear()

        if "spotify" in uri:
            #logger.debug('found spotify in uri')
            client.add(uri)
        else:
            #logger.debug('does not find spotify in uri')
            client.load(uri)

        if play_mode == 'play':
            client.random(0)
            client.play()
        elif play_mode == 'shuffle':
            client.random(1)
            client.play()
        mopidy.mpdDisconnect()


    def play_list(uri, play_mode):
        logger.debug('play_list')
        logger.debug('mopidy.play_list uri: ' + uri)
        logger.debug('mopidy.play_list play_mode: ' + play_mode)
        mopidy.mpdConnect()
        uris = csv.reader(open("plist.csv", "r"),delimiter=';')
        plist = []
        plist.extend(uris)

        client.clear()

        if "spotify" in uri:
            #logger.debug('found spotify in uri')
            client.add(uri)
        else:
            #logger.debug('does not find spotify in uri')
            client.load(uri)

        if play_mode == 'play':
            client.random(0)
            client.play()
        elif play_mode == 'shuffle':
            client.random(1)
            client.play()
        mopidy.mpdDisconnect()


    def play():
        mopidy.mpdConnect()
        state = client.status()['state'].split(":")
        if 'play' in state:
            client.pause()
        elif 'pause' in state:
            client.play()
        mopidy.mpdDisconnect()


    def stop():
        mopidy.mpdConnect()
        state = client.status()['state'].split(":")
        if 'play' in state:
            client.stop()
        mopidy.mpdDisconnect()


    def next():
        mopidy.mpdConnect()
        state = client.status()['state'].split(":")
        if 'play' in state:
            client.next()
        mopidy.mpdDisconnect()


    def previous():
        mopidy.mpdConnect()
        state = client.status()['state'].split(":")
        if 'play' in state:
            client.previous()
        mopidy.mpdDisconnect()


    def repeat():
        mopidy.mpdConnect()
        state = client.status()['repeat'].split(":")
        logger.debug(state)
        if '0' in state:
            client.repeat(1)
            logger.debug('repeat an')
        elif '1' in state:
            client.repeat(0)
            logger.debug('repeat aus')
        mopidy.mpdDisconnect()
