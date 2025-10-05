# Reaktiopeli: anti-cheat + keskeytys + tilastot (ekstra)
from machine import Pin
import utime, urandom
from utils import Stats

LED_PIN, BTN_PIN = 15, 14
led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)

pressed_at = None
def on_press(pin):
    global pressed_at
    if pressed_at is None:
        pressed_at = utime.ticks_ms()

btn.irq(trigger=Pin.IRQ_RISING, handler=on_press)

s = Stats()
rounds = 5

for i in range(rounds):
    pressed_at = None
    led.value(1)  # odotusvalo
    delay = 1000 + (urandom.getrandbits(10) % 2000)  # 1..3s
    utime.sleep_ms(delay)
    led.value(0)  # mitataan tästä

    start = utime.ticks_ms()
    while pressed_at is None:
        utime.sleep_ms(1)
    rt = utime.ticks_diff(pressed_at, start)
    # Anti-cheat: jos nappi oli pohjassa ennen starttia
    if rt < 20:
        print("Liian nopea - huijauksen mahdollisuus. Ei lasketa.")
        continue
    print("Kierros", i+1, "reaktio:", rt, "ms")
    s.add(rt)
    utime.sleep_ms(500)

print("Kierroksia:", s.count, "keskiarvo:", s.mean(), "ms  min:", s.min_v, "max:", s.max_v)
