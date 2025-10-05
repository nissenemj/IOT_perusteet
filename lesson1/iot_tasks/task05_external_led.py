from machine import Pin
from time import sleep
LED_PIN = 15
led = Pin(LED_PIN, Pin.OUT)

period = 0.5
while True:
    led.value(1); sleep(period)
    led.value(0); sleep(period)
