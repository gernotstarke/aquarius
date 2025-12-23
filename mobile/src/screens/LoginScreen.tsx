import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert, Image } from 'react-native';
import { useAppStore } from '../store/useAppStore';
import apiClient from '../api/client';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { SafeAreaView } from 'react-native-safe-area-context';

export const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const setAuth = useAppStore((state) => state.setAuth);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Fehler', 'Bitte Benutzernamen und Passwort eingeben.');
      return;
    }

    setLoading(true);
    try {
      // 1. Get Token
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await apiClient.post('/auth/token', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const { access_token } = response.data;

      // 2. Get User Details
      // Need to temporarily set token in store or header for this request? 
      // Client interceptor reads from store, so we might need to set it first or pass explicitly.
      // Let's manually add header here for simplicity or update store optimistically.
      // Actually, standard OAuth flow often returns user info or we call /me.
      
      const meResponse = await apiClient.get('/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      setAuth(access_token, meResponse.data);
      
    } catch (error: any) {
      console.error(error);
      Alert.alert('Login fehlgeschlagen', 'Überprüfen Sie Ihre Zugangsdaten.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>Arqua42</Text>
          <Text style={styles.subtitle}>Offiziellen-Login</Text>
        </View>

        <View style={styles.form}>
          <Input 
            label="Benutzername"
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
          />
          <Input 
            label="Passwort"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
          
          <Button 
            title="Anmelden" 
            onPress={handleLogin} 
            loading={loading} 
          />
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 48,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#0f172a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 18,
    color: '#64748b',
  },
  form: {
    backgroundColor: 'white',
    padding: 24,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
});
