# Bibliotheken laden
from machine import Pin
from time import sleep

# Initialisierung: Onboard-LED
led1 = Pin(13, Pin.OUT, value=0)
led2 = Pin(14, Pin.OUT, value=0)

# Initialisierung: GPIO21 und 22 als Eingang für die 2 TRCT5000
btn1 = Pin(21, Pin.IN)
btn2 = Pin(22, Pin.IN)

# Wiederholung (Endlos-Schleife)
while True:
    #value_d = sensor_d.value()
    # print(value_d)
    #if value_d == 0:
    if btn1.value() == 0 or btn2.value() == 0:
        # LED einschalten
        led1.on()
        led2.on()              
    # halbe Sekunde warten
        sleep(0.5)
    # LED ausschalten
        led1.off()
        led2.off()             
    # 1 Sekunde warten
        sleep(0.5)
            
    else:
        led1.off()
        led2.off()
        