# linke Aussentaste an der Maus startet eine random Playliste
def linksAussen():
	mpdConnect()
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
	mpdDisconnect()

def linkeMaustaste():
  mpdConnect()
  state = client.status()['state'].split(":")
  if 'play' in state:
    client.pause()
  elif 'pause' in state:
    client.play()
  mpdDisconnect()

def rechteMaustaste():
  mpdConnect()
  state = client.status()['state'].split(":")
  if 'play' in state:
    client.stop()
  else:
    client.stop()
  mpdDisconnect()

def rechtsAussen():
  mpdConnect()
  client.stop()
  client.clear()
  client.add('http://ndr-ndr2-niedersachsen.cast.addradio.de/ndr/ndr2/niedersachsen/mp3/128/stream.mp3')
  client.play()
  mpdDisconnect()
