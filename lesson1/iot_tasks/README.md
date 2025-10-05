# IOT-tehtävät — MicroPython

## 🔐 Turvallisuus

**TÄRKEÄÄ:** Tämä projekti käyttää `.gitignore`-tiedostoa estämään `config.py`:n pushamisen GitHubiin.

### Ensimmäinen käyttökerta:

1. Kopioi `config.example.py` -> `config.py`:
   ```bash
   cp config.example.py config.py
   ```

2. Muokkaa `config.py` ja lisää:
   - Wi-Fi SSID ja salasana
   - ThingSpeak API-avain (task13 varten)
   - Pinnit laitteesi mukaan (ESP8266/ESP32/Pico W)

3. **ÄLÄ** koskaan pushaa `config.py`:tä GitHubiin!

## 📁 Tiedostorakenne

```
iot_tasks/
├── .gitignore              # Estää config.py:n pushamisen
├── config.example.py       # Esimerkki-konfiguraatio (pushaa tämä)
├── config.py              # Omat asetuksesi (ÄLÄ pushaa!)
├── utils.py               # Apuluokat (WiFiHelper, Debouncer, Stats, jne.)
├── boot.py                # Valinnainen: auto-WiFi käynnistyksessä
├── main.py                # Valikkokäynnistin tehtävien ajamiseen
├── task01_print.py        # Tulosta numerot 0-9
├── task02_name.py         # Supersankari-tunnistus
├── task03_blink.py        # Sisäinen LED blink + PWM breathing
├── task04_timer_blink.py  # Timer-pohjainen blink
├── task05_external_led.py # Ulkoinen LED blink
├── task06_button_led.py   # Nappi ohjaa LEDiä
├── task07_traffic.py      # Liikennevalot
├── task08_reaction.py     # Reaktiopeli
├── task09_pir_alarm.py    # PIR-murtohälytin
├── task10_dht_console.py  # DHT-sääasema konsoliin
├── task11_dht_oled.py     # DHT-sääasema OLED-näytöllä
├── task12_pot_adc_pwm.py  # Potentiometri -> ADC -> PWM
├── task13_thingspeak.py   # DHT -> ThingSpeak (vaatii API-avaimen!)
├── task14_buzzer_pwm.py   # Buzzer PWM-äänimerkein
└── task15_button_irq.py   # Nappi keskeytyksenä
```

## 🚀 Käyttö

### Vaihtoehto 1: Aja yksittäinen tehtävä
```python
import task01_print
```

### Vaihtoehto 2: Käytä valikkoa (main.py)
```python
import main
```
Valitse tehtävä numerolla 1-15, tai `q` lopettaaksesi.

## 📝 Huomioita

- **Pinnit:** Muokkaa `config.py`:ssä olevat pinnit laitteesi mukaan
- **OLED (task11):** Vaatii `ssd1306`-kirjaston. Jos ei ole asennettuna, poista tai lataa kirjasto laitteelle
- **ThingSpeak (task13):** Vaatii `urequests`-kirjaston ja API-avaimen `config.py`:ssä
- **WiFi:** Käytä `WiFiHelper`-luokkaa `utils.py`:stä helppoon yhdistämiseen

## 🔧 Tekninen toteutus

Kaikki tehtävät on suunniteltu:
- ✅ Toimimaan itsenäisesti
- ✅ Käyttämään yhteistä konfiguraatiota (`config.py`)
- ✅ Hyödyntämään apuluokkia (`utils.py`)
- ✅ Robustisti virheenkäsittelyn kanssa
- ✅ Turvallisesti ilman API-avainten vuotamista GitHubiin

## 📚 Lisätiedot


