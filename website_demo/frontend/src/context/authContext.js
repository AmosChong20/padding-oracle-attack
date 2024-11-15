// AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  const login = (username) => {
    setIsAuthenticated(true);
    setUser(username);
    // Save token to localStorage or cookies for real apps
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUser(null);
    // Remove token from localStorage or cookies for real apps
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
