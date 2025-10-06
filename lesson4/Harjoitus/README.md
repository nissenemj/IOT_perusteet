# IoT Complete Pipeline (Device → Server → Dashboard)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Node](https://img.shields.io/badge/node-%3E%3D18-green.svg)

Tämä projekti demonstroi täydellisen IoT-pipelinen, joka sisältää:

1. **Device**: MicroPython-koodi ESP8266/ESP32 + DHT11/DHT22 -sensorille
   - Lähettää lämpötila- ja kosteustiedot palvelimelle (webhook)
   - Tukee ThingSpeak-integrointia
   - Wokwi-simulaatio tuettu

2. **Server**: Node.js/Express-palvelin WebSocket- ja webhook-tuella
   - Vastaanottaa dataa laitteelta
   - Lähettää real-time päivityksiä frontendille (Socket.io)
   - Webhook-rekisteröintijärjestelmä ulkoisille palveluille
   - Lämpötila-hälytysjärjestelmä (Discord-notifikaatiot)
   - CSV-datavienti
   - ThingSpeak-integraatio

3. **Frontend**: Moderni dashboard Chart.js-kaavioilla
   - 3 kaavio: lämpötila, kosteus, yhdistetty
   - Real-time tilastotiedot (min/max/avg)
   - WebSocket-yhteys real-time päivityksiin
   - Taulukkonäkymä viimeisimmistä mittauksista

## Ominaisuudet

###  Perusominaisuudet
- Real-time WebSocket-päivitykset (Socket.io)
- Webhook-endpoint laitteille
- Automaattinen edelleenlähetys ThingSpeakiin
- CSV-vienti (`/export.csv`)
- JSON API (`GET /data`)
- API-avainsuojaus (`x-api-key` header)
- Docker-tuki

---

##  Asennusohjeet

### 1️ Palvelimen asennus ja käynnistys

```bash
# Siirry server-kansioon
cd server

# Asenna riippuvuudet
npm install

# Kopioi .env.example -> .env ja muokkaa asetukset
cp .env.example .env
# Muokkaa .env-tiedostoa: THINGSPEAK_API_KEY, DISCORD_WEBHOOK_URL jne.

# Käynnistä palvelin
npm start
```

Palvelin käynnistyy osoitteessa `http://localhost:3000`

### 2️ Laitteen asennus (MicroPython)

**Vaihtoehdot:**
- **A) Fyysinen ESP32/ESP8266 + DHT-sensori**
- **B) Wokwi-simulaatio (suositus testaamiseen)**

#### A) Fyysinen laite:
1. Muokkaa `device/micropython_dht_thingspeak.py`:
   ```python
   SSID = 'YourWiFi'
   PASSWORD = 'YourPassword'
   SERVER_WEBHOOK_URL = 'http://YOUR_SERVER_IP:3000/webhook'
   DHT_PIN = 14  # GPIO-pinni
   ```

2. Lataa koodi ESP-laitteelle Thonny/ampy/mpremote-työkalulla

3. Käynnistä laite → alkaa lähettää dataa

#### B) Wokwi-simulaatio:
1. Mene osoitteeseen [wokwi.com](https://wokwi.com)
2. Luo uusi ESP32-projekti
3. Kopioi `device/diagram.json` ja `device/micropython_dht_thingspeak.py`
4. Muokkaa `SERVER_WEBHOOK_URL` osoittamaan palvelimellesi (käytä ngrok/cloudflare tunnel jos paikallinen)
5. Käynnistä simulaatio

### 3️ Avaa dashboard

Avaa selaimessa: `http://localhost:3000`

---

##  IoT-pipeline toiminta

```
[ESP32 + DHT] → (WiFi) → [Node.js Server] → (WebSocket) → [Dashboard]
                              ↓
                         [ThingSpeak]
                              ↓
                      [Discord Alerts]
                              ↓
                    [Registered Webhooks]
```

### Data flow:
1. **Laite** lukee lämpötilan ja kosteuden DHT-sensorista
2. **Laite** lähettää JSON `{ temp, hum, source }` palvelimen webhookiin
3. **Palvelin**:
   - Tallentaa datan muistiin (circular buffer, max 500)
   - Lähettää WebSocketilla dashboardille (`socket.emit('reading')`)
   - Tarkistaa raja-arvot ja lähettää hälytyksen Discordiin tarvittaessa
   - Välittää datan ThingSpeakiin
   - Lähettää datan rekisteröidyille webhookeille
4. **Dashboard** päivittää kaaviot ja tilastot real-time

---

## 📊 API Endpoints

### Laite-webhook
```http
POST /webhook
Content-Type: application/json
x-api-key: YOUR_API_KEY (jos SERVER_API_KEY asetettu)

Body:
{
  "temp": 23.5,
  "hum": 65.2,
  "source": "device_name"
}
```

### Datanäkymä
```http
GET /data
→ { readings: [...] }
```

### CSV-vienti
```http
GET /export.csv
→ Lataa CSV-tiedosto
```

### Webhook-rekisteröinti
```http
POST /webhooks/register
Content-Type: application/json

Body:
{
  "url": "https://example.com/my-webhook",
  "name": "My Service"
}
```

```http
GET /webhooks
→ { webhooks: [...] }

DELETE /webhooks/:id
→ Poista webhook
```

## 🐳 Docker (valinnainen)

```bash
# Rakenna image
docker build -t iot-pipeline ./server

# Käynnistä container
docker run -p 3000:3000 --env-file server/.env -d iot-pipeline
```

---

##  Testausohjeet

### 1. Testaa palvelin manuaalisesti:

```bash
# Käynnistä palvelin
cd server && npm start

# Toisessa terminaalissa: lähetä testidataa
curl -X POST http://localhost:3000/webhook \
  -H "Content-Type: application/json" \
  -d '{"temp": 22.5, "hum": 60, "source": "test"}'
```

### 2. Avaa dashboard selaimessa:
- `http://localhost:3000`
- Tarkista että kaaviot päivittyvät

### 3. Testaa Wokwi-simulaatio:
- Lataa `device/`-kansion tiedostot Wokwiin
- Aseta palvelimen URL (käytä ngrok jos paikallinen)
- Käynnistä simulaatio ja tarkista data

### 4. Testaa webhook-rekisteröinti:

```bash
curl -X POST http://localhost:3000/webhooks/register \
  -H "Content-Type: application/json" \
  -d '{"url": "https://webhook.site/your-id", "name": "Test Service"}'
```

---

##  Projektirakenteen yhteenveto

```
lesson4/Harjoitus/
├── device/
│   ├── micropython_dht_thingspeak.py  # MicroPython-koodi laitteelle
│   ├── diagram.json                    # Wokwi-kytkentäkaavio
│   └── wokwi.toml                      # Wokwi-konfiguraatio
├── server/
│   ├── index.js                        # Express-palvelin + Socket.io
│   ├── package.json                    # npm-riippuvuudet
│   ├── .env.example                    # Ympäristömuuttuja-esimerkki
│   └── Dockerfile                      # Docker-konfiguraatio
├── frontend/
│   └── index.html                      # Dashboard (Chart.js + Socket.io)
└── README.md                           # Tämä tiedosto
```

