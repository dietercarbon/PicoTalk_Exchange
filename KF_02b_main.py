from machine import UART, Pin, RTC
import time
from Voltage import read_voltage
from PData import phone_number_receiver, PIN_self

# Pinbelegung für Raspberry PI Pico

# UART-Schnittstelle initialisieren (UART0, 9600 Baud, TX auf Pin 12, RX auf Pin 13)
# Dient zur Kommunikation vom Pico mit dem SIM800L G2-Modem
uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))
print("UART wurde initialisiert.")

def send(cmd):
    """
    Sendet ein AT-Kommando an das SIM800L-Modul.
    Fügt automatisch Zeilenumbruch hinzu.
    Gibt das gesendete Kommando zur Kontrolle aus.
    """
    uart.write(cmd + "\r\n")
    print(f"sent: {cmd}")

def read_lines(expected = "OK", timeout_s=60):
    """
    Liest alle empfangenen Zeilen vom UART
    bis der erwartete Inhalt expected enthalten ist und gibt diesen Inhalt als String aus, oder
    bis der timeout_s in Sekunden überschritten ist und gibt dan den String "Timout" aus.
    """
    lines = []
    line = b""
    start = time.time()
    while (time.time() - start < timeout_s):
        #print(".",end="")
        if uart.any():  # Wenn Daten im UART-Puffer liegen
            b = uart.read(1)  # Lese ein Byte
            if b == b'\n' or b == b'\r':  # Zeilenende erkannt
                #if line:  # Wenn die Zeile nicht leer ist
                #    print("line", line)
                if expected in line:
                    return str(line)
                    break
            else:
                line += b  # Byte zur aktuellen Zeile hinzufügen
        else:
            time.sleep(0.02)  # Kurze Pause, um CPU zu schonen
    return "timeout"

def sync_rtc_with_sim800():
    """Fragt die Uhrzeit beim SIM-Karten Mobilfunkanbieter ab und setzt damit die RTC des Pico"""
    # 1) Uhrzeit abfragen
    send("AT+CCLK?")
    line = read_lines(expected = "+CCLK:")
    #print(line)
    # 2) Zeile mit +CCLK splitten
    parts = line.split('"')
    if len(parts) >= 2:
        ts = parts[1]                    # '25/04/21,14:30:50+08'
        #print("pqrts", parts, "ts", ts)
        date_part, _tz = ts.split('+', 1)
        d_str, t_str = date_part.split(',')  
        year2, month, day = d_str.split('/')
        hour, minute, second = t_str.split(':')
        year = 2000 + int(year2)
        rtc = RTC()
        rtc.datetime((year,
                      int(month),
                      int(day),
                      0,              # weekday (wird ignoriert)
                      int(hour),
                      int(minute),
                      int(second),
                      0))
        print(f"✅ RTC gesetzt auf {year}-{month}-{day} {hour}:{minute}:{second}")
        return
    print("❌ +CCLK: Zeile nicht gefunden oder ungültiges Format")



def send_sms(phonenumber, message):
    """Sendet eine SMS mit dem Inhalt message an eine Telefonnummer phonenumber"""
    uart.write(f'AT+CMGS="{phonenumber}"\r'.encode())
    print(read_lines(expected = phonenumber, timeout_s=2))
    uart.write((message + "\x1A").encode())
    print(read_lines(expected = "+CMGS"))
    return

def netreg():
    """Überprüft, ob das SIM800L Modem mit dem Netzwerk des Mobilfunkanbieter verbunden ist.
       Dies versucht er maximal 10-mal jeweils für 10 Sekunden""" 
    print("⏳ Warte auf Netzregistrierung…")
    for _ in range(10):
        send("AT+CREG?")
        resp = read_lines(expected = "+CREG: 0,1", timeout_s=10)
        if "+CREG: 0,1" in resp:
            print("✅ Registriert!")
            break
        else:
            print("⚠️ Keine Netzregistrierung")

def SIMping():
    """Pico pingt das SIM800L Modem  an um zu überprüfen, ob die Kommunikation funktioniert
       Dies versucht er maximal 10-mal."""
    print("⏳ Warte auf SIM800L Einsatzbereitschaft…")
    for _ in range(10):
        send("AT")
        resp = read_lines(timeout_s = 10)
        if "ATOK" in resp:
            print("✅ Einsatzbereit!")
            PIN()
            break
        else:
            print("⚠️ Nicht Einsatzbereit")   

def PIN(pin = PIN_self()):
    """Es wird getestet, ob die eingelegte SIM-Karte eine PIN-Eingabe fordert.
       Ist dies der Fall wird sie übergeben."""
    print("⏳ pin Registrierung...")
    send('AT+CPIN?')
    resp1 = read_lines(expected = "+CPIN:")
    if "READY" in resp1:
        print("PIN erkannt!")
        return 
    for _ in range(10):
        send(f'AT+CPIN="{pin}"')
        resp = read_lines(expected = "+CPIN:", timeout_s = 10)
        if "READY" in resp:
            print("PIN erkannt!")
            return
        else:
            print("PIN nicht erkannt.")
    return

def balance():
    """Das aktulle Guthaben auf der eingelegten SIM-Karte wird abgefragt und als String ausgegeben.
       z.B.:" 8,19 EUR""""
    send('AT+CUSD=1,"*100#"')  # Starte Guthabenabfrage
    text_out = read_lines(expected="Guthaben")
    #print("text_out", text_out)
    # Extraktion des Sub-Strings, der den Guthabenwert enthält
    pos_start = text_out.rfind(':')
    pos_end = text_out.rfind('"')
    if pos_end < len(text_out):
        pos_end = len(text_out)
    Guthaben = text_out[pos_start+1:pos_end]
    send('AT+CUSD=2') # beenden der laufenden USSD-Sitzung
    time.sleep(3)
    uart.read() # hierdurch soll evtl. gesendeter Inhalt ausgelesen und damit aus dem UART Puffer gelöscht werden
    return Guthaben

def DT(dt="d"):
    """Extraktion von Datum D (im Format: dd.mm.jj) und Uhrzeit T (im Format: hh:mm:ss) aus der RTC"""
    year, month, day, _, hour, minute, second, _ = RTC().datetime()
    D = f"{day:02d}.{month:02d}.{year:04d}"
    T = f"{hour:02d}:{minute:02d}:{second:02d}"
    if dt == "t":
        return T
    else:
        return D
    

# === Ablauf: Initialisierung und Abfrage ===
SIMping()
#send("AT")            # Teste Kommunikation
#print(read_lines())         # Lies Antwort auf AT

#send("AT+CPIN?")
#print(read_lines())

netreg()

send("AT+COPS?") # fragt den aktuell verbundenen Mobilfunkanbieter ab
print(read_lines())

""" Zur Zeitabfrage notwendig:
AT+CLTS=1      --> Aktiviert Zeitsynchronisation
AT&W           --> Speichert Einstellungen im Flash
AT+CFUN=1,1    --> Rebootet das Modul, damit CLTS aktiv wird """
send("AT+CLTS=1") # aktiviert beim SIM800L-Modul das automatische Abrufen der Uhrzeit vom Netz
print(read_lines())
send("AT&W")
print(read_lines())
send("AT+CFUN=1,1")
print(read_lines())
"""Da das SIM800L Modem zur Netzzeitabfrage rebootet wurde, wird die UART Verbindung auch "reseted""""
uart.deinit()         # UART sauber abschalten
print("UART wurde deinitialisiert.")
time.sleep(1)
uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))
time.sleep(3)
print("UART wurde initialisiert.")

SIMping()
#send("AT")            # Teste Kommunikation
#print(read_lines())

#send("AT+CREG?")      # Prüfe, ob im Netz eingebucht
#print(read_lines(expected = "+CREG: 0,1"))         # Lies Antwort auf AT+CREG?

netreg()

send("AT+CSQ")            # Teste SIgnalstärke
print(read_lines(expected = "+CSQ:"))  


send("AT+CMGF=1") # schaltet GSM-Modul in den SMS-Textmodus
print(read_lines())

send("AT+CUSD=2")     # Beende evtl. alte USSD-Sitzung
print(read_lines())         # Lies Antwort auf AT+CUSD=2

# RTC synchronisieren
sync_rtc_with_sim800()
# interne RTC ausgeben
print("🕰 Aktuelle RTC:", RTC().datetime())

text = f"Stromueberwachung startet am {DT("d")} um {DT("t")} Uhr,  (Restguthaben:{balance()}"
print(text)
send_sms(phone_number_receiver(), text)

while True:
    """Ab hier beginnt die eigentliche Netztstromüberwachung.
       Dafür muss die Schaltung über das TP4056 und USB-Kabel am Netzteil angeschlossen sein,
       welches in der zu überwachenden Steckdose steckt."""
       threshold = 2 # Wenn kein Sromausfall ist, dann liegt bei voll geladenem Li 18650
                     # eine Spannung von unter 0.2 V an.
                     # Wenn der Strom ausgefallen ist, dann liegen maximal 4.2 V bei voll geladenem Li 18560 an
    if read_voltage() > threshold: # Hier wird die Eingangsspannung am TP4056 gemessen.
        text = f"ACHTUNG! am {DT("d")} um {DT("t")} Uhr ist der Strom ausgefallen! (Restguthaben:{balance()})"
        send_sms(phone_number_receiver(), text)
        print(text)
        """Ohne diesen Teil, würden so lange SMS mit der Mitteilung über den Stromausfall geschickt werden,
           bis dieser vorüber ist. Daher die neue While-Schleife"""
        while read_voltage() > threshold:
            time.sleep(1)
        """Sobald der Strom wieder da ist, wird dies per SMS mitgeteilt."""
        text = f"Am {DT("d")} um {DT("t")} Uhr wurde der Strom wieder eingeschalten! (Restguthaben:{balance()})"
        send_sms(phone_number_receiver(), text)
        print(text)
    time.sleep(1)

uart.deinit()         # UART sauber abschalten


print("UART wurde deinitialisiert.")
