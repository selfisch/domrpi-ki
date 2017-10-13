<img src='/pic/1.jpg' alt='aktueller Stand'>
<img src='/pic/2.jpg' alt='aktueller Stand'>
<img src='/pic/3.jpg' alt='aktueller Stand'>

# RPi Media Player Projekt
Projekt Aiwa Kompaktanlage

Hardware:
- Aiwa Kompaktanlage(komplett ausgeschlachtet)
- raspberry Pi 2 B+
- Hifiberry Amp
- Edimax WLAN USB Dongle
- Microsoft 5 Button USB Maus

Software:
- RaspBian Lite
- Mopidy
- Mopidy-Spotify
- Mopidy Iris Webextension

### Update: initial
Skript läuft soweit.
Aktuell habe ich mich für die Steuerung über eine 5 Button Maus entschieden, um überhaupt etwas machen zu können.
Grundsätzlich hat die Anlage auf der Front an die 20 Knöpfe, die ich jedoch nicht via GPIO ansteuern kann, da ich auch noch diverse LEDs ansteuern muss.
Alternativ habe ich somit momentan die Überlegung, die Button über eine USB Lösung anzusteuern/auszulesen.
Falls jemand etwas derartiges schon gemacht hat, ich bin für Vorschläge offen :-).

### Update: 18.08.17
- die Spotify Playlisten funktionieren endlich, es funktionieren aber nur persönliche Playlisten, öffentliche Spotify Playlisten lassen sich nicht hinzufügen

### Update: 12.10.17
- der alte RPi2 wird durch einen neuen RPi3 ersetzt. Dieser ist bereits im Testeinsatz. Außerdem wurde ein Buttoninterface und ein Kartenleser angebunden, für die nächste Ausbaustufe.
Eigentlich hätte ich die LEDs für die Knöpfe auf der Front auch gerne noch eingebaut bevor das ganze aufgestellt wird, das würde aber eine Inbetriebnahme enorm in Zeitverzug bringen, da ich aktuell keine Zeit für die Lötarbeiten an der Platine habe.

ToDo:
- Skript läuft nach der Installation soweit bis auf:
  - es ist keine plist.csv vorhanden, woraufhin ein harter Fehler erscheint
  - die Grundkonfiguration von Mopidy muss noch erstellt und hinterlegt werden

- Stromverbrauch messen
- geeignetes Display suchen
- Lötarbeiten LEDs anzubinden
- Skript weiter ausfeilen um auf die LEDs entsprechend anzusteuern
- nach einer Möglich suchen die Beleuchtung via Proximity zu aktivieren
- ...
