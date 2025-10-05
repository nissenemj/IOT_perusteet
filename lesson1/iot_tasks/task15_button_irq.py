# Button keskeytys + Debouncer-luokka (ekstra) -> toggle LED
from machine import Pin
from utils import Debouncer

LED_PIN, BTN_PIN = 15, 14
led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)

state = 0
def on_press(pin):
    global state
    state = 1 - state
    led.value(state)
    print("LED:", state)

deb = Debouncer(btn, delay_ms=200)
deb.attach(on_press)
btn.irq(trigger=Pin.IRQ_RISING, handler=deb.irq)

while True:
    pass
