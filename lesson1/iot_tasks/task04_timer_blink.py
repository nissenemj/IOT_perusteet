# Timer-pohjainen blink (ei aktiivista odotusta) + laskuri
from machine import Pin, Timer
led = Pin("LED", Pin.OUT) if isinstance("LED", str) else Pin(2, Pin.OUT)
tim = Timer()
count = 0

def tick(t):
    global count
    led.toggle()
    count += 1
    if count % 10 == 0:
        print("Toggles:", count)

tim.init(freq=5, mode=Timer.PERIODIC, callback=tick)

while True:
    pass
