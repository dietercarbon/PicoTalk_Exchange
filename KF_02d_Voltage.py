from machine import ADC
import time

def read_voltage(ADC_Pin=26, V_max=4.2):
    adc = ADC(ADC_Pin)
    adc_value = adc.read_u16()
    voltage = (adc_value / 65535) * V_max  # Umrechnung des ADC-Werts in Spannung
    return voltage

if __name__ == "__main__":

    while True:
        voltage = read_voltage()
        #print(f"Gemessene Spannung am Optokoppler-Ausgang: {voltage:.2f} V")
        print(voltage)
        time.sleep(1)
