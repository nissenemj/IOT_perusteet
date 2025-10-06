// Simple Express server with Socket.io for real-time dashboard + webhook + ThingSpeak forwarding
// Usage: configure THINGSPEAK_API_KEY and optional SERVER_API_KEY in .env or environment variables.

const express = require('express');
const http = require('http');
const cors = require('cors');
const axios = require('axios');
const { Server } = require('socket.io');
const path = require('path');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

const PORT = process.env.PORT || 3000;
const THINGSPEAK_API_KEY = process.env.THINGSPEAK_API_KEY || 'Q8I4WJ10G8GNYMUW';
const SERVER_API_KEY = process.env.SERVER_API_KEY || ''; // optional simple auth for webhook
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL || ''; // Discord notifications
const TEMP_THRESHOLD_HIGH = parseFloat(process.env.TEMP_THRESHOLD_HIGH) || 30; // Alert if temp > 30°C
const TEMP_THRESHOLD_LOW = parseFloat(process.env.TEMP_THRESHOLD_LOW) || 10; // Alert if temp < 10°C

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend')));

// In-memory readings store (circular buffer)
const MAX_READINGS = 500;
const readings = [];

// Registered webhooks (external services can register to receive notifications)
const registeredWebhooks = [];

function pushReading(r) {
  readings.push(r);
  if (readings.length > MAX_READINGS) readings.shift();
}

// Simple API: get recent readings
app.get('/data', (req, res) => {
  res.json({ readings });
});

// CSV export
app.get('/export.csv', (req, res) => {
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', 'attachment; filename="readings.csv"');
  res.write('timestamp,temp,hum,source\n');
  readings.forEach(r => res.write(`${r.timestamp},${r.temp},${r.hum},${r.source}\n`));
  res.end();
});

// Webhook registration endpoints
app.post('/webhooks/register', (req, res) => {
  const { url, name } = req.body;
  if (!url || !name) {
    return res.status(400).json({ error: 'URL and name required' });
  }
  const id = Date.now().toString();
  registeredWebhooks.push({ id, url, name, created: new Date().toISOString() });
  console.log(`Webhook registered: ${name} -> ${url}`);
  res.json({ ok: true, id, message: 'Webhook registered successfully' });
});

app.get('/webhooks', (req, res) => {
  res.json({ webhooks: registeredWebhooks });
});

app.delete('/webhooks/:id', (req, res) => {
  const { id } = req.params;
  const index = registeredWebhooks.findIndex(w => w.id === id);
  if (index === -1) return res.status(404).json({ error: 'Webhook not found' });
  registeredWebhooks.splice(index, 1);
  res.json({ ok: true, message: 'Webhook deleted' });
});

// Helper function to notify registered webhooks
async function notifyWebhooks(reading) {
  for (const webhook of registeredWebhooks) {
    try {
      await axios.post(webhook.url, reading, { timeout: 5000 });
      console.log(`Notified webhook: ${webhook.name}`);
    } catch (err) {
      console.warn(`Failed to notify ${webhook.name}:`, err.message);
    }
  }
}

// Helper function to send Discord alert
async function sendDiscordAlert(message) {
  if (!DISCORD_WEBHOOK_URL) return;
  try {
    await axios.post(DISCORD_WEBHOOK_URL, { content: message }, { timeout: 5000 });
    console.log('Discord alert sent');
  } catch (err) {
    console.warn('Discord alert failed:', err.message);
  }
}

// Check temperature thresholds and send alerts
function checkThresholds(reading) {
  if (reading.temp > TEMP_THRESHOLD_HIGH) {
    const msg = `⚠️ High temperature alert! Current: ${reading.temp}°C (threshold: ${TEMP_THRESHOLD_HIGH}°C)`;
    console.log(msg);
    sendDiscordAlert(msg);
  } else if (reading.temp < TEMP_THRESHOLD_LOW) {
    const msg = `❄️ Low temperature alert! Current: ${reading.temp}°C (threshold: ${TEMP_THRESHOLD_LOW}°C)`;
    console.log(msg);
    sendDiscordAlert(msg);
  }
}

// Webhook endpoint for devices to POST measurements
app.post('/webhook', async (req, res) => {
  try {
    // optional API key check
    if (SERVER_API_KEY) {
      const key = req.headers['x-api-key'] || req.query.api_key;
      if (key !== SERVER_API_KEY) return res.status(401).json({ error: 'Unauthorized' });
    }

    const { temp, hum, source } = req.body;
    const timestamp = new Date().toISOString();
    const reading = { temp: Number(temp), hum: Number(hum), source: source || 'webhook', timestamp };
    pushReading(reading);

    // Broadcast to connected dashboards
    io.emit('reading', reading);

    // Check temperature thresholds
    checkThresholds(reading);

    // Notify registered webhooks
    notifyWebhooks(reading).catch(err => console.warn('Webhook notification error:', err));

    // Forward to ThingSpeak (GET request expected)
    try {
      const url = `https://api.thingspeak.com/update?api_key=${THINGSPEAK_API_KEY}&field1=${reading.temp}&field2=${reading.hum}`;
      const resp = await axios.get(url, { timeout: 5000 });
      console.log('ThingSpeak forwarded, status', resp.status);
    } catch (err) {
      console.warn('ThingSpeak forward failed:', err.message);
    }

    res.json({ ok: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

// Serve the frontend (index.html in ../frontend)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Socket.io connection
io.on('connection', (socket) => {
  console.log('Client connected', socket.id);
  // send recent readings on connect
  socket.emit('history', readings);

  // Handle commands from dashboard (can be forwarded to devices)
  socket.on('command', (cmd) => {
    console.log('Command received from client:', cmd);
    // Broadcast command to all clients (devices can listen to this)
    io.emit('device_command', cmd);
  });

  // Handle custom messages
  socket.on('message', (msg) => {
    console.log('Message from client:', msg);
    io.emit('broadcast', { from: socket.id, message: msg, timestamp: new Date().toISOString() });
  });

  socket.on('disconnect', () => console.log('Client disconnected', socket.id));
});

server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
  console.log(`ThingSpeak API key in use: ${THINGSPEAK_API_KEY ? 'yes' : 'no'}`);
  console.log(`Discord webhook: ${DISCORD_WEBHOOK_URL ? 'configured' : 'not configured'}`);
  console.log(`Temperature thresholds: ${TEMP_THRESHOLD_LOW}°C - ${TEMP_THRESHOLD_HIGH}°C`);
});
