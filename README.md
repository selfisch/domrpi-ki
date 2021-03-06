<img src='/pic/1.jpg' alt='aktueller Stand'>
<img src='/pic/2.jpg' alt='aktueller Stand'>
<img src='/pic/3.jpg' alt='aktueller Stand'>

# RPi Media Player Projekt
## if someone is interested in an english version, please let me know

Hi,
ich hatte zuhause noch eine alte Aiwa Kompaktanlage stehen, welche ich aber aufgrund der
Boxen zu schade zum entsorgen fand. Kurz um, das Innere entleert und einen Raspberry Pi2
eingebaut. Und so hat das Projekt begonnen.
Jetzt mag sich der ein oder andere frage, wieso kauft der sich nicht eine fertige Kompaktanlage
mit WLAN und Spotify Anbindung beim einem Elektronik Fachmarkt?
Ganz einfach. Auch wenn es viel Arbeit und womöglich Pflegeaufwand im Nachhinein bedeutet,
setze ich solche Sachen gerne selber um, um genau zu wissen was drin ist und was ich eventuell
noch machen kann. Außerdem wollte ich gerne eine NFC Lösung mit verbauen, da die Anlage für das Kinderzimmer gedacht ist und die Kinder eine CD Hülle mit NFC Aufkleber bekommen und diese nur über die Anlage halten brauchen um das Hörspiel oder die Musik ihrer Wahl zu hören.
Einfacher als jeder Touchscreen und ich kann den RPi noch mit vielen anderen Sachen ausrüsten und womöglich noch mit in meine SmartHome Lösung integrieren.

Hardware:
- Aiwa Kompaktanlage(komplett entleert)
- raspberry Pi 3
- Hifiberry Amp
- Microsoft 5 Button USB Maus
- Buttons - https://www.amazon.de/gp/product/B01IQTN1NO/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1
- NFC Reader - https://www.amazon.de/gp/product/B01LY6NVHN/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1

Software:
- RaspBian Jessie(Stretch hatte noch Probleme mit ein paar python und spotify libs)
- Mopidy
- Mopidy-Spotify
- Mopidy Iris Webextension

### Update: initial
Skript läuft soweit.
Aktuell habe ich mich für die Steuerung über eine 5 Button Maus entschieden, um überhaupt etwas machen zu können.
Grundsätzlich hat die Anlage auf der Front an die 20 Knöpfe, die ich jedoch nicht via GPIO ansteuern kann, da ich auch noch diverse LEDs ansteuern muss.
Alternativ habe ich somit momentan die Überlegung, die Button über eine USB Lösung anzusteuern/auszulesen.
Falls jemand etwas derartiges schon gemacht hat, ich bin für Vorschläge offen :-).

### Update 17.03.18
- da wir inzwischen ein paar CDs haben, die bei Spotify nicht verfügbar sind, musste ich mir eine Möglichkeit mit lokalen Playlisten einfallen lassen. Kurzerhand, CDs gerippt und auf einem Netzwerkshare hinterlegt. M3U8 Playlisten erstellt und diese in Mopidy hinterlegt und siehe da, wenn man erstmal verstanden hat wie es funktioniert, ist es eine Kleinigkeit.
Der Code musste etwas angepasst werden, da die URIs für M3U Listen etwas anders aussehen.
Wer Fragen zu dem Konstrukt in Verbindung mit Mopidy hat, kann sich gern an mich wenden.

### Update: 18.08.17
- die Spotify Playlisten funktionieren endlich, es funktionieren aber nur persönliche Playlisten, öffentliche Spotify Playlisten lassen sich nicht hinzufügen

### Update: 07.09.17
- eine Lösung für die Buttons wurde gefunden und angebunden(siehe Hardwareliste)
- ein NFC Reader wurde ebenfalls bestellt und angebunden(siehe Hardwareliste)

### Update: 12.10.17
- der alte RPi2 wird durch einen neuen RPi3 ersetzt. Dieser ist bereits im Testeinsatz. Außerdem wurde ein Buttoninterface und ein Kartenleser angebunden, für die nächste Ausbaustufe.
Eigentlich hätte ich die LEDs für die Knöpfe auf der Front auch gerne noch eingebaut bevor das ganze aufgestellt wird, das würde aber eine Inbetriebnahme enorm in Zeitverzug bringen, da ich aktuell keine Zeit für die Lötarbeiten an der Platine habe.

### Update: 18.10.17
- es läuft, im jetzigen Stand gibt es ein Instal Skript währenddessen man auswählen kann, welche Eingabemethode man nutzen möchte. Da ich in Zukunft nur USB-Buttons und Cardreader nutzen möchte, wird die Mausalternative nicht weiter gepflegt.
Was noch fehlt ist der Test und Einsatz mit dem Hifiberry, da ich hier bisher nur einen besitze und dieser im Einsatz bei der aktuellen Lösung ist. Da der Go-Live aber kurz bevor steht, wird das der nächste Schritt.
Danach mache ich mir noch ein paar Gedanken zu
  - Random Playlisten
  - andere Funktionen wie z.B. auf einen Spotify Reveiver via "Source Buttons" an der Aiwa Anlage umschalten
  - und mal schauen, was mir noch so in den Sinn kommt :-)

## Installation
Die Installation gestaltet sich(hoffentlich für jeden) relativ einfach.
1. das Repository an einen Ort der Wahle clonen
2. soll Spotify mit Mopidy genutzt werden, bitte conf/spotify.template beachten
3. plist.template beachten und entsprechend anlegen
4. setup.sh ausführen ACHTUNG: hier werden diverse Pakete installiert und deinstalliert, man sollte dies also nicht achtlos auf seinem Desktop Linux Rechner machen, da man sich einiges kaputt machen könnte, am besten einen Raspberry Pi verwenden
5. main.py ausführen

Möchte man die Python Applikation beim Systemstart automatisch anschmeißen, so muss dies noch konfiguriert werden.
Zu gegebener Zeit kann ich diese hier gerne mit dokumentieren.


ToDo:
- logrotate muss eingebaut werden
- Skript läuft nach der Installation:
  - es wird noch eine Abfrage während der Installation benötigt, ob ein Reader oder Buttons vorhanden sind
- Wiedergabefunktionen via Source Buttons auswählen(umschalten zwischen Mopidy und Spotify Receiver)
- Stromverbrauch messen
- geeignetes Display suchen
- Lötarbeiten LEDs anzubinden
- Skript weiter ausfeilen um auf die LEDs entsprechend anzusteuern
- nach einer Möglichkeit suchen die Beleuchtung via Proximity zu steuern
- ...
