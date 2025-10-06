# MicroPython: DHT -> ThingSpeak + Webhook example
# ESP8266/ESP32 version. Configure DHT_PIN, DHT_TYPE, SSID, PASSWORD and SERVER_URL.
#
# This script posts measurements both to ThingSpeak and to your own server webhook
# at SERVER_URL (POST /webhook). That lets the server broadcast via websockets and
# optionally forward to ThingSpeak or persist data.

import network
import time
import urequests
import dht
from machine import Pin

# --- Konfigurointi ---
SSID = 'Wokwi-GUEST'
PASSWORD = ''  # jätä tyhjäksi jos avoin verkko

THINGSPEAK_API_KEY = 'Q8I4WJ10G8GNYMUW'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Aseta oma palvelimen osoite, esim 'http://192.168.1.50:3000/webhook' tai ngrok-tunnelia
SERVER_WEBHOOK_URL = 'http://YOUR_SERVER_IP:3000/webhook'  # MUUTA TÄHÄN
# Tai käytä Wokwissa: 'https://iot-server.example.com/webhook'

DHT_PIN = 14           # Muuta laitteesi GPIO-pinniin (Wokwi: 14)
DHT_TYPE = 'DHT22'     # 'DHT22' tai 'DHT11'

SLEEP_SECONDS = 15     # ThingSpeak: varovasti; älä lähetä liian usein
SERVER_API_KEY = ''    # Lisää API-avain jos palvelin vaatii

# --- Alustus ---
if DHT_TYPE == 'DHT22':
    sensor = dht.DHT22(Pin(DHT_PIN))
else:
    sensor = dht.DHT11(Pin(DHT_PIN))

wlan = network.WLAN(network.STA_IF)

def connect_wifi(ssid, password, timeout=15):
    wlan.active(True)
    if wlan.isconnected():
        print('WiFi already connected:', wlan.ifconfig())
        return True

    print('Connecting to WiFi:', ssid)
    wlan.connect(ssid, password)
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            print('WiFi connection timed out.')
            return False
        time.sleep(1)
    print('Connected! IP:', wlan.ifconfig()[0])
    return True

def read_dht():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        return float(temp), float(hum)
    except Exception as e:
        print('DHT read failed:', e)
        return None, None

def send_to_thingspeak(api_key, temp, hum):
    try:
        url = '{base}?api_key={key}&field1={t}&field2={h}'.format(
            base=THINGSPEAK_URL, key=api_key, t=temp, h=hum)
        print('Sending to ThingSpeak:', url)
        resp = urequests.get(url)
        print('ThingSpeak status:', resp.status_code)
        resp.close()
        return resp.status_code
    except Exception as e:
        print('ThingSpeak send error:', e)
        return None

def post_to_server(webhook_url, temp, hum):
    try:
        payload = {'temp': temp, 'hum': hum, 'source': 'micropython_device'}
        headers = {'Content-Type': 'application/json'}
        if SERVER_API_KEY:
            headers['x-api-key'] = SERVER_API_KEY
        print('Posting to server webhook:', webhook_url, payload)
        resp = urequests.post(webhook_url, json=payload, headers=headers)
        print('Server webhook status:', resp.status_code)
        resp.close()
        return resp.status_code
    except Exception as e:
        print('Webhook post error:', e)
        return None

def main_loop():
    if not connect_wifi(SSID, PASSWORD):
        print('No WiFi - retry later.')
        return

    while True:
        temp, hum = read_dht()
        if temp is None or hum is None:
            print('Invalid DHT reading - retrying...')
            time.sleep(5)
            continue

        print('Measurement: temp', temp, 'C  hum', hum, '%')
        # Send to ThingSpeak
        ts_status = send_to_thingspeak(THINGSPEAK_API_KEY, temp, hum)
        # Post to your server webhook (so dashboard + websocket see it)
        webhook_status = post_to_server(SERVER_WEBHOOK_URL, temp, hum)

        time.sleep(SLEEP_SECONDS)

if __name__ == '__main__':
    try:
        main_loop()
    except Exception as e:
        print('Fatal error:', e)
