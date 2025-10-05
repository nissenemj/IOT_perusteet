# Valinnainen: auto-WiFi bootissa, ei pakollinen
import config
from utils import WiFiHelper

try:
    wifi = WiFiHelper(config.WIFI["SSID"], config.WIFI["PASSWORD"], timeout=10)
    wifi.connect()
except Exception as e:
    print("boot.py WiFi virhe:", e)
