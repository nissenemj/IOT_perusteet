# Sisäinen LED blink + "breathing" PWM 
from machine import Pin, PWM
from time import sleep

# ESP32: käytä pin 2
led = Pin(2, Pin.OUT)

# Perusblink
print("Perusblink alkaa...")
for _ in range(4):
    led.value(1)
    sleep(0.2)
    led.value(0)
    sleep(0.2)

print("Breathing PWM alkaa...")
# "Breathing" PWM
try:
    p = PWM(led)
    p.freq(1000)
    for _ in range(2):
        # Himmeästä kirkkaaksi
        for d in range(0, 65535, 1024):
            p.duty_u16(d)
            sleep(0.01)
        # Kirkkaasta himmeäksi
        for d in range(65535, -1, -1024):
            p.duty_u16(d)
            sleep(0.01)
    p.deinit()
    print("Valmis!")
except Exception as e:
    print("PWM-virhe:", e)

