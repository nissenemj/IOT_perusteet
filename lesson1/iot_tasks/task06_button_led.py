
from machine import Pin
from time import sleep
LED_PIN = 15
BTN_PIN = 14

led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)

INVERT = False
while True:
    v = btn.value()
    led.value(0 if (INVERT and v) else v)
    sleep(0.01)
