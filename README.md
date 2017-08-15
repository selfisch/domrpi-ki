# domrpi-ki
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


Skript läuft soweit.
Aktuell habe ich mich für die Steuerung über eine 5 Button Maus entschieden, um überhaupt etwas machen zu können.
Grundsätzlich hat die Anlage auf der Front an die 20 Knöpfe, die ich jedoch nicht via GPIO ansteuern kann, da ich auch noch diverse LEDs ansteuern muss.
Alternativ habe ich somit momentan die Überlegung, die Button über eine USB Lösung anzusteuern/auszulesen.
Falls jemand etwas derartiges schon gemacht hat, ich bin für Vorschläge offen :-).

ToDo:
- Stromverbrauch messen
- geeignete USB Lösung für die Realisierung der Buttons suchen
- geeignetes Display suchen
- Lötarbeiten um Buttons und LEDs anzubinden
- Skript weiter ausfeilen um auf die LEDs entsprechend anzusteuern
- nach einer Möglich suchen die Beleuchtung via Proximity zu aktivieren
- ...
