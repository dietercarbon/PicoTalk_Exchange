# Program for continous swings of the Magic Pendulum [Version 5.0]
# 06.12.2024
# Importiere Libraries
import machine
import utime
from machine import ADC
from machine import Pin

# Initialize ADC0 (GPIO26) - PIN-31
adc0 = ADC(0)

# Initialisierung von GPIO25 als Ausgang
led_onboard = Pin(25, Pin.OUT)

# Switch on onboard LED, zum Zeichen, dass der Raspi läuft...
led_onboard.on()

# Definition LEDs
led_red    = machine.Pin(15, machine.Pin.OUT) # PIN-20
led_yellow = machine.Pin(14, machine.Pin.OUT) # PIN-19
led_green  = machine.Pin(13, machine.Pin.OUT) # PIN-17

# Definition von Variablen
off = 0
on = 1

tck = 0
tck0 = 0
tck1 = 0
tck2 = 0
tck3 = 0

# Initialisiere Hall Sensor. GPIO16 = PIN-21
button_16 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)


# Schalte die LEDs kurz ein, zum Zeichen, dass das Programm läuft
def initialize():
    led_red.value(off); led_yellow.value(off); led_green.value(off)
    utime.sleep(4)
    led_red.value(on); led_yellow.value(on); led_green.value(on)
    utime.sleep(2)
    led_red.value(off); led_yellow.value(off); led_green.value(off)
    utime.sleep(1)
    led_onboard.value(on)
    
# Prüfe den Wert der Hall-Sensors und melde zurück, ob dieser ein Magnetfeld entdeckt hat
def read_hall():
    read0 = 0
    read0 = adc0.read_u16()
    tck = utime.ticks_add(utime.ticks_ms(), 0)
    #print("read0 = \t", read0)
    #print(tck, '\t', read0)
    if read0 < 20000:
        return(on) 		# Ein Magnetfeld wurde enteckt
    else:
        return(off) 	# Kein Magnetfeld entdeckt

# Warte bis zum Triggerpunkt
def wait_trigger():
# Warte bis der Hall-Sensor ein Magnetfeld erkennt
    while read_hall() == off:
        utime.sleep_ms(2)
    led_yellow.value(on)
    
# Warte bis das Magnetfeld wieder verschwindet     
    while read_hall() == on:
        utime.sleep_ms(2)
    tck1 = utime.ticks_ms()
    led_yellow.value(off)
    return tck1   
    
        
# Hauptprogramm
initialize()
tck0 = utime.ticks_ms() 
tck1_00 = 0
m = 0

while True:
    tck1 = wait_trigger()
# Berechne die Zeitdauer vom letzten Triggerimpuls
    tdauer = tck1-tck1_00
    tck1_00 = tck1

# Wenn tdauer bei etwa 800ms liegt, dann ist der Triggerzeitpunkt erreicht
    if (tdauer > 750) and (tdauer < 850):
        led_green.value(on)	# Start der aktiven Phase
        tck1 = utime.ticks_ms()
        
# Jetzt ist der Triggerzeitpunkt erreicht
# Warte noch kurz bis das Pendel in der Nähe des E-Magneten ist
        utime.sleep_ms(220)
        tck2 = utime.ticks_ms()
        
# Schalte den E-Magnet kurz ein
        led_red.value(on)
        utime.sleep_ms(200)
        
# Schalte den E-Magnet wieder aus
        led_red.value(off)
        
        tck3 = utime.ticks_ms()
        led_green.value(off) # Ende der aktiven Phase
        m += 1
        # print(m, '\t', tck1-tck0,'\t', tck2-tck0, '\t', tck3-tck0)
       
                  




