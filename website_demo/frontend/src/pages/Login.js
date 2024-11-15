import React, { useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';

const Login = () => {
  const [data, setData] = useState({
    username: '',
    password: '',
  })
  const [encryptedData, setEncryptedData] = useState('');
  const [alertMessage, setAlertMessage] = useState(null);
  const [showAlert, setShowAlert] = useState(false);
  const [error, setError] = useState(null);

  const [socket, setSocket] = useState(null);

  const { login } = useAuth();
  const navigate = useNavigate();

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

  useEffect(() => {
    if (encryptedData) {
      (async () => {
        try {
          const response = await fetch('http://localhost:3001/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ encryptedData }),
          });

          if (response.ok) {
            const responseData = await response.json();
            login(data.username, responseData.accountBalance);
            navigate('/');
          } else {
            setAlertMessage('User does not exist or password is wrong');
            setShowAlert(true);
          }
        } catch (err) {
          console.error('Error during login:', err);
          setAlertMessage('Error occurred while logging in');
          setShowAlert(true);
        }
      })();
    }
  }, [encryptedData]);

  const handleLogin = async() => {
    try {
      if (!data.username || !data.password) {
        setAlertMessage('Please enter username and password');
        setShowAlert(true);
        return;
      }
      
      if (socket && socket.readyState === WebSocket.OPEN) {
        // Send message to Python server for encryption
        const client_data = "ENCRYPT:" + JSON.stringify(data);
        socket.send(client_data);
      } else {
        console.log("WebSocket not connected");
        setError("WebSocket connection is not established");
        return;
      }

    } catch (err) {
      setAlertMessage('Error occurred while logging in');
      setShowAlert(true);
      console.error(err);
    }
  }

  // Encrypt the message and send it over WebSocket
  const handleEncrypt = async () => {
    try {
      if (socket && socket.readyState === WebSocket.OPEN) {
        // Send message to Python server for encryption
        const client_data = "ENCRYPT:" + JSON.stringify(data);
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
    <h1 style={styles.title}>Bank Account Login</h1>
    <input
      type="text"
      placeholder="Enter username"
      autoComplete='off'
      value={data.username}
      onChange={(e) => {
        setData({
          ...data,
          username: e.target.value,
        })
        setEncryptedData('');
      }}
      style={styles.input}
    />
    <input
      type="password"
      placeholder="Enter password"
      autoComplete='off'
      value={data.password}
      onChange={(e) => {
        setData({
          ...data,
          password: e.target.value,
        })
        setEncryptedData('');
      }}
      style={styles.input}
    />
    <button onClick={handleLogin} style={styles.button}>Login</button>
    <button onClick={() => navigate('/register')} style={styles.createAccountButton}>Create Account</button>
  </div>
  
  {showAlert && (
    <div style={styles.alertOverlay}>
      <div style={styles.alertBox}>
        <p style={styles.alertText}>{alertMessage}</p>
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
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    background: 'linear-gradient(135deg, #73a5ff, #5477f5)',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  form: {
    backgroundColor: '#fff',
    padding: '40px',
    borderRadius: '10px',
    boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '400px',
    textAlign: 'center',
  },
  title: {
    fontSize: '2em',
    color: '#333',
    marginBottom: '20px',
  },
  input: {
    width: '100%',
    padding: '10px',
    margin: '10px 0',
    fontSize: '1em',
    borderRadius: '5px',
    border: '1px solid #ddd',
    boxSizing: 'border-box',
  },
  button: {
    backgroundColor: '#4CAF50',
    color: '#fff',
    padding: '10px 20px',
    marginTop: '15px',
    fontSize: '1em',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '5px',
    width: '100%',
    transition: 'background-color 0.3s ease',
  },
  createAccountButton: {
    marginTop: '15px',
    color: '#4CAF50',
    backgroundColor: 'transparent',
    border: 'none',
    fontSize: '0.9em',
    cursor: 'pointer',
    textDecoration: 'underline',
  },
  encryptedDataContainer: {
    marginTop: '20px',
    padding: '10px',
    backgroundColor: '#f4f4f4',
    borderRadius: '5px',
    wordWrap: 'break-word',
    overflowWrap: 'break-word',
    whiteSpace: 'normal',
  },
  encryptedText: {
    color: '#555',
    fontSize: '0.9em',
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
    borderRadius: '5px',
    width: '80%',
    maxWidth: '300px',
    textAlign: 'center',
  },
  alertText: {
    marginBottom: '15px',
    color: '#333',
  },
  closeButton: {
    padding: '10px 20px',
    fontSize: '1em',
    color: '#fff',
    backgroundColor: '#ff6b6b',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease',
  },
};


export default Login;

