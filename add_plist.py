#from readtest import *
from pList import pList
pList = pList()

while True:
    plist_id=raw_input('Specfiy Playlist ID: ')
    plist_uri=raw_input('Specify Spotify URI, q to quit: ')
    if plist=="q":
        break
	pList.addPlaylist(plist_id, plist_uri)
print "Exiting"
