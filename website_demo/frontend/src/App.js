import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState('');
  const [encryptedData, setEncryptedData] = useState('');
  const [message, setReceivedMessage] = useState('');
  const [error, setError] = useState('');

  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Create a new WebSocket connection when the component mounts
    const ws = new WebSocket('ws://localhost:4444'); 

    // Set up event handlers for WebSocket
    ws.onopen = () => {
      console.log("Connected to WebSocket server");
      setSocket(ws); // Store the WebSocket instance in the state
    };

    ws.onmessage = (event) => {
      const encryptedData = event.data;
      setEncryptedData(encryptedData);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
      setError('WebSocket connection failed'); // Set error state on connection failure
    };

    ws.onclose = () => {
      console.log("Disconnected from WebSocket server");
      setSocket(null); // Remove the WebSocket instance from the state
    };

    return () => {
      ws.close(); // Close WebSocket connection when the component unmounts
    };
  }
  , []);

  const handleLogin = async() => {
    console.log({"data": encryptedData})
    try {
      const response = await fetch('http://localhost:3001/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "data": encryptedData })
      });

      if (response.ok) {
        const data = await response.json();
        setReceivedMessage(data.message);
      } else {
        setError('Failed to decrypt message');
      }
    } catch (err) {
      setError('Error decrypting message');
      console.error(err);
    }
  }

  // Encrypt the message and send it over WebSocket
  const handleEncrypt = async () => {
    try {
      if (socket && socket.readyState === WebSocket.OPEN) {
        // Send message to Python server for encryption
        const client_data = "ENCRYPT:" + data;
        socket.send(client_data);
      } else {
        console.log("WebSocket not connected");
        setError("WebSocket connection is not established");
      }
    } catch (err) {
      setError('Error encrypting message');
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Padding Oracle Demo</h1>
      <input
        type="text"
        placeholder="Enter data"
        value={data}
        onChange={e => setData(e.target.value)}
      />
      <button onClick={handleEncrypt}>Encrypt</button>
      {encryptedData && 
        <>
        <button onClick={handleLogin}>Login</button>
        <div>
          <p>Encrypted Data: {encryptedData}</p>
        </div>
        </>
      }
    </div>
  );
}

export default App;
