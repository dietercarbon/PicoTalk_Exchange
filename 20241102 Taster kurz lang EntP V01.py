from machine import Pin
import time

# Initialisiere die LEDs und den Taster mit den neuen GPIO-Pins
green_led = Pin(20, Pin.OUT, value=0)  # Grüne LED ist initial aus
red_led = Pin(18, Pin.OUT, value=0)    # Rote LED ist initial aus
button = Pin(0, Pin.IN, Pin.PULL_DOWN)  # Verwende Pin 0 für den Taster

# Variablen zum Speichern der Zeit
press_time = 0
release_time = 0

# Variable für die Entprellung
last_press = 0  # Zeitpunkt des letzten Tastendrucks
debounce_time = 100  # 100 ms Entprellzeit

def button_isr(pin):
    global press_time, release_time, last_press
    
    # Verhindern, dass Prellen als Tastendruck erkannt wird
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press) < debounce_time:
        return
    
    last_press = current_time  # Aktualisiere den Zeitpunkt des letzten Tastendrucks
    
    if button.value() == 1:  # Taster wurde gedrückt
        press_time = current_time
        print("Taster gedrückt")
    else:  # Taster wurde losgelassen
        release_time = current_time
        print("Taster losgelassen")
        
        # Berechne die Dauer des Tastendrucks
        press_duration = time.ticks_diff(release_time, press_time)
        
        # Schwellenwert für kurzen oder langen Tastendruck (z.B. 1000 ms)
        if press_duration < 1000:
            # Kurzer Druck, grüne LED leuchtet
            green_led.on()
            red_led.off()
            print("Kurzer Druck: Grüne LED")
        else:
            # Langer Druck, rote LED leuchtet
            red_led.on()
            green_led.off()
            print("Langer Druck: Rote LED")

# Verwende nur den FALLING-Interrupt und überprüfe den Pin-Zustand in der ISR
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_isr)

# Hauptschleife (kann leer bleiben)
while True:
    time.sleep(0.1)
