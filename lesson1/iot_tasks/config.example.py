

WIFI = {
    "SSID": "YourWiFiName",     
    "PASSWORD": "YourPassword"   
}

# ThingSpeak
THINGSPEAK = {
    "API_KEY": "YOUR_API_KEY_HERE",  # Lisää oma ThingSpeak API-avain
    "URL": "https://api.thingspeak.com/update",
    "PERIOD_S": 15
}

PINS = {
    "LED_INTERNAL": "LED",  # Pico W: "LED", ESP32 usein 2
    "LED_EXT": 15,
    "BTN": 14,
    "BUZZ": 5,
    "DHT": 13,      # datapiuha
    "PIR": 16,
    "ADC_POT": 26,  # GP26/ADC0 (Pico)
    "I2C_SCL": 1,
    "I2C_SDA": 0,
    "RED": 2,
    "YEL": 3,
    "GRN": 4
}
