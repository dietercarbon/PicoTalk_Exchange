***Themen & Links*** <br><br>
HERZLICHEN DANK an die "Melder" !!! <br><br>

17  Harry (Harald Tietze) hat (glücklicherweise) das Waveshare Touch-Display 3.5 (siehe 11) für Pico bereits on Betrieb nehmen können; es hat funktioniert mit Pico und Pico 2, allerdings "ohne W".<br>
Test-Programm siehe oben "HT_01 ...".<br><br>

16  Patrick (Schnabel; PS): führt eindrucksvoll Offline-Spracherkennung mit Pico vor auf Basis von:<br>
Gravity: Offline Language Learning Voice Recognition Sensor for Arduino/Raspberry Pi/Python / ESP32 - I2C & UART - SEN0539-EN.<br>
Bezugsmöglichkeit:  https://www.berrybase.de/dfrobot-gravity-offline-spracherkennungssensor-i2c-uart-121-befehle-370ma-3-5v<br>
Siehe hierzu auch auf Youtube:<br>
https://www.youtube.com/watch?v=CSvMd9mN9Q0<br>
https://www.youtube.com/watch?v=k7IjKCNlVqk<br><br>

15  Johannes (Marko; JM): stellt "Energie sparen mit Raspberry Pi Pico" vor auf Basis des Timers "Nano-Power System Timer TPL5111".<br>
Hierdurch kann deutlich die Laufzeit der Stromversorgung erhöht werden.<br>
Beschreibung siehe oben: "JM_03 ...".<br>
Bezugsmöglichkeit:  https://www.berrybase.de/adafruit-tpl5111-low-power-timer-breakout<br> <br>

14  Harry (Harald Tietze) unterstützt unsere Suche nach guten Temperatursensoren: der TMP117 mit sensationeller Genauigkeit < 0.1 Grad:<br>
https://www.ti.com/lit/ds/symlink/tmp117.pdf?ts=1751518805932<br>
https://learn.adafruit.com/adafruit-tmp117-high-accuracy-i2c-temperature-monitor/downloads<br>
https://www.berrybase.de/adafruit-tmp117-0.10c-hochpraeziser-i2c-temperatursensor
<br><br>

13  Patrick stellt vor und beschreibt allgemein "Raspberry Pi Pico im Stand-alone-Betrieb":<br>
https://www.elektronik-kompendium.de/sites/raspberry-pi/2802141.htm<br>

... und speziell eine geschickte Methode, auf Programm-Abbrüche automatisch und "manuell" reagieren zu können "Raspberry Pi Pico: Autostart mit Abbruch, Fehlerbehandlung und Neustart":<br>
https://www.elektronik-kompendium.de/sites/raspberry-pi/2905071.htm
<br><br>

12  Dieter findet eine für Pico-Lötungen und Lösungen geeignete (Größe und Preis) Streifenplatine:<br>
https://www.amazon.de/dp/B085WJ7535?ref=fed_asin_title
<br><br>

11  Ralf nennt auf Dieters Umfrage nach einem Waveshare-Produkt den passenden Link für einen "großen und günstigen" Touch-Screen:<br>
https://www.berrybase.de/3-5-zoll-touch-display-modul-fuer-raspberry-pi-pico-65k-farben-480-320-spi
<br><br>

10  Johannes hat den Watch Dog Timers (WDT) in Micropython genauer untersucht:<br>
"Ich habe mir das Ganze jetzt noch mal genauer angeschaut und das eigentliche Problem war, dass ich nur ca. ein Mal pro Minute eine gemachte Messung an einen Server melden wollte (einfach um Strom zu sparen für eine Messgröße, die  sich kaum ändert innerhalb einer Minute...) , aber der WDT in Micropython einen Maximalwert von ca. 8 Sekunden hat (s. Aussage unten). Zudem kann es Probleme im WLAN geben, wenn man zu viele Messwerte in kurzer Zeit übertragen will.<br> 
Mittlerweile experimentiere ich mit einer sehr einfachen Lösung wie folgt:Man stellt den WDT z.B. fest auf 6 Sekunden ein und führt dann in der Hauptschleife nur bei  jedem zehnten Schleifendurchgang eine Messung tatsächlich durch. Die Hauptschleife selber sollte dann keine großen Verzögerungen oder Wartezeiten haben.  
Beispiel:<br>
Man kann den %-Operator nutzen, um zu erreichen, dass eine Aktion z.B. nur bei jedem zehnten Schleifendurchgang tatsächlich ausgeführt wird.  
if (counter % 10)  == 0: &nbsp;&nbsp; # Die Variable counter wird  bei jedem Schleifendurchgang um eins erhöht.<br>
action() &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  #  Der %-Operator berechnet den Rest einer Division<br>

Man sollte (ggf. mehrmals) den WDT in der Hauptschleife "füttern", damit dieser nicht ungewollt zuschlägt. <br>
Ich werde jetzt mal  ausprobieren, ob eine entspr. Änderung in dem Programmcode hilft, die Messungen dauerhaft stabil zu betreiben. In ein paar Monaten kann ich dann zuverlässig sagen, ob diese Lösung stabil läuft. Wichtig für mich ist, dass der Pico sich immer wieder selbst neu startet, wenn ein unerwartetes Problem auftritt. Wenn dann mal ein paar Messungen nicht "ankommen", spielt das keine große Rolle. <br>
P.S.<br> 
Der maximale Timeout-Wert für den Watchdog-Timer (WDT) in MicroPython für RP2040-Geräte ist 8388 Millisekunden (8,388 Sekunden). Dieser Wert muss in Millisekunden angegeben werden. Sobald der WDT gestartet ist, kann der Timeout-Wert nicht mehr geändert werden. Der WDT kann auch nicht gestoppt werden."<br> <br>

9  Uli (Romahn; UR): beschreibt liebevoll und einsteiger-geeignet (!) eine selbstentwickelte Ampelanlage für Bahnübergang mit automatischer Zug-Annäherungserkennung.<br>
Beste Grüße an die Enkel, die tatkräftig mitgewirkt haben.<br>
Beschreibung und Programm siehe "UR_01 ...".<br> <br>

8  Johannes (Marko; JM): beschreibt eine selbstkonzipierte "remote Meldestelle" auf Basis LoRa P2P Verbindung, autonom und ohne Gateway.<br>
Beschreibung siehe oben: "JM_02 ...".<br>
Programme siehe: https://github.com/trapperjoe/  im Repository "Ereignismeldung".<br> <br>

7  Kai (Fuchsberger; KF): beschreibt einen selbstkonzipierten "Stromausfallmelder".<br>
Beschreibung und Programme siehe oben: "KF_02 ...".<br> <br>

6  Dieter (Carbon; DC): wenn das so funktioniert wie ich GLAUBE, kann "Pimoroni Presto" m.E. ein Gamechanger werden! <br>
... habe vorsichtshalber 2 bestellt ... und werde berichten ... spätestens im nächsten PicoTalk. <br>
https://shop.pimoroni.com/products/presto?variant=54894104019323 <br>
... und ein erster Erfahrungsbericht von Kevin McAleer: <br>
https://www.youtube.com/watch?v=9F3R4p2UXoo <br> <br>

5  Michel (Dr. Döhring; MD): Das erste ist eine 19“-Workstation als open source Hardware-Projekt für die eigene Werkstatt. Das finde ich sehr interessant, da es Modular ist. Aktuell fehlen mir noch einige Teile, die ich gerne hätte, aber grundsätzlich sobald die da sind, könnte man damit tolle Dinge tun. <br>
https://github.com/Synthron/ModLab <br><br>

4  Michel (Dr. Döhring; MD): Das zweite befasst sich mit Passkeys auf dem Pico. Habe ich selbst nicht benutzt bisher aber als Hinweis für einige vielleicht interessant.
"Fido2 Passkey - Looking for a secure login with 2FA? With Pico Fido you will have a Fido2 Passkey in your hands." <br>
https://www.picokeys.com/ <br><br>

3  Patrick (Schnabel; PS): Website zum Simulieren von Pico-Projekten. <br>
https://wokwi.com/projects/new/micropython-pi-pico <br><br>

2  Bernhard (Betz; BB): PicoCalc ist ein neuer Handheld. Dieser basiert auf einem Raspberry Pi, wobei für die Eingabe von Text eine entsprechende Tastatur bereitsteht.
Optisch ist das Modell deutlich an einen Taschenrechner angelehnt, bei der Rechenkapazität ergeben sich doch deutlich Einschränkungen.  <br>
https://www.clockworkpi.com  <br><br>

1  Kai (Fuchsberger; KF): Olimex Schaltsteckdose 230V 16A für Arduino, ESP32 und Raspberry Pi PWR-SWITCH <br>
https://www.roboter-bausatz.de/p/olimex-schaltsteckdose-230v-16a-fuer-arduino-esp32-und-raspberry-pi-pwr-switch <br><br>
