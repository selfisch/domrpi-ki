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
