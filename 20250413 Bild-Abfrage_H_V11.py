# 20250413 Bild-Abfrage_G_V11.py
#
# NEU:  3 Antwort-Angebote nur mit schwarzer Schrift (ohne weißen Untergrund)
#
# ggf. refresh ???
#
# TEST mit 240 x 240 
#
# "Wer oder was ist das ?"
#
# Von SD-Karte aus Verzeichnis "gallery" werden all Ordner eingelesen,
# und max. 5 werden zur Auswahl angezeigt.
#
# alle Bilder  werden von SD-Karte aus Verzeichnis "gallery"
#              und entsprechendem Ordner eingelesen,
#              müssen Format haben: 120x180 und  .jpg ,
#              erscheinen auf linker Screen-Hälfte.
#
# Bild-Titel werden in 3 Antwort-Button auf rechter Screen-Hälfte angezeigt,
# der korrekte ist dabei und 2 weitere zufällig,
# die 3 Antwort-Button werden in zufälliger Reihenfolge anzezeigt.
#
# bei Touch auf richtige Antwort:
#     - unten wird "Richtig!" auf grünem Feld angezeigt,
#     - 2 Sek. später: nächstes Bild.
#
# bei Touch auf falsche Antwort:
#     - unten wird "Falsch!" auf rotem Feld angezeigt,
#     - Bild bleibt stehen, bis richtige Antwort.
#
# bei Touch auf unten_links:    Rücksprung zur Ordner-Übersicht
# bei Touch auf unten_rechts:   Ende
#
#
#
import machine
import sdcard
import uos
import jpegdec
from presto import Presto
from touch import Button
from utime import sleep
import random

# Presto initialisieren
presto = Presto()
display = presto.display
touch = presto.touch
WIDTH, HEIGHT = display.get_bounds()
print("Breite:", WIDTH, "Höhe:", HEIGHT)
j = jpegdec.JPEG(display)
display.set_font("bitmap8")

# Couple of colours for use later
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(230, 60, 45)
GREEN = display.create_pen(9, 185, 120)
BLACK = display.create_pen(0, 0, 0)

CX = WIDTH // 2
CY = HEIGHT // 2
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 20
ANZEIGE_X = 140
ANZEIGE_Y = 190

# Create a touch button and set the touch region.
# Button(x, y, width, height)
button_1 = Button(125, 60, BUTTON_WIDTH, BUTTON_HEIGHT)
button_2 = Button(125, 95, BUTTON_WIDTH, BUTTON_HEIGHT)
button_3 = Button(125, 130, BUTTON_WIDTH, BUTTON_HEIGHT)
button_unten_links = Button(0,220,40,20)
button_unten_rechts = Button(200,220,40,20)


# SD-Karte mounten
sd_spi = machine.SPI(0, sck=machine.Pin(34), mosi=machine.Pin(35), miso=machine.Pin(36))
sd = sdcard.SDCard(sd_spi, machine.Pin(39))
uos.mount(sd, "/sd")
#

weiter_machen = True
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
while weiter_machen == True:
#
    # Buttons zur Ordnerauswahl definieren (x, y, Breite, Höhe)
    ordner_buttons = [
        Button(10, 40 + i * 30, 200, 25) for i in range(5)
    ]

    # Alle Ordner in /sd/gallery finden und sortieren
    alle_ordner = [f for f in uos.listdir("/sd/gallery") if not "." in f]
    alle_ordner.sort()
    print("Gefundene Ordner:", alle_ordner)

    # Maximal 5 Ordner anzeigen
    anzahl_anzeigen = min(5, len(alle_ordner))
    ordner_auswahl = alle_ordner[:anzahl_anzeigen]

    # Anzeige: Auswahltext und Ordner-Buttons
    display.set_pen(WHITE)
    display.clear()
    display.set_pen(BLACK)
    display.text("Bitte Ordner wählen:", 10, 10)

    for i in range(anzahl_anzeigen):
        display.set_pen(BLACK)
        display.rectangle(*ordner_buttons[i].bounds)
        display.set_pen(WHITE)
        display.text(ordner_auswahl[i], ordner_buttons[i].x + 5, ordner_buttons[i].y + 5)

    presto.update()

    # Auf Touch warten
    gewaehlter_ordner = None
    while gewaehlter_ordner is None:
        touch.poll()
        if touch.state:
            for i, button in enumerate(ordner_buttons[:anzahl_anzeigen]):
                if button.is_pressed():
                    gewaehlter_ordner = ordner_auswahl[i]
                    print("Ausgewählter Ordner:", gewaehlter_ordner)
                    break

    # Bildverzeichnis neu setzen basierend auf Auswahl
    directory = f"/sd/gallery/{gewaehlter_ordner}"



    # Bildverzeichnis einlesen
    # directory = "/sd/gallery"
    files = [f for f in uos.listdir(directory) if f.endswith(".jpg")]
    files.sort()
    print("Gefundene Dateien:", files)

    # Liste der Namen ohne Dateiendung
    names = [f[:-4] for f in files]  # ".jpg" entfernen
    print("Namen:", names)

    # Bildanzeige-Funktion
    def show_image(filename):
        try:
            path = f"{directory}/{filename}"
            print(f"filename: {path}")
            j.open_file(path)
            display.set_pen(WHITE)
            display.clear()
    
            j.decode(0,0)  # 30 Pixel nach unten
            presto.update()  # Zeigt Foto an     <------------------
        except Exception as e:
            print(f"Fehler beim Anzeigen von {filename}: {e}")

    # Start mit zufälligem Bild
    total = len(files)                  # Anzahl der Fotos
    indices = list(range(total))        # Indices gehen von 0 bis total-1
    print("total =", total)             # im Bsp.: 4
    print("Alle Indices:", indices)     # 0,1,2,3


    presto.update()

    if total <= 0:
        print("Keine Bilder gefunden.")
        # Hier könntest du ggf. eine Schleife oder eine Funktion zum Stoppen aufrufen
        raise SystemExit  # Das beendet das Programm
    else:
        # Clear the screen and set the background colour
        display.set_pen(WHITE)
        display.clear()
        display.set_pen(BLACK)
        
        #display.text("Wer oder was ist das ?", 12, 8)
        
        im_Ordner_weitermachen = True
        
        while im_Ordner_weitermachen == True and weiter_machen == True:
            indices = list(range(total))
            index_aktuell = random.randint(0, total - 1)   # Index für aktuelles Foto per Zufall
            print()
            print("index_aktuell =", index_aktuell)
            show_image(files[index_aktuell])               # Funktion lädt + zeigt Foto 
            print("Name =", names[index_aktuell])
            
            # nimm aktuellen Index raus aus indices
            indices.remove(index_aktuell)                   # Foto-Index wird rausgenommen
            indices_ohne_Zeige_Index = indices
            print("indices_ohne_Zeige_Index:", indices_ohne_Zeige_Index)
            index0 = index_aktuell
            
            # Zwei zufällige, unterschiedliche Indices aus indices_ohne_Zeige_Index
            if len(indices_ohne_Zeige_Index) >= 2:
                i1 = random.randint(0, len(indices_ohne_Zeige_Index) - 1)
                
                # Schleife, um sicherzustellen, dass i2 ≠ i1
                while True:
                    i2 = random.randint(0, len(indices_ohne_Zeige_Index) - 1)
                    if i2 != i1:
                        break
                
                index1 = indices_ohne_Zeige_Index[i1]
                index2 = indices_ohne_Zeige_Index[i2]
                
                print("Zufällige Indices (ohne aktuellen):", index1, index2)
            else:
                print("Nicht genug weitere Indices für zwei Alternativen.")
            
            print()
            print("antwort1 = ",names[index0])
            print("antwort2 = ",names[index1])
            print("antwort3 = ",names[index2])

            # Liste der Namen der drei Antworten
            antworten = [names[index0], names[index1], names[index2]]

            # Eigene Shuffle-Alternative
            antworten_indices = list(range(3))
            for i in range(2, 0, -1):
                r = random.randint(0, i)
                antworten_indices[i], antworten_indices[r] = antworten_indices[r], antworten_indices[i]

            antwort1 = antworten[antworten_indices[0]]
            antwort2 = antworten[antworten_indices[1]]
            antwort3 = antworten[antworten_indices[2]]

            print()
            print("Zufällige Zuordnung:")
            print("antwort1 =", antwort1)
            print("antwort2 =", antwort2)
            print("antwort3 =", antwort3)
            
            #display.set_pen(WHITE)
            #display.rectangle(*button_1.bounds)
            #display.rectangle(*button_2.bounds)
            #display.rectangle(*button_3.bounds)
            
            display.set_pen(BLACK)
            display.text(antwort1, button_1.x+4, button_1.y+3, 100, 2)
            display.text(antwort2, button_2.x+4, button_2.y+3, 100, 2)
            display.text(antwort3, button_3.x+4, button_3.y+3, 100, 2)
            
            
            presto.update()
            
            print("Z 157")
            
            Antwort = False
            
            while Antwort == False and im_Ordner_weitermachen == True and weiter_machen == True:
            
                touch.poll()
                if touch.state:
            
                    if button_1.is_pressed():
                        if names[index_aktuell] == antwort1:
                            Antwort = True
                            print("richtig")
                            display.set_pen(GREEN)
                            display.rectangle(ANZEIGE_X,ANZEIGE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)                            
                        else:
                            print("falsch")
                            display.set_pen(RED)
                            display.rectangle(ANZEIGE_X,ANZEIGE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)   
                            
                    if button_2.is_pressed():
                        if names[index_aktuell] == antwort2:
                            Antwort = True
                            print("richtig")
                            display.set_pen(GREEN)
                            display.rectangle(ANZEIGE_X,ANZEIGE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)        
                        else:
                            print("falsch")
                            display.set_pen(RED)
                            display.rectangle(ANZEIGE_X,ANZEIGE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)   
                            
                    if button_3.is_pressed():
                        if names[index_aktuell] == antwort3:
                            Antwort = True
                            print("richtig")
                            display.set_pen(GREEN)
                            display.rectangle(ANZEIGE_X,ANZEIGE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)        
                        else:
                            print("falsch")
                            display.set_pen(RED)
                            display.rectangle(ANZEIGE_X,ANZEIGE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)      
                            
                                        
                    if button_unten_links.is_pressed():
                        im_Ordner_weitermachen = False
                        break
                        
                    if button_unten_rechts.is_pressed():
                        weiter_machen = False
                        break
                    
                    display.set_pen(BLACK)
                    display.text("Richtig!" if Antwort else "Falsch!", ANZEIGE_X + 2, ANZEIGE_Y + 2, 100, 2)

                    presto.update()
                    sleep(2)
                    
                    display.set_pen(WHITE)
                    display.rectangle(ANZEIGE_X,ANZEIGE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)   
                    
                    presto.update()
                    
print("292",weiter_machen)
display.set_pen(WHITE)
display.clear()
display.set_pen(BLACK)
display.text("Bye bye !!!",60,110,140,3)      
presto.update()                        
        
        
