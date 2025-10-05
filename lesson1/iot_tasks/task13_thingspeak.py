# DHT -> ThingSpeak robusti: uudelleen-yhdistys + backoff + LED kuittaus (ekstra)
import time, dht
from machine import Pin
from utils import WiFiHelper, safe_sleep, led_blink
import config

try:
    import urequests
except Exception as e:
    print("Puuttuu urequests:", e)
    raise

# konfig
SSID = config.WIFI["SSID"]
PWD  = config.WIFI["PASSWORD"]
API  = config.THINGSPEAK["API_KEY"]
URL  = config.THINGSPEAK["URL"]
PERIOD = config.THINGSPEAK["PERIOD_S"]

DHT_PIN = config.PINS["DHT"]
sensor = dht.DHT22(Pin(DHT_PIN))

# LED
try:
    led = Pin(config.PINS["LED_INTERNAL"], Pin.OUT)
except:
    try:
        led = Pin(2, Pin.OUT)
    except:
        led = None

wifi = WiFiHelper(SSID, PWD, timeout=20)

def send(temp, hum):
    url = "{}?api_key={}&field1={}&field2={}".format(URL, API, temp, hum)
    r = urequests.get(url)
    code, body = r.status_code, r.text
    r.close()
    return code, body

def main():
    if not API:
        print("Lisää ThingSpeak API KEY config.py:hin")
        return

    backoff = 1
    while True:
        if not wifi.ensure():
            print("WiFi ei yhdistä -> odotus", backoff, "s")
            safe_sleep(backoff)
            backoff = min(backoff * 2, 60)
            continue

        try:
            sensor.measure()
            t = float(sensor.temperature())
            h = float(sensor.humidity())
            print("Mittaus:", t, h)
            code, body = send(t, h)
            print("TS:", code, body)
            if code == 200:
                led_blink(led, times=2)
                backoff = 1
        except Exception as e:
            print("Virhe mittauksessa/lähetyksessä:", e)
            safe_sleep(backoff)
            backoff = min(backoff * 2, 60)

        safe_sleep(PERIOD)

if __name__ == "__main__":
    main()
