import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import apiClient from '../api/client';

export interface User {
  id: number;
  username: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  is_app_user: boolean;
  can_read_all: boolean;
  can_write_all: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  canRead: boolean;
  canWrite: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [isLoading, setIsLoading] = useState(true);

  // Load user on mount and token change
  useEffect(() => {
    const loadUser = async () => {
      if (!token) {
        setIsLoading(false);
        setUser(null);
        return;
      }

      try {
        const response = await apiClient.get('/auth/me');
        setUser(response.data);
      } catch (error) {
        // Token is invalid, clear it
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, [token]);

  const login = async (username: string, password: string) => {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await apiClient.post('/auth/token', formData);
      const { access_token } = response.data;

      localStorage.setItem('token', access_token);
      setToken(access_token);

      // Fetch user info
      const userResponse = await apiClient.get('/auth/me');
      setUser(userResponse.data);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = !!user && !!token;
  const isAdmin = user?.role === 'ROOT' || false;
  const canRead = isAdmin || user?.can_read_all || false;
  const canWrite = isAdmin || user?.can_write_all || false;

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isAuthenticated,
        canRead,
        canWrite,
        login,
        logout,
        isAdmin,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
