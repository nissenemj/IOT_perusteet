# Sääasema: DHT lukema konsoliin + virheiden käsittely
from machine import Pin
from time import sleep
import dht

DHT_PIN = 13
sensor = dht.DHT22(Pin(DHT_PIN))

while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print("Temp: {:.1f} C  Hum: {:.1f} %".format(t, h))
    except Exception as e:
        print("DHT error:", e)
    sleep(2)
