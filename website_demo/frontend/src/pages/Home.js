import React, {useEffect, useState} from 'react';
import { useAuth } from '../context/authContext';

const Home = () => {
  const { user, balance, logout } = useAuth();
  const [localBalance, setBalance] = useState(balance);

  const handleTranfer = async () => {
    const response = await fetch('http://localhost:3001/make-payment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: user, amount: 1000 }),
    });
    const data = await response.json();
    setBalance(data.accountBalance);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Welcome, {user}!</h1>
        <p style={styles.subtitle}>Your account balance is S$ {localBalance.toLocaleString()}</p>
        <button 
          onClick={handleTranfer} 
          style={styles.transferButton}
        >
          Make a Payment
        </button>
        <button 
          onClick={logout} 
          style={styles.logoutButton}
        >
          Logout
        </button>
      </div>
    </div>
  );
};

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
  card: {
      textAlign: 'center',
      backgroundColor: '#fff',
      padding: '40px',
      borderRadius: '8px',
      boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
      maxWidth: '400px',
      width: '100%',
      transition: 'transform 0.2s ease-in-out',
  },
  title: {
      fontSize: '2em',
      color: '#333',
      margin: '0 0 10px',
  },
  subtitle: {
      fontSize: '1.2em',
      color: '#666',
      marginBottom: '20px',
  },
  transferButton: {
      backgroundColor: '#007bff',
      color: '#fff',
      padding: '10px 20px',
      marginRight: '10px',
      border: 'none',
      borderRadius: '5px',
      fontSize: '1em',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease',
  },
  logoutButton: {
      backgroundColor: '#ff6b6b',
      color: '#fff',
      padding: '10px 20px',
      border: 'none',
      borderRadius: '5px',
      fontSize: '1em',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease',
  },
};

export default Home;
