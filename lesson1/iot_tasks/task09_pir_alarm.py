# PIR-murtohälytin: Armaa/Disarmaa napilla, LED+summeri, tapahtumaloki (ekstra)
from machine import Pin
from time import sleep
from utils import Debouncer

PIR_PIN  = 16
LED_PIN  = 15
BUZZ_PIN = 5
BTN_PIN  = 14

pir  = Pin(PIR_PIN, Pin.IN)
led  = Pin(LED_PIN, Pin.OUT)
buzz = Pin(BUZZ_PIN, Pin.OUT)
btn  = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)

armed = True

def on_btn(pin):
    global armed
    armed = not armed
    print("ARMED" if armed else "DISARMED")

deb = Debouncer(btn, delay_ms=250)
deb.attach(lambda pin: on_btn(pin))
btn.irq(trigger=Pin.IRQ_RISING, handler=deb.irq)

while True:
    if armed and pir.value():
        led.value(1); buzz.value(1)
        print("Motion detected!")
        sleep(1.0)
        buzz.value(0)
    else:
        led.value(0)
    sleep(0.05)
