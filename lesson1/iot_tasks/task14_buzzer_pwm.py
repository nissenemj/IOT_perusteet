# Buzzer: PWM äänimerkit + pieni "melodia" (ekstra)
from machine import Pin, PWM
from time import sleep
BUZZ = PWM(Pin(5))
BUZZ.freq(1000)

def tone(freq, ms=200):
    BUZZ.freq(freq)
    BUZZ.duty_u16(32768)
    sleep(ms/1000)
    BUZZ.duty_u16(0)

scale = [523, 587, 659, 698, 784, 880, 988, 1047]  # C5..C6
for f in scale:
    tone(f, 120)
sleep(0.5)
for f in reversed(scale):
    tone(f, 90)
BUZZ.deinit()
