const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const WebSocket = require('ws');
const mongoose = require('mongoose');
const User = require('./models/user');
const bcrypt = require('bcrypt');

const app = express();
const PORT = 3001;
const SERVER_IP = 'ws://127.0.0.1';  // WebSocket protocol
const SERVER_PORT = 4444;

app.use(bodyParser.json());
app.use(cors());

// WebSocket client setup
const ws = new WebSocket(`${SERVER_IP}:${SERVER_PORT}`);

async function decryptMiddleware(req, res, next) {
  const { encryptedData } = req.body;

  if (!encryptedData) {
    return res.status(400).send({ error: 'No encrypted message provided' });
  }

  // Ensure the WebSocket client is connected before proceeding
  if (ws.readyState !== WebSocket.OPEN) {
    console.log('WebSocket connection not open');
    return res.status(500).send({ error: 'WebSocket connection not open' });
  }
  console.log(`Received encrypted data: ${encryptedData}`);
  // Send the encrypted message through the WebSocket
  console.log("----------------------Perform decryption----------------------");
  ws.send(encryptedData);

  // Handle the response from the WebSocket server
  ws.on('message', (data) => {
    console.log(`Decrypted data: ${data}`);
    const decryptedData = JSON.parse(data);
    req.body.decryptedData = decryptedData;
    next();
  });

  ws.on('error', (err) => {
    console.error('WebSocket connection error:', err);
    res.status(500).send({ error: 'Internal server error' });
  });
}

app.post('/register', decryptMiddleware, async (req, res) => {
  const { username, password } = req.body.decryptedData;

  try {
    const newUser = new User({ username, password });
    await newUser.save();

    res.status(200).json({
      message: 'User registered successfully',
      newUser: newUser._id
    })
  } catch (error) {
    console.error('Error registering user:', error);
    return res.status(500).send({ error: 'Internal server error' });
  }
});

app.post('/login', decryptMiddleware, async (req, res) => {
  const { username, password } = req.body.decryptedData;

  try {
    const user = await User.findOne({ username });

    if (!user) {
      return res.status(404).send({ error: 'User not found' });
    }

    // const isPasswordValid = bcrypt.compareSync(password, user.password);
    const isPasswordValid = password === user.password;
    if (!isPasswordValid) {
      return res.status(401).send({ error: 'Invalid password' });
    }

    res.status(200).json({ message: 'Login successful' });
  } catch (error) {
    console.error('Error logging in:', error);
    return res.status(500).send({ error: 'Internal server error' });
  }
});


const mongoURI = 'mongodb://localhost:27035/users';

mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const db = mongoose.connection;
db.on('error', (error) => console.error('MongoDB connection error:', error));
db.on('open', () => console.log('Connected to MongoDB'));

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
