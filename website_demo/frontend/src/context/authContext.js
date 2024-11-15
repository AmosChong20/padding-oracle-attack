// AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [balance, setBalance] = useState(0);

  const login = (username, accountBalance) => {
    setIsAuthenticated(true);
    setUser(username);
    setBalance(accountBalance);
    // Save token to localStorage or cookies for real apps
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUser(null);
    setBalance(0);
    // Remove token from localStorage or cookies for real apps
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, balance, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
