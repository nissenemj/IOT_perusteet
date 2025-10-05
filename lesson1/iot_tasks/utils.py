# Apuluokat & -funktiot
import time
try:
    import uasyncio as asyncio
except:
    asyncio = None

def safe_sleep(seconds):
    # katko pieniin pätkiin, ettei watchdog tai timereiden callbackit jäädy
    end = time.time() + seconds
    while time.time() < end:
        time.sleep(0.05)

class Stats:
    def __init__(self):
        self.count = 0
        self.total = 0.0
        self.min_v = None
        self.max_v = None

    def add(self, v):
        self.count += 1
        self.total += v
        self.min_v = v if self.min_v is None else min(self.min_v, v)
        self.max_v = v if self.max_v is None else max(self.max_v, v)

    def mean(self):
        return self.total / self.count if self.count else None

try:
    from machine import Pin
except:
    Pin = None

def led_blink(pin_obj, times=2, on_ms=80, off_ms=80):
    if not pin_obj:
        return
    for _ in range(times):
        pin_obj.value(1); time.sleep(on_ms/1000)
        pin_obj.value(0); time.sleep(off_ms/1000)

class Debouncer:
    def __init__(self, pin, delay_ms=200):
        self.pin = pin
        self.delay_ms = delay_ms
        self.last = 0
        self.fn = None

    def attach(self, fn):
        self.fn = fn

    def irq(self, *_):
        import utime
        now = utime.ticks_ms()
        if utime.ticks_diff(now, self.last) > self.delay_ms:
            self.last = now
            if self.fn:
                self.fn(self.pin)

class WiFiHelper:
    def __init__(self, ssid, pwd, timeout=20):
        import network
        self.ssid = ssid
        self.pwd = pwd
        self.timeout = timeout
        self.network = network
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        self.wlan.active(True)
        if self.wlan.isconnected():
            return True
        self.wlan.connect(self.ssid, self.pwd)
        start = time.time()
        while not self.wlan.isconnected():
            if time.time() - start > self.timeout:
                return False
            time.sleep(0.5)
        return True

    def ensure(self):
        if not self.wlan.isconnected():
            return self.connect()
        return True
