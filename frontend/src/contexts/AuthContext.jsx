import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check localStorage for existing session
    const storedUser = localStorage.getItem('tradalife_user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = (email, password) => {
    // Mock login - will be replaced with real API
    const mockUser = {
      id: Date.now().toString(),
      email,
      firstName: '',
      lastName: '',
      country: '',
      phone: '',
      kycStatus: 'pending',
      purchases: []
    };
    
    setUser(mockUser);
    localStorage.setItem('tradalife_user', JSON.stringify(mockUser));
    return mockUser;
  };

  const register = (email, password) => {
    // Mock register - will be replaced with real API
    const mockUser = {
      id: Date.now().toString(),
      email,
      firstName: '',
      lastName: '',
      country: '',
      phone: '',
      kycStatus: 'pending',
      purchases: []
    };
    
    setUser(mockUser);
    localStorage.setItem('tradalife_user', JSON.stringify(mockUser));
    return mockUser;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('tradalife_user');
  };

  const updateUser = (userData) => {
    const updatedUser = { ...user, ...userData };
    setUser(updatedUser);
    localStorage.setItem('tradalife_user', JSON.stringify(updatedUser));
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};