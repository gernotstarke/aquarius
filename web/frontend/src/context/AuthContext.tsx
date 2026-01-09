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
      setIsLoading(true);

      try {
        const response = await apiClient.get('/auth/app-me');
        setUser(response.data);
      } catch (error) {
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
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      const response = await apiClient.post('/auth/token', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      });
      const { access_token } = response.data;

      localStorage.setItem('token', access_token);
      setToken(access_token);

      // Fetch user info
      const userResponse = await apiClient.get('/auth/app-me');
      setUser(userResponse.data);
    } catch (error: any) {
      // Extract error message from various error formats
      let errorMessage = 'Login failed';
      
      if (error?.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error?.message) {
        errorMessage = error.message;
      }
      
      throw new Error(errorMessage);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = !!user;
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
