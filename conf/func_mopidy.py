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
        client.add(uri)
        if play_mode == 'play':
            client.random(0)
            client.play()
        elif play_mode == 'shuffle':
            client.random(1)
            client.play()
        mopidy.mpdDisconnect()


    def playList(uri, play_mode):
        logger.debug('mopidy.playList uri: ' + uri)
        logger.debug('mopidy.playList play_mode: ' + play_mode)
        mopidy.mpdConnect()
        client.clear()
        client.add(uri)
        if play_mode == 'play':
            client.random(0)
            client.play()
        elif play_mode == 'shuffle':
            client.random(1)
            client.play()
        mopidy.mpdDisconnect()


    def play():
        mopidy.mpdConnect()
        logger.debug('mpd status: ' + str(mpd_status))
        state = client.status()['state'].split(":")
        if 'play' in state:
            client.pause()
        elif 'pause' in state:
            client.play()
        mopidy.mpdDisconnect()


    def stop():
        state = client.status()['state'].split(":")
        if 'play' in state:
            mopidy.mpdConnect()
            client.stop()
            mopidy.mpdDisconnect()


    def next():
        state = client.status()['state'].split(":")
        if 'play' in state:
            mopidy.mpdConnect()
            client.next()
            mopidy.mpdDisconnect()


    def previous():
        state = client.status()['state'].split(":")
        if 'play' in state:
            mopidy.mpdConnect()
            client.previous()
            mopidy.mpdDisconnect()


    def repeat():
        state = client.status()['random'].split(":")
        if 0 in random:
            mopidy.mpdConnect()
            client.random(1)
        elif 1 in random:
            client.random(0)
