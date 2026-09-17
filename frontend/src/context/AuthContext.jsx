import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

const API = `${process.env.REACT_APP_BACKEND_URL || ''}/api`;

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('admin_token'));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    const verify = async () => {
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      try {
        const { data } = await axios.get(`${API}/admin/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (active) setUser(data);
      } catch (e) {
        if (active) {
          localStorage.removeItem('admin_token');
          setToken(null);
          setUser(null);
        }
      } finally {
        if (active) setLoading(false);
      }
    };
    verify();
    return () => {
      active = false;
    };
  }, [token]);

  const login = async (username, password) => {
    const { data } = await axios.post(`${API}/admin/login`, { username, password });
    localStorage.setItem('admin_token', data.access_token);
    setToken(data.access_token);
    setUser({ username: data.username, role: 'admin' });
    return data;
  };

  const logout = () => {
    localStorage.removeItem('admin_token');
    setToken(null);
    setUser(null);
  };

  const authHeader = () => (token ? { Authorization: `Bearer ${token}` } : {});

  return (
    <AuthContext.Provider value={{ token, user, loading, login, logout, authHeader }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
};
