import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState('');
  const [encryptedData, setEncryptedData] = useState('');
  const [alertMessage, setAlertMessage] = useState(null);
  const [showAlert, setShowAlert] = useState(false);

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
        body: JSON.stringify({ "password": encryptedData }),
      });

      if (response.ok) {
        const data = await response.json();
        setAlertMessage("Login successful! Can check the console for the decrypted message");
        setShowAlert(true);
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
    <div style={styles.container}>
      <div style={styles.form}>
        <h1 style={styles.title}>Login Page</h1>
        <input
          type="text"
          placeholder="Enter password"
          autoComplete='off'
          value={data}
          onChange={(e) => setData(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleEncrypt} style={styles.button}>Encrypt</button>
        {encryptedData && (
          <>
            <button onClick={handleLogin} style={styles.button}>Login</button>
            <div style={styles.encryptedDataContainer}>
              <p style={styles.encryptedText}>Encrypted Data: {encryptedData}</p>
            </div>
          </>
        )}
      </div>
      {showAlert && (
        <div style={styles.alertOverlay}>
          <div style={styles.alertBox}>
            <p>{alertMessage}</p>
            <button onClick={() => setShowAlert(false)} style={styles.closeButton}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f0f2f5',
  },
  form: {
    width: '300px',
    padding: '60px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    backgroundColor: 'white',
    textAlign: 'center',
  },
  title: {
    fontSize: '40px',
    marginBottom: '40px',
    color: '#333',
  },
  input: {
    padding: '15px',
    width: '90%',
    marginBottom: '30px',
    borderRadius: '4px',
    border: '1px solid #ddd',
    fontSize: '20px',
  },
  button: {
    width: '100%',
    padding: '10px',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: 'white',
    fontSize: '20px',
    cursor: 'pointer',
    marginTop: '15px',
  },
  alertOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  alertBox: {
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
    width: '300px',
  },
  closeButton: {
    marginTop: '10px',
    padding: '5px 15px',
    cursor: 'pointer',
  },
  encryptedDataContainer: {
    marginTop: '30px',
    wordWrap: 'break-word',
    overflowWrap: 'break-word',
    backgroundColor: '#f7f7f7',
    padding: '10px',
    borderRadius: '4px',
  },
  encryptedText: {
    fontSize: '20px',
    color: '#666',
  },
};

export default App;
