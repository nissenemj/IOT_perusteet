const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
const DISCORD_WEBHOOK_URL = `https://discord.com/api/webhooks/1424409531403735131/EfxyuJzdnSQaJATpe9S7IKrG78xHk7snq9XcL01YShq5eFhnhC-E68p8hYYG-BgjBGuJ`;

// Middleware JSON-datan käsittelyyn
app.use(express.json());

// Webhook-endpoint
app.get('/webhook', (req, res) => {
    res.send('Webhook-endpoint on valmis vastaanottamaan POST-pyyntöjä.');
});

app.post('/webhook', (req, res) => {
    console.log('Webhook vastaanotettu:');
    console.log('Headers:', req.headers);
    console.log('Body:', req.body);

    // Vastaa onnistuneesti
    res.status(200).json({
        message: 'Webhook vastaanotettu onnistuneesti',
        timestamp: new Date().toISOString()
    });
});

app.post('/notify', async (req, res) => {
    const { message } = req.body;
    if (!message) {
        return res.status(400).json({ error: 'Väärä viesti' });
    }

    fetch(DISCORD_WEBHOOK_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: message })
    })
    .then(response => {
        if (response.ok) {
            res.status(200).json({ message: 'Discord viesti lähetetty' });
        } else {
            throw new Error(`Discord vastasi virheellisesti ${response.status}`);
        }
    })
    .catch(error => {
        res.status(500).json({ error: 'Discord viestin lähettämisessä virhe' });
    });
});


// Favicon-reitti (estää 404-virheet)
app.get('/favicon.ico', (_req, res) => {
    res.status(204).end();
});

// Tervetuliaisviesti juuressa
app.get('/', (req, res) => {
    res.send('Webhook-palvelin käynnissä. Lähetä POST-pyyntö /webhook-osoitteeseen.');
});

// Palvelimen käynnistys
app.listen(PORT, () => {
    console.log(`Webhook-palvelin kuuntelee portissa ${PORT}`);
    console.log(`Webhook-URL: http://localhost:${PORT}/webhook`);
});
