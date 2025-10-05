# Potentiometri -> ADC -> LED-kirkkaus PWM + jännite (ekstra)
from machine import ADC, Pin, PWM
from time import sleep

pot = ADC(26)  # GP26/ADC0
led = PWM(Pin(15))
led.freq(1000)

while True:
    raw = pot.read_u16()       # 0..65535
    volts = raw * 3.3 / 65535  # jännite-asteikko
    duty = raw                 # käytä suoraan
    led.duty_u16(duty)
    print(raw, "->", "{:.2f} V".format(volts))
    sleep(0.1)
