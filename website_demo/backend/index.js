const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const WebSocket = require('ws');

const app = express();
const PORT = 3001;
const SERVER_IP = 'ws://127.0.0.1';  // WebSocket protocol
const SERVER_PORT = 4444;

app.use(bodyParser.json());
app.use(cors());

// WebSocket client setup
const ws = new WebSocket(`${SERVER_IP}:${SERVER_PORT}`);

async function decryptMiddleware(req, res, next) {
  const { password } = req.body;
  console.log("Received data: ", password);
  if (!password) {
    return res.status(400).send({ error: 'No encrypted message provided' });
  }

  // Ensure the WebSocket client is connected before proceeding
  if (ws.readyState !== WebSocket.OPEN) {
    console.log('WebSocket connection not open');
    return res.status(500).send({ error: 'WebSocket connection not open' });
  }

  // Send the encrypted message through the WebSocket
  console.log("----------------------Perform decryption----------------------");
  ws.send(password);

  // Handle the response from the WebSocket server
  ws.on('message', (data) => {
    req.decryptedData = data.toString(); // Convert the buffer to string
    next();
  });

  ws.on('error', (err) => {
    console.error('WebSocket connection error:', err);
    res.status(500).send({ error: 'Internal server error' });
  });
}

app.post('/login', decryptMiddleware, (req, res) => {
  console.log("Decrypted data: ", req.decryptedData);
  
  // You can send a response after decryption
  res.status(200).json({ message: 'Successfully decrypted the data', decryptedData: req.decryptedData });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
