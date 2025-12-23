import axios from 'axios';
import { useAppStore } from '../store/useAppStore';

// For iOS Simulator, localhost is fine.
// For Android Emulator, use 'http://10.0.2.2:8000'
const BASE_URL = 'http://localhost:8000/api'; 

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = useAppStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
