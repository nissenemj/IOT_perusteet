# Sääasema OLED-näytöllä (valinnainen) + trendinuoli (ekstra)
from machine import Pin, I2C
from time import sleep
import dht
try:
    import ssd1306
except:
    ssd1306 = None

DHT_PIN = 13
SCL_PIN, SDA_PIN = 1, 0
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
sensor = dht.DHT22(Pin(DHT_PIN))

oled = ssd1306.SSD1306_I2C(128, 64, i2c) if ssd1306 else None
last_t = None

def trend(cur, prev):
    if prev is None: return "-"
    if cur > prev + 0.2: return "↑"
    if cur < prev - 0.2: return "↓"
    return "→"

while True:
    sensor.measure()
    t = sensor.temperature()
    h = sensor.humidity()
    tr = trend(t, last_t)
    last_t = t
    if oled:
        oled.fill(0)
        oled.text("Weather", 0, 0)
        oled.text("T: {:.1f} C {}".format(t, tr), 0, 16)
        oled.text("H: {:.1f} %".format(h), 0, 32)
        oled.show()
    print("T={:.1f}C{} H={:.1f}%".format(t, tr, h))
    sleep(2)
